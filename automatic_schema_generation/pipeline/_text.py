"""Identifier normalization shared across config and pipeline stages.

Multi-word identifiers appear in four common surface forms in
OpenAPI specs: ``PascalCase``, ``camelCase``, ``kebab-case``, and
``snake_case``. Users writing aliases in ``app_config.yaml`` may
also reach for any of those forms depending on where they copied
the word from. To make matching work regardless of the surface,
every identifier-like string goes through ``normalize_identifier``
before being stored or compared. The canonical form is
``snake_case`` — lowercase letters, digits, underscores.

Rule of thumb for every caller:

  * If the thing is user-written or spec-derived and represents a
    multi-word identifier, run it through ``normalize_identifier``.
    Aliases, schema names, URL segments, parameter names all
    qualify.
  * If the thing is a top-level ``resources:`` key, validate it
    against ``IDENTIFIER_PATTERN`` and reject mismatches at load
    time. We don't silently normalize canonical keys because they
    become table names in the generated service and the user's
    yaml should match the generated code byte-for-byte.
  * If the thing is prose (descriptions, summaries), do NOT run
    it through ``normalize_identifier`` — the function is tuned
    for identifier shapes, not sentences.
"""

from __future__ import annotations

import re


# Canonical shape for snake_case identifiers — starts with a
# lowercase letter, then lowercase letters / digits / underscores.
# Used both to validate ``resources:`` keys in config.py and (later)
# to validate tokens produced by the pipeline's tokenizer.
IDENTIFIER_PATTERN: re.Pattern[str] = re.compile(r"[a-z][a-z0-9_]*")


# Internal regex fragments used by ``normalize_identifier``.
#
# _CAMEL_BOUNDARY_1 matches a capital letter that follows a
# lowercase letter or digit — the ``r→R`` transition in
# ``userRequest`` or ``a1Bc`` — and inserts an underscore before
# it.
#
# _CAMEL_BOUNDARY_2 handles the tail of an all-caps acronym
# followed by a CamelCase word: the ``P→Pa`` in ``APIPage`` needs a
# boundary inserted so we end up with ``api_page`` rather than
# ``a_p_i_page``. The pattern matches ``[A-Z][a-z]`` preceded by
# another ``[A-Z]``.
#
# _COLLAPSE_UNDERSCORES flattens runs of underscores introduced by
# any of the above steps plus the raw input (``pull--request`` has
# a double hyphen that becomes a double underscore after the
# ``replace``).
_CAMEL_BOUNDARY_1: re.Pattern[str] = re.compile(r"(?<=[a-z0-9])([A-Z])")
_CAMEL_BOUNDARY_2: re.Pattern[str] = re.compile(r"(?<=[A-Z])([A-Z][a-z])")
_COLLAPSE_UNDERSCORES: re.Pattern[str] = re.compile(r"_+")


def normalize_identifier(text: str) -> str:
    """Normalize an identifier-like string to ``snake_case``.

    Handles every common multi-word form found in OpenAPI specs
    and user configs:

      * ``PullRequest``   → ``pull_request``  (PascalCase)
      * ``pullRequest``   → ``pull_request``  (camelCase)
      * ``pull-request``  → ``pull_request``  (kebab-case)
      * ``pull_request``  → ``pull_request``  (already snake_case — no-op)
      * ``APIToken``      → ``api_token``     (acronym prefix)
      * ``simple-user``   → ``simple_user``
      * ``HTTPSProxy``    → ``https_proxy``
      * ``pull--request`` → ``pull_request``  (collapses double separators)

    The function is deliberately narrow: it does NOT touch
    whitespace, so running prose through it is safe in the sense
    that words stay separated (a description like ``"The user
    request"`` becomes ``"the user request"``), but it also means
    whitespace-separated tokens in identifier context like
    ``"Pull Request"`` are NOT collapsed to ``pull_request``. The
    intent is "normalize identifier shape," not "tokenize arbitrary
    text." Callers that need to handle user-written spaces should
    reject them at validation time and ask for snake/camel/kebab.
    """
    # 1. Insert underscore before capital letters that follow
    #    lowercase/digit — handles the common camelCase / PascalCase
    #    boundary (``pullRequest`` → ``pull_Request``).
    text = _CAMEL_BOUNDARY_1.sub(r"_\1", text)
    # 2. Insert underscore before [A-Z][a-z] that follows [A-Z] —
    #    handles the acronym-to-word transition (``APIPage`` →
    #    ``API_Page`` which becomes ``api_page`` after step 4).
    text = _CAMEL_BOUNDARY_2.sub(r"_\1", text)
    # 3. Hyphens are an explicit word separator in kebab-case.
    text = text.replace("-", "_")
    # 4. Collapse any runs of underscores (from repeated separators
    #    in the input or from the regex work above) into singles.
    text = _COLLAPSE_UNDERSCORES.sub("_", text)
    # 5. Trim leading/trailing underscores and lowercase the whole
    #    thing. Lowercasing here is safe because the boundary
    #    insertion already happened — if we lowercased first we'd
    #    lose the case information the boundary regex needs.
    return text.strip("_").lower()
