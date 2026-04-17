"""Syntactic alias expansion — candidate extraction, LLM call, cache.

Runs before bucketing. Produces an ``AliasMap`` that the role
classifier uses to recognize resource words in URL segments, path
params, and schema references.

The LLM sees a closed candidate list (extracted deterministically
from the spec) and picks which words are syntactic aliases for each
canonical resource. It cannot invent words — only select from the
list we give it. Role words like "assignee" are explicitly excluded
in the prompt and deferred to step 6 (unresolved-FK classification).

Cache contract:

    The output is persisted to ``<output_dir>/resource_vocabulary.json``
    with a ``cache_key`` derived from the hashable inputs (resources,
    candidate vocabulary, model ID, prompt version, pinned aliases).
    On re-run, if the cache file exists and its key matches, we skip
    the LLM call. Any input change invalidates the cache.
"""

from __future__ import annotations

import hashlib
import json
import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from pipeline.naming import singularize

from . import load_prompt_template
from ._text import snake_case, tokenize
from .claude_cli import call_claude_json, ClaudeCliJsonParseError
from .config import FkNamingConfig


logger = logging.getLogger(__name__)


# Version the prompt file so cache keys invalidate when we change it.
# Bump this whenever ``prompts/syntactic_aliases.md`` is edited in a
# way that could change outputs.
PROMPT_VERSION: str = "v1"

VOCABULARY_CACHE_FILENAME: str = "resource_vocabulary.json"


@dataclass
class ResourceAliasEntry:
    """One resource's full alias set after expansion.

    ``canonical`` is the plural form the user declared in config.
    ``singular`` is the deterministic singularization (used by the
    classifier for fk_column stem matching). ``syntactic_aliases``
    are the additional words picked by the LLM or pinned by the user.
    ``pinned_by_user`` flags whether the user's ``resource_aliases``
    config contributed any of them — useful for debugging.
    """

    canonical: str
    singular: str
    syntactic_aliases: list[str] = field(default_factory=list)
    pinned_by_user: bool = False
    source: str = "llm"  # "llm" | "user_config" | "mixed"


@dataclass
class AliasMap:
    """The full alias expansion artifact.

    Two views over the same underlying data:
      * ``entries`` — per-canonical entries with their alias lists.
      * ``lookup`` — flat word → canonical dict for O(1) classifier lookups.
    """

    entries: dict[str, ResourceAliasEntry]
    lookup: dict[str, str]
    unmatched_vocabulary: list[str]
    cache_key: str
    cache_hit: bool = False


# ---------------------------------------------------------------------------
# Candidate vocabulary extraction — pure function, no LLM
# ---------------------------------------------------------------------------


# Words we never want to hand the LLM as candidates. These are HTTP
# verbs, common action words, and structural keywords that appear in
# nearly every spec but are never aliases for anything.
_VOCABULARY_STOPLIST: frozenset[str] = frozenset({
    # Action / verb words
    "archive", "unarchive", "close", "reopen", "move", "duplicate",
    "rename", "shared", "remove", "add", "delete", "create", "update",
    "list", "get", "post", "put", "patch", "search", "query", "find",
    "batch", "bulk", "import", "export", "sync", "refresh", "reset",
    "enable", "disable", "activate", "deactivate", "lock", "unlock",
    "subscribe", "unsubscribe", "follow", "unfollow", "star", "unstar",
    "restore", "revert", "rollback", "merge", "rebase", "squash",
    "convert", "transfer", "fork", "clone",
    # Common structural wrappers / envelopes
    "data", "meta", "metadata", "pagination", "links", "_links",
    "_embedded", "error", "errors", "response", "request", "body",
    "payload", "attributes", "relationships", "included", "self",
    "next", "prev", "previous", "first", "last",
    # Common property-name fragments that carry no resource info
    "id", "type", "kind", "name", "title", "description", "status",
    "state", "created", "updated", "deleted", "modified", "at",
    "by", "count", "total", "page", "size", "limit", "offset",
    "cursor", "filter", "sort", "order", "direction", "query",
    "since", "until", "before", "after", "from", "to",
})

