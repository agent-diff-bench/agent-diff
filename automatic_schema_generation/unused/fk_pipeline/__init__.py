"""FK pipeline v2 — clean re-implementation.

Step 1: Resource ↔ endpoint bidirectional bucketing, with LLM-driven
syntactic alias expansion up front. Later steps (FK candidate extraction,
cardinality inference, semantic role resolution) build on top of the
artifacts this step produces.

Strictly additive to the existing ``pipeline/`` directory — nothing in
this package mutates or depends on the old implementation stages beyond
re-using a couple of pure primitives (``singularize``, ``resolve_ref``).
"""

from __future__ import annotations

import sys
from pathlib import Path

# One-time sys.path bootstrap so sibling modules can ``from pipeline.naming
# import singularize`` at module-top level. Previously every submodule
# did this dance itself — having it here once keeps the imports at the
# top of each file tidy.
_THIS_DIR = Path(__file__).resolve().parent
_PARENT_DIR = _THIS_DIR.parent
if str(_PARENT_DIR) not in sys.path:
    sys.path.insert(0, str(_PARENT_DIR))


def load_prompt_template(filename: str) -> str:
    """Read a prompt template from the ``prompts/`` directory.

    Shared by ``vocabulary.py`` and ``resolution.py``. Bumping
    ``PROMPT_VERSION`` in the caller is still how cache invalidation
    happens when a prompt changes — this helper only handles the read.
    """
    return (_THIS_DIR / "prompts" / filename).read_text()
