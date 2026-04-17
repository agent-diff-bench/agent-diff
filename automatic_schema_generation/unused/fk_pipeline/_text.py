"""Shared text helpers used across the pipeline.

Snake-case conversion, tokenization, and schema-name token sets live
here so every module uses the same rules. Previously each of vocabulary,
extractor, shapes, and bucketing defined its own slightly-different
variant, which was a subtle source of classifier drift.
"""

from __future__ import annotations

import re

from pipeline.naming import singularize


# Camel-/Pascal-case → snake_case insertion points. Two patterns:
# 1. lowercase/digit boundary followed by uppercase  → insert before upper.
# 2. run-of-uppercase followed by Upper+lower         → insert before upper.
_CAMEL_BOUNDARY_RE: re.Pattern[str] = re.compile(
    r"(?<=[a-z0-9])([A-Z])|(?<=[A-Z])([A-Z][a-z])"
)

# A token is a lowercase run starting with a letter.
_TOKEN_RE: re.Pattern[str] = re.compile(r"[a-z][a-z0-9_]*")


def snake_case(name: str) -> str:
    """Convert CamelCase / PascalCase to snake_case.

    ``PullRequestReview`` → ``pull_request_review``. Already-snake names
    are returned unchanged (modulo lowercasing).
    """
    # The regex rewrites both capture groups into ``_\1\2`` — only one
    # of the two groups matches per position, so the other contributes
    # the empty string.
    return _CAMEL_BOUNDARY_RE.sub(r"_\1\2", name).lower()


def tokenize(s: str) -> list[str]:
    """Split a string into lowercase tokens, emitting compound runs AND parts.

    The regex finds maximal ``[a-z][a-z0-9_]*`` runs, which naturally
    strips surrounding non-word characters like braces (``{gist_id}``
    → ``gist_id``) and splits on hyphens (``user-profiles`` →
    ``user``, ``profiles``). For each run that contains an underscore,
    we additionally emit its underscore-separated parts.

    Emitting both the compound and the parts serves two callers with
    opposing needs:

      * Compound aliases like ``pull_request`` or ``user_profile``
        must stay intact in the vocabulary so the LLM can classify
        them as aliases for canonical resources (``pulls``, ``users``).
      * Path-parameter names like ``{gist_id}`` or ``{pull_number}``
        are only useful decomposed — ``gist_id`` would never match a
        canonical resource, but ``gist`` might.

    The stoplist in ``vocabulary.py`` filters common structural parts
    (``id``, ``number``, ``at``, ``by``, ...) out of the final
    candidate set, so the dual-emission doesn't flood the LLM with
    junk.
    """
    out: list[str] = []
    for run in _TOKEN_RE.findall(s.lower()):
        out.append(run)
        if "_" in run:
            # Split parts must still start with a letter, same as the
            # top-level regex — otherwise trailing digits (``name_0``
            # → ``0``) or leading ones (``_1foo`` → ``1foo``) leak in.
            out.extend(
                part for part in run.split("_")
                if part and part[0].isalpha()
            )
    return out


def name_tokens(name: str) -> set[str]:
    """Return the set of tokens AND their singular forms for a schema name.

    Splits on non-alphanumerics AND on CamelCase boundaries, then emits
    every piece in singular + plural form. Used by ``shapes`` to decide
    whether a component schema name carries the resource word.

    ``pull-request`` → ``{pull, request}``
    ``PullRequestReview`` → ``{pull, request, review}``
    ``simple-user`` → ``{simple, user}``
    """
    parts: set[str] = set()
    for chunk in re.split(r"[^A-Za-z0-9]+", name):
        if not chunk:
            continue
        for token in snake_case(chunk).split("_"):
            if not token:
                continue
            parts.add(token)
            parts.add(singularize(token))
    return parts