def extract_candidate_vocabulary(
    spec: dict[str, Any],
    ignore_key_patterns: list[str] | None = None,
    ignore_value_patterns: list[str] | None = None,
    ignore_token_patterns: list[str] | None = None,
) -> list[str]:
    """Extract candidate words the LLM will classify as aliases.

    Two sources:

    1. **Every string in the entire spec** — we walk the full spec
       tree and tokenize every string we encounter, whether it's a
       dict key, a dict value, or an item in a list. This catches
       URL segments, operation summaries, parameter names, schema
       property names, enum values, ``$ref`` pointers, example
       values — everything. The philosophy is "cast a wide net":
       false positives are cheap because the stoplist drops common
       junk (``id``, ``type``, ``at``, HTTP verbs, structural
       wrappers) and the LLM filters whatever slips through at
       classification time. Missed aliases are expensive, because
       the downstream walker has no way to recover them.

    2. **Component schema names with snake_case splitting** —
       ``components.schemas`` keys like ``PullRequest`` are
       usually CamelCase. The generic walker lowercases them into
       one fused token (``pullrequest``) which isn't useful. This
       source runs snake_case first so they split into the parts
       that actually match canonical resources (``pull`` / ``request``
       → ``pulls``).

    Three optional filter lists prune candidates at three layers:

      * ``ignore_key_patterns`` — regex patterns matched (via
        ``re.fullmatch``) against dict keys during the walk. Matching
        keys cause both the key AND their entire value subtree to be
        skipped. Use for wholesale exclusions like ``^description$``
        or ``^\\$ref$``.
      * ``ignore_value_patterns`` — regex patterns matched (via
        ``re.fullmatch``) against each raw string value BEFORE it's
        tokenized. Raw case is preserved during matching, so
        patterns can target ``ALL_CAPS`` enum values
        (``^[A-Z][A-Z0-9_]*$``) or standalone hash strings
        (``^[a-zA-Z0-9]{31,}$``). Applied at every tokenize call
        site — string leaves, dict keys, and source-2 schema names.
      * ``ignore_token_patterns`` — regex patterns matched (via
        ``re.fullmatch``) against each token AFTER tokenization.
        This is the post-tokenize layer: it catches tokens that only
        become visible once ``tokenize`` has split a longer string.
        Most commonly hashes embedded in URLs, which
        ``ignore_value_patterns`` can't see because the whole URL
        doesn't match the hash pattern. Example:
        ``^[a-zA-Z0-9]{31,}$`` applied here catches the
        ``3a0f86fb8db8eea7ccbb9a95f325ddbedfb25e15`` token that
        comes out of
        ``https://api.github.com/repos/octocat/example/git/blobs/3a0f86...``.

    The stoplist removes verbs and structural keywords; the singular/
    plural relationship is preserved (both ``repo`` and ``repos`` pass
    through) so the LLM can decide which variants are in play.

    Returns a sorted list for deterministic cache keying.
    """
    # Compile once up front. Empty lists mean "apply no filter".
    compiled_key_ignores: list[re.Pattern[str]] = [
        re.compile(pattern) for pattern in (ignore_key_patterns or [])
    ]
    compiled_value_ignores: list[re.Pattern[str]] = [
        re.compile(pattern) for pattern in (ignore_value_patterns or [])
    ]
    compiled_token_ignores: list[re.Pattern[str]] = [
        re.compile(pattern) for pattern in (ignore_token_patterns or [])
    ]

    vocab: set[str] = set()

    # Source 1: iterative walk of the whole spec. Every string we hit
    # — dict key, dict value, or list element — gets tokenized. An
    # explicit stack (rather than recursion) avoids both a helper
    # function and any recursion-depth concerns on deeply nested
    # specs. Dict keys matching any key-ignore pattern cause the
    # value to be skipped entirely; string values matching any
    # value-ignore pattern are skipped before tokenization so the
    # raw case (``ALL_CAPS``) is still visible.
    stack: list[Any] = [spec]
    while stack:
        node = stack.pop()
        if isinstance(node, str):
            if any(pattern.fullmatch(node) for pattern in compiled_value_ignores):
                continue
            for token in tokenize(node):
                vocab.add(token)
        elif isinstance(node, dict):
            for key, value in node.items():
                if isinstance(key, str):
                    if any(
                        pattern.fullmatch(key) for pattern in compiled_key_ignores
                    ):
                        # Skip both the key and its entire subtree.
                        continue
                    if not any(
                        pattern.fullmatch(key) for pattern in compiled_value_ignores
                    ):
                        for token in tokenize(key):
                            vocab.add(token)
                stack.append(value)
        elif isinstance(node, list):
            stack.extend(node)

    # Source 2: component schema names, snake-cased first so
    # CamelCase runs split into their parts rather than becoming
    # one fused token. The generic walker already tokenized the
    # lowercased form; this adds the split variants alongside.
    # Not subject to ``ignore_key_patterns`` (that's a walker-level
    # filter), but IS subject to ``ignore_value_patterns`` so a user
    # who blocks ``ALL_CAPS`` values also blocks any schema whose
    # name is in that shape.
    schemas = (spec.get("components") or {}).get("schemas") or {}
    for schema_name in schemas.keys():
        if not isinstance(schema_name, str):
            continue
        if any(pattern.fullmatch(schema_name) for pattern in compiled_value_ignores):
            continue
        for token in tokenize(snake_case(schema_name)):
            vocab.add(token)

    # Drop stoplisted tokens first, then apply the post-tokenize
    # ignore patterns. We do both at the end so the patterns can
    # see every candidate token, including ones produced by splitting
    # on underscores inside ``tokenize`` or by snake-casing a CamelCase
    # schema name.
    final = vocab - _VOCABULARY_STOPLIST
    if compiled_token_ignores:
        final = {
            token for token in final
            if not any(pattern.fullmatch(token) for pattern in compiled_token_ignores)
        }
    return sorted(final)


