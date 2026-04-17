"""FK candidate data types.

A *candidate* is a field (or parameter) that the walker thinks MIGHT
be a foreign key to another resource. The walker's job is to cast a
wide net — record everything that could possibly be a FK — so that
downstream LLM disambiguation has a complete list to work from. Zero
false negatives at this stage, false positives are fine.

A candidate is either:

  * **Linked** — the walker resolved the target resource via the
    syntactic alias map (``alias_map.lookup``). The edge is strong
    and its cardinality is inferable without an LLM:

      - scalar ``_id``          → ``ONE_TO_MANY`` (parent points at one)
      - nested ``$ref`` object  → ``ONE_TO_MANY``
      - array of ``$ref``       → ``MANY_TO_MANY``
      - inline object w/ pk     → ``ONE_TO_MANY``
      - path/query param        → ``ONE_TO_MANY``

  * **Unresolved** — the walker saw a FK-shaped field but couldn't
    match it to any known resource via the alias map. The field name
    is kept verbatim so the LLM step can decide what it points at
    (``assignee`` / ``reviewer`` / ``closed_by`` / etc. all land here).

No role-word tables, no heuristic semantic mapping. If the alias map
doesn't say what it is, it's unresolved and the LLM handles it.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


# Stable key used to match a candidate back to a cached LLM decision.
# Must stay in sync with ``FkResolution.signature`` in resolution.py —
# the two types share this shape deliberately.
CandidateSignature = tuple[str, tuple[str, ...], str, str]


class CandidateType(str, Enum):
    """What shape the candidate has in the source schema/endpoint.

    The shape determines the inferred cardinality when the target
    resolves, and it's recorded regardless of whether the target
    resolves — downstream code might render unresolved candidates
    differently based on their type.
    """

    SCALAR_ID = "SCALAR_ID"             # e.g. project_id: integer
    NESTED_REF = "NESTED_REF"           # field: {$ref: X}
    ARRAY_OF_REFS = "ARRAY_OF_REFS"     # field: [{$ref: X}]
    INLINE_OBJECT = "INLINE_OBJECT"     # field: {type: object, properties: {id: ...}}
    PATH_PARAM_FK = "PATH_PARAM_FK"     # {foo_id} in an endpoint path
    QUERY_PARAM_FK = "QUERY_PARAM_FK"   # ?foo_id= on an endpoint


class ResolutionReason(str, Enum):
    """How the walker matched (or failed to match) the target.

    Linked reasons mirror ``bucketing._resolve_param_to_resource``'s
    lookup chain: direct word match, then strip fk_suffix, then strip
    a qualifier prefix as well. ``SCHEMA_REF`` is the fourth linked
    reason, used when the target was resolved via a component schema
    name rather than a field name. ``UNRESOLVED`` covers everything
    the LLM has to handle.
    """

    DIRECT = "DIRECT"
    SUFFIX_STRIP = "SUFFIX_STRIP"
    QUALIFIER_STRIP = "QUALIFIER_STRIP"
    SCHEMA_REF = "SCHEMA_REF"
    UNRESOLVED = "UNRESOLVED"


class Cardinality(str, Enum):
    """Inferred cardinality of a linked candidate.

    Intentionally coarse: the walker is a proposal engine, not a
    semantic classifier. ``None`` on a candidate means "we don't know
    and shouldn't guess" — that's the shape for unresolved candidates.
    """

    ONE_TO_MANY = "ONE_TO_MANY"
    MANY_TO_MANY = "MANY_TO_MANY"


class Confidence(str, Enum):
    """Walker's confidence that this is actually a FK.

    * ``STRONG`` — the candidate resolved to a known resource via the
      alias lookup, or it's the exact ``{foo_id}`` pattern with a
      resolved stem. Safe to use without LLM review.
    * ``WEAK`` — the candidate looks FK-shaped but didn't resolve, or
      the target is the resource itself (self-reference), or some
      other condition the downstream step should verify.
    """

    STRONG = "STRONG"
    WEAK = "WEAK"


class LlmDecision(str, Enum):
    """LLM's verdict on an unresolved (or cardinality-only) candidate.

    Set by step 3 (``resolution.py``) on candidates the walker couldn't
    fully decide. Absent on mechanically-resolved candidates.

    * ``LINKED`` — LLM picked a canonical target. The candidate is
      upgraded: ``target_resource`` is set, ``inferred_cardinality``
      is set, ``needs_llm`` flips to False.
    * ``REJECTED`` — LLM decided the field is not a FK at all. The
      candidate is kept for audit but should be displayed in a
      separate ``rejected`` bucket by the writer.
    * ``CARDINALITY_ONLY`` — the walker had already inferred the
      target but not the cardinality; the LLM only filled in
      ``inferred_cardinality``. (Not currently produced by the
      walker — all step-2 linked candidates ship with a cardinality —
      but kept in the taxonomy for forward compatibility.)
    """

    LINKED = "LINKED"
    REJECTED = "REJECTED"
    CARDINALITY_ONLY = "CARDINALITY_ONLY"


@dataclass
class FkCandidate:
    """One proposed FK edge, linked or unresolved.

    ``source_resource`` is the canonical plural of the resource whose
    shape contains the candidate field. ``source_path`` is a tuple
    describing where inside that shape the field lives — e.g.
    ``("Issue", "assignee")`` or ``("GET /repos/{owner}/{repo}/pulls",
    "query.base")`` for endpoint-lifted candidates.

    ``raw_target`` is the field name (or stem, after suffix strip)
    used for the alias lookup. Kept verbatim so the LLM step can see
    the original word — crucial for unresolved candidates, because
    the raw word IS the classification input.

    ``target_resource`` is populated only on linked candidates. On
    unresolved candidates it is ``None`` and ``needs_llm`` is True.

    ``evidence`` is a short human-readable string naming what the
    walker saw. It's the first thing an operator reads when a
    candidate looks wrong.
    """

    source_resource: str
    source_path: tuple[str, ...]
    raw_target: str
    candidate_type: CandidateType
    resolution_reason: ResolutionReason
    target_resource: str | None
    inferred_cardinality: Cardinality | None
    confidence: Confidence
    needs_llm: bool
    evidence: str

    # --- Step 3 (LLM resolution) annotations. Default to "not touched
    # by the LLM" so step-1/step-2-only runs serialize unchanged.
    #
    # ``llm_inferred`` flips to True when ``resolution.py`` has taken
    # a decision on this candidate, regardless of whether the decision
    # was "linked" or "rejected". The writer uses this to mark which
    # fields in the artifact are LLM-derived vs walker-derived.
    llm_inferred: bool = False
    llm_decision: LlmDecision | None = None
    llm_reason: str | None = None
    llm_model: str | None = None

    @property
    def signature(self) -> CandidateSignature:
        """Stable identity for cache lookup and extractor sort order."""
        return (
            self.source_resource,
            tuple(self.source_path),
            self.raw_target,
            self.candidate_type.value,
        )

    def to_dict(self) -> dict[str, object]:
        """Stable JSON-serializable view for the writer.

        LLM annotation fields are only emitted when ``llm_inferred``
        is True — this keeps the artifact small and visually clean for
        the common case (most candidates are mechanically resolved).
        """
        out: dict[str, object] = {
            "source_resource": self.source_resource,
            "source_path": list(self.source_path),
            "raw_target": self.raw_target,
            "target_resource": self.target_resource,
            "candidate_type": self.candidate_type.value,
            "resolution_reason": self.resolution_reason.value,
            "inferred_cardinality": (
                self.inferred_cardinality.value
                if self.inferred_cardinality is not None
                else None
            ),
            "confidence": self.confidence.value,
            "needs_llm": self.needs_llm,
            "evidence": self.evidence,
        }
        if self.llm_inferred:
            out["llm_inferred"] = True
            out["llm_decision"] = (
                self.llm_decision.value if self.llm_decision is not None else None
            )
            out["llm_reason"] = self.llm_reason
            out["llm_model"] = self.llm_model
        return out
