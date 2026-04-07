"""
Slack API conformance tests (docs-golden methodology).

Validates Slack replica response shapes and error semantics against
documented API contracts. Unlike Box/Calendar/Linear, Slack conformance
uses docs-golden tests rather than production API comparison because
live Slack workspace parity is difficult to standardize.

Usage:
    pytest tests/validation/test_slack_conformance.py -v
"""

import pytest

# Re-export under conformance markers — pytest collects TestSlackConformance only
# because the parent class is hidden via __test__ = False below.
from tests.integration.test_slack_api_docs import TestSlackDocsGolden as _Base

# Prevent pytest from collecting the imported base class directly
_Base.__test__ = False


@pytest.mark.conformance
@pytest.mark.replica_only
class TestSlackConformance(_Base):
    """Slack conformance via documented API contract validation."""

    __test__ = True