# ---------------------------------------------------------------------------
# Cache key + artifact I/O
# ---------------------------------------------------------------------------


def compute_cache_key(
    resources: list[str],
    vocabulary: list[str],
    pinned_aliases: dict[str, str],
    model: str,
    prompt_version: str,
) -> str:
    """Deterministic cache key over the hashable LLM-call inputs.

    Any change to the inputs invalidates the cache and triggers a
    re-run. We canonicalize by sorting so the order doesn't matter.
    """
    h = hashlib.sha256()
    payload = {
        "resources": sorted(resources),
        "vocabulary": sorted(vocabulary),
        "pinned_aliases": {k: pinned_aliases[k] for k in sorted(pinned_aliases)},
        "model": model,
        "prompt_version": prompt_version,
    }
    h.update(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode())
    return h.hexdigest()


def load_cached_vocabulary(
    cache_path: Path,
    expected_key: str,
) -> AliasMap | None:
    """Load the cache file if it exists and matches the expected key.

    Returns None on any mismatch (missing file, corrupted JSON, key
    mismatch). Callers re-run the LLM in those cases.
    """
    if not cache_path.exists():
        return None
    try:
        data = json.loads(cache_path.read_text())
    except (json.JSONDecodeError, OSError):
        return None
    if not isinstance(data, dict):
        return None
    meta = data.get("_meta") or {}
    if meta.get("cache_key") != expected_key:
        return None

    entries_raw = data.get("aliases") or {}
    if not isinstance(entries_raw, dict):
        return None

    entries: dict[str, ResourceAliasEntry] = {}
    for canonical, raw in entries_raw.items():
        if not isinstance(raw, dict):
            return None
        entries[canonical] = ResourceAliasEntry(
            canonical=canonical,
            singular=raw.get("singular", singularize(canonical)),
            syntactic_aliases=list(raw.get("syntactic_aliases") or []),
            pinned_by_user=bool(raw.get("pinned_by_user", False)),
            source=raw.get("source", "llm"),
        )

    lookup = _build_lookup(entries)
    unmatched = list(data.get("unmatched_vocabulary") or [])

    return AliasMap(
        entries=entries,
        lookup=lookup,
        unmatched_vocabulary=unmatched,
        cache_key=expected_key,
        cache_hit=True,
    )


def write_vocabulary_artifact(
    alias_map: AliasMap,
    cache_path: Path,
    source_spec: str,
    model: str,
    vocabulary_size: int,
) -> None:
    """Serialize the AliasMap to ``resource_vocabulary.json``."""
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    payload: dict[str, Any] = {
        "_meta": {
            "cache_key": alias_map.cache_key,
            "model": model,
            "prompt_version": PROMPT_VERSION,
            "source_spec": source_spec,
            "user_resource_count": len(alias_map.entries),
            "spec_vocabulary_size": vocabulary_size,
        },
        "aliases": {
            canonical: {
                "canonical": entry.canonical,
                "singular": entry.singular,
                "syntactic_aliases": sorted(entry.syntactic_aliases),
                "pinned_by_user": entry.pinned_by_user,
                "source": entry.source,
            }
            for canonical, entry in sorted(alias_map.entries.items())
        },
        "unmatched_vocabulary": sorted(alias_map.unmatched_vocabulary),
    }
    cache_path.write_text(json.dumps(payload, indent=2) + "\n")


# ---------------------------------------------------------------------------
# LLM call + merge logic
# ---------------------------------------------------------------------------


def expand_aliases(
    resources: list[str],
    spec: dict[str, Any],
    naming: FkNamingConfig,
    model: str,
    output_dir: Path,
    source_spec_path: str,
    *,
    use_cache: bool = True,
    vocabulary_ignore_keys: list[str] | None = None,
    vocabulary_ignore_values: list[str] | None = None,
    vocabulary_ignore_tokens: list[str] | None = None,
) -> AliasMap:
    """Produce an AliasMap for the given resources via LLM classification.

    This is the public entry point. Steps:
      1. Extract candidate vocabulary from the spec (honoring
         ``vocabulary_ignore_keys`` — regex patterns matched against
         dict keys to skip entire subtrees wholesale — and
         ``vocabulary_ignore_values`` — regex patterns matched
         against raw string values before tokenization, useful for
         ``ALL_CAPS`` enum values and hash-shaped opaque IDs).
      2. Compute cache key. If ``use_cache`` is True and the cache
         file matches, return it.
      3. Otherwise call the LLM, merge with pinned user aliases, write
         the cache file, and return the result.

    ``use_cache=False`` forces regeneration even when a matching cache
    file exists. The regenerated result is still written to disk, so
    the next run with ``use_cache=True`` will pick it up.

    Pinned user aliases ALWAYS win. If the user declared
    ``repository: repos`` in config, the LLM cannot override that
    (and if it tries to assign ``repository`` somewhere else, we
    reject its assignment).
    """
    vocabulary = extract_candidate_vocabulary(
        spec,
        ignore_key_patterns=vocabulary_ignore_keys,
        ignore_value_patterns=vocabulary_ignore_values,
        ignore_token_patterns=vocabulary_ignore_tokens,
    )

    # Pinned aliases are already validated against ``scoped_resources``
    # by ``config._load_naming`` at load time, so we can trust the dict
    # here — every value is guaranteed to be in ``resources``.
    pinned: dict[str, str] = dict(naming.resource_aliases)

    cache_key = compute_cache_key(
        resources, vocabulary, pinned, model, PROMPT_VERSION
    )
    cache_path = output_dir / VOCABULARY_CACHE_FILENAME

    if use_cache:
        cached = load_cached_vocabulary(cache_path, cache_key)
        if cached is not None:
            logger.info("  [cache hit] %s", cache_path)
            return cached
    else:
        logger.info("  [cache disabled] regenerating aliases via LLM")

    logger.info(
        "  [llm] calling %s to classify %d candidate words across %d resources",
        model, len(vocabulary), len(resources),
    )

    llm_aliases = _call_alias_llm(resources, vocabulary, model)
    alias_map = _merge_aliases(
        resources=resources,
        vocabulary=vocabulary,
        pinned=pinned,
        llm_aliases=llm_aliases,
        cache_key=cache_key,
    )

    write_vocabulary_artifact(
        alias_map,
        cache_path,
        source_spec=source_spec_path,
        model=model,
        vocabulary_size=len(vocabulary),
    )
    logger.info("  [write] %s", cache_path)

    return alias_map


def _call_alias_llm(
    resources: list[str],
    vocabulary: list[str],
    model: str,
) -> dict[str, list[str]]:
    """Run the LLM call and return its alias assignments.

    Returns a mapping canonical_resource → list of aliases chosen from
    the candidate vocabulary. Any aliases the LLM returns that are NOT
    in the vocabulary list are dropped silently (defensive against
    hallucinations, even though the prompt forbids them).
    """
    prompt_template = _load_prompt_template()
    prompt = prompt_template.replace(
        "{CANONICAL_RESOURCES_JSON}",
        json.dumps(resources, indent=2),
    ).replace(
        "{CANDIDATE_VOCABULARY_JSON}",
        json.dumps(vocabulary, indent=2),
    )

    try:
        response = call_claude_json(prompt, model=model, max_retries=1)
    except ClaudeCliJsonParseError as e:
        raise RuntimeError(
            "LLM alias expansion failed: claude returned unparseable JSON "
            f"after retry.\nRaw response head:\n{(e.stdout or '')[:800]}"
        ) from e

    if not isinstance(response, dict):
        raise RuntimeError(
            f"LLM alias response is not a JSON object: {type(response).__name__}"
        )

    raw_aliases = response.get("aliases") or {}
    if not isinstance(raw_aliases, dict):
        raise RuntimeError(
            f"LLM alias response.aliases is not a mapping: {type(raw_aliases).__name__}"
        )

    # Validate and filter.
    vocab_set = set(vocabulary)
    result: dict[str, list[str]] = {}
    for canonical in resources:
        entries = raw_aliases.get(canonical) or []
        if not isinstance(entries, list):
            entries = []
        clean: list[str] = []
        for word in entries:
            if not isinstance(word, str):
                continue
            if word not in vocab_set:
                # Hallucination — drop silently.
                continue
            if word == canonical:
                # Canonical is implicit; don't duplicate it.
                continue
            clean.append(word)
        result[canonical] = clean

    return result


def _merge_aliases(
    resources: list[str],
    vocabulary: list[str],
    pinned: dict[str, str],
    llm_aliases: dict[str, list[str]],
    cache_key: str,
) -> AliasMap:
    """Merge LLM output with pinned user aliases.

    Rules:
      * Pinned aliases always win. If the user declared ``repository
        → repos``, that's the assignment regardless of LLM output.
      * An alias assigned to a pinned canonical cannot also appear
        under a different canonical's LLM list.
      * Each canonical resource gets: its singular (deterministic),
        plus its pinned aliases, plus LLM aliases that survived
        validation.
      * Every word ends up in exactly one place: a canonical's alias
        set, or the ``unmatched_vocabulary`` list.
    """
    entries: dict[str, ResourceAliasEntry] = {}
    claimed: set[str] = set()

    for canonical in resources:
        singular = singularize(canonical)
        entries[canonical] = ResourceAliasEntry(
            canonical=canonical,
            singular=singular,
            syntactic_aliases=[],
            pinned_by_user=False,
            source="llm",
        )
        # The canonical and its singular are implicit and count as claimed.
        claimed.add(canonical)
        if singular != canonical:
            claimed.add(singular)

    # Pinned first — they cannot be overridden.
    for alias, canonical in pinned.items():
        if alias in claimed and alias not in entries[canonical].syntactic_aliases:
            # Claimed by another canonical's singular — user conflict.
            # Pinned still wins for the alias slot, but we allow it.
            pass
        entry = entries[canonical]
        if alias not in entry.syntactic_aliases:
            entry.syntactic_aliases.append(alias)
        entry.pinned_by_user = True
        entry.source = "user_config"
        claimed.add(alias)

    # LLM assignments, skipping anything already claimed.
    for canonical, words in llm_aliases.items():
        if canonical not in entries:
            continue
        for word in words:
            if word in claimed:
                continue
            entry = entries[canonical]
            entry.syntactic_aliases.append(word)
            if entry.source == "user_config":
                entry.source = "mixed"
            claimed.add(word)

    # Everything left over is unmatched.
    unmatched = sorted(set(vocabulary) - claimed)

    lookup = _build_lookup(entries)

    return AliasMap(
        entries=entries,
        lookup=lookup,
        unmatched_vocabulary=unmatched,
        cache_key=cache_key,
        cache_hit=False,
    )


def _build_lookup(entries: dict[str, ResourceAliasEntry]) -> dict[str, str]:
    """Flatten entries into a single word → canonical dict.

    O(1) membership checks for the role classifier. Includes the
    canonical plural, the singular, and every syntactic alias.
    """
    lookup: dict[str, str] = {}
    for canonical, entry in entries.items():
        lookup[canonical] = canonical
        lookup[entry.singular] = canonical
        for alias in entry.syntactic_aliases:
            lookup[alias] = canonical
    return lookup


def _load_prompt_template() -> str:
    """Read the versioned prompt template from disk.

    Kept as a separate file so it can be edited and reviewed without
    touching Python code. Bump ``PROMPT_VERSION`` whenever the content
    changes in a way that could change outputs.
    """
    return load_prompt_template("syntactic_aliases.md")
