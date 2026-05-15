from __future__ import annotations

from typing import Any, Literal, Mapping, Sequence
from datetime import date, datetime
import json
import re
import logging

logger = logging.getLogger(__name__)

Kind = Literal["added", "removed", "changed"]


def _normalize_for_comparison(value: Any) -> Any:
    """Normalize values for comparison - recursively convert date/datetime to ISO string."""
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, dict):
        return {k: _normalize_for_comparison(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        normalized = [_normalize_for_comparison(item) for item in value]
        return type(value)(normalized)
    if isinstance(value, set):
        return {_normalize_for_comparison(item) for item in value}
    return value


Bucket = Literal["inserts", "deletes", "updates"]


def _get_ignore_sets(
    spec: Mapping[str, Any], entity: str, assertion_ignore: Sequence[str] | None
) -> set[str]:
    ignores = set((spec.get("ignore_fields", {}).get("global") or []))
    entity_ignores = spec.get("ignore_fields", {}).get(entity) or []
    ignores.update(entity_ignores)
    if assertion_ignore:
        ignores.update(assertion_ignore)
    return ignores


def _get(row: Mapping[str, Any], key: str) -> Any:
    cur: Any = row
    for part in key.split("."):
        if not isinstance(cur, Mapping) or part not in cur:
            return None
        cur = cur[part]
    return cur


def _matches_predicate(value: Any, pred: Mapping[str, Any]) -> bool:
    if not pred:
        return True
    if len(pred) != 1:
        return all(_matches_predicate(value, {op: v}) for op, v in pred.items())
    op, expected = next(iter(pred.items()))

    # Normalize date/datetime values to ISO strings for comparison
    value = _normalize_for_comparison(value)
    expected = _normalize_for_comparison(expected)

    if op == "eq":
        return value == expected
    if op in ("ne", "not_eq"):
        return value != expected
    if op == "in":
        try:
            return value in expected
        except TypeError:
            return False
    if op == "not_in":
        try:
            return value not in expected
        except TypeError:
            return False
    if op == "contains":
        # Handle JSONB (dict/list) by converting to JSON string (compact, no spaces)
        if isinstance(value, (dict, list)):
            value = json.dumps(value, separators=(",", ":"))
        return (
            isinstance(value, str) and isinstance(expected, str) and expected in value
        )
    if op == "not_contains":
        if isinstance(value, (dict, list)):
            value = json.dumps(value, separators=(",", ":"))
        return (
            isinstance(value, str)
            and isinstance(expected, str)
            and expected not in value
        )
    if op == "i_contains":
        if isinstance(value, (dict, list)):
            value = json.dumps(value, separators=(",", ":"))
        return (
            isinstance(value, str)
            and isinstance(expected, str)
            and expected.lower() in value.lower()
        )
    if op == "starts_with":
        return (
            isinstance(value, str)
            and isinstance(expected, str)
            and value.startswith(expected)
        )
    if op == "ends_with":
        return (
            isinstance(value, str)
            and isinstance(expected, str)
            and value.endswith(expected)
        )
    if op == "i_starts_with":
        return (
            isinstance(value, str)
            and isinstance(expected, str)
            and value.lower().startswith(expected.lower())
        )
    if op == "i_ends_with":
        return (
            isinstance(value, str)
            and isinstance(expected, str)
            and value.lower().endswith(expected.lower())
        )
    if op == "regex":
        try:
            return isinstance(value, str) and re.search(expected, value) is not None
        except re.error:
            return False
    if op == "gt":
        try:
            return value > expected
        except Exception:
            return False
    if op == "gte":
        try:
            return value >= expected
        except Exception:
            return False
    if op == "lt":
        try:
            return value < expected
        except Exception:
            return False
    if op == "lte":
        try:
            return value <= expected
        except Exception:
            return False
    if op == "exists":
        present = value is not None
        return bool(expected) is present
    if op == "has_any":
        return isinstance(value, Sequence) and any(
            item in value for item in (expected or [])
        )
    if op == "has_all":
        return isinstance(value, Sequence) and all(
            item in value for item in (expected or [])
        )
    return False


def _row_matches_where(row: Mapping[str, Any], where: Mapping[str, Any]) -> bool:
    for key, pred in where.items():
        if not _predicate_matches(_get(row, key), pred):
            return False
    return True


def _truncate_text(value: str, max_len: int = 120) -> str:
    if len(value) <= max_len:
        return value
    return value[: max_len - 3] + "..."


def _format_value(value: Any) -> str:
    value = _normalize_for_comparison(value)
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, str):
        return repr(_truncate_text(value))
    try:
        return _truncate_text(
            json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)
        )
    except TypeError:
        return _truncate_text(repr(value))


def _predicate_items(pred: Any) -> list[tuple[str, Any]]:
    if isinstance(pred, Mapping):
        return list(pred.items())
    return [("eq", pred)]


def _predicate_matches(value: Any, pred: Any) -> bool:
    if isinstance(pred, Mapping):
        return _matches_predicate(value, pred)
    return _matches_predicate(value, {"eq": pred})


def _format_predicate(pred: Any) -> str:
    parts: list[str] = []
    for op, expected in _predicate_items(pred):
        if op == "eq":
            parts.append(_format_value(expected))
        elif op == "exists":
            parts.append("present" if expected else "absent")
        else:
            parts.append(f"{op} {_format_value(expected)}")
    return " and ".join(parts)


def _format_field_condition(field: str, pred: Any) -> str:
    items = _predicate_items(pred)
    if len(items) != 1:
        return f"{field} {_format_predicate(pred)}"

    op, expected = items[0]
    if op == "eq":
        return f"{field}={_format_value(expected)}"
    if op == "exists":
        return f"{field} is {'present' if expected else 'absent'}"
    return f"{field} {op} {_format_value(expected)}"


def _format_field_mismatch(field: str, actual: Any, pred: Any) -> str:
    return f"{field}={_format_value(actual)} (expected {_format_predicate(pred)})"


def _where_match_details(
    row: Mapping[str, Any], where: Mapping[str, Any]
) -> tuple[list[str], list[str]]:
    matched: list[str] = []
    mismatched: list[str] = []
    for field, pred in where.items():
        actual = _get(row, field)
        if _predicate_matches(actual, pred):
            matched.append(_format_field_condition(field, pred))
        else:
            mismatched.append(_format_field_mismatch(field, actual, pred))
    return matched, mismatched


_ROW_ID_FIELDS = (
    "id",
    "identifier",
    "title",
    "name",
    "summary",
    "message_id",
    "channel_id",
    "calendar_id",
    "issue_id",
    "user_id",
    "email",
)


def _format_row_identity(row: Mapping[str, Any]) -> str:
    parts: list[str] = []
    for field in _ROW_ID_FIELDS:
        if field in row and row.get(field) is not None:
            parts.append(f"{field}={_format_value(row.get(field))}")
        if len(parts) >= 3:
            break

    if not parts:
        for field, value in row.items():
            if field == "__table__" or field.startswith("_"):
                continue
            parts.append(f"{field}={_format_value(value)}")
            if len(parts) >= 3:
                break

    if not parts:
        return "row"
    return "row " + ", ".join(parts)


def _format_where_mismatch_rows(
    rows: Sequence[Mapping[str, Any]], where: Mapping[str, Any]
) -> str:
    summaries: list[str] = []
    for row in rows:
        matched, mismatched = _where_match_details(row, where)
        identity = _format_row_identity(row)
        if matched and mismatched:
            summaries.append(
                f"{identity}: matched {', '.join(matched)}, but "
                f"{', '.join(mismatched)}"
            )
        elif mismatched:
            summaries.append(f"{identity}: {', '.join(mismatched)}")
        else:
            summaries.append(f"{identity}: matched all where predicates")
    return "; ".join(summaries)


def _format_matching_rows(rows: Sequence[Mapping[str, Any]]) -> str:
    return "; ".join(_format_row_identity(row) for row in rows)


def _best_where_details_for_update(
    update: Mapping[str, Any], where: Mapping[str, Any]
) -> tuple[str, Mapping[str, Any], list[str], list[str]]:
    before = update.get("before", {}) or {}
    after = update.get("after", {}) or {}
    before_matched, before_mismatched = _where_match_details(before, where)
    after_matched, after_mismatched = _where_match_details(after, where)
    if len(after_matched) >= len(before_matched):
        return "after", after, after_matched, after_mismatched
    return "before", before, before_matched, before_mismatched


def _format_update_where_mismatch_rows(
    updates: Sequence[Mapping[str, Any]], where: Mapping[str, Any]
) -> str:
    summaries: list[str] = []
    for update in updates:
        side, row, matched, mismatched = _best_where_details_for_update(update, where)
        identity = _format_row_identity(row or update.get("before", {}) or {})
        if matched and mismatched:
            summaries.append(
                f"{identity} ({side}): matched {', '.join(matched)}, but "
                f"{', '.join(mismatched)}"
            )
        elif mismatched:
            summaries.append(f"{identity} ({side}): {', '.join(mismatched)}")
        else:
            summaries.append(f"{identity} ({side}): matched all where predicates")
    return "; ".join(summaries)


def _format_change_mismatch_rows(
    mismatches: Sequence[tuple[Mapping[str, Any], list[str]]],
) -> str:
    summaries: list[str] = []
    for update, reasons in mismatches:
        after = update.get("after", {}) or {}
        before = update.get("before", {}) or {}
        identity = _format_row_identity(after or before)
        summaries.append(f"{identity}: {', '.join(reasons)}")
    return "; ".join(summaries)


def _change_expectation_failures(
    before: Mapping[str, Any],
    after: Mapping[str, Any],
    changed: set[str],
    expected_changes: Mapping[str, Any],
) -> list[str]:
    failures: list[str] = []
    for field, spec_chg in expected_changes.items():
        if not isinstance(spec_chg, Mapping):
            spec_chg = {"to": spec_chg}
        if field not in changed:
            failures.append(
                f"{field} did not change "
                f"(before={_format_value(before.get(field))}, "
                f"after={_format_value(after.get(field))})"
            )
            continue

        pred_from = spec_chg.get("from")
        pred_to = spec_chg.get("to")
        if pred_from is not None and not _predicate_matches(before.get(field), pred_from):
            failures.append(
                f"{field} before={_format_value(before.get(field))} "
                f"(expected from {_format_predicate(pred_from)})"
            )
        if pred_to is not None and not _predicate_matches(after.get(field), pred_to):
            failures.append(
                f"{field} after={_format_value(after.get(field))} "
                f"(expected to {_format_predicate(pred_to)})"
            )
    return failures


def _changed_keys(
    before: Mapping[str, Any], after: Mapping[str, Any], ignores: set[str]
) -> set[str]:
    keys = set(before.keys()) | set(after.keys())
    return {k for k in keys if k not in ignores and before.get(k) != after.get(k)}


class AssertionEngine:
    def __init__(self, compiled_spec: Mapping[str, Any]):
        self.spec = compiled_spec
        self.strict = bool(compiled_spec.get("strict", True))

    def evaluate(self, diff: Mapping[str, Sequence[Mapping[str, Any]]]) -> dict:
        failures: list[str] = []
        failed_indexes: set[int] = set()

        assertions_list = list(self.spec.get("assertions", []))
        for idx, a in enumerate(assertions_list, start=1):
            diff_type: Kind = a["diff_type"]
            entity = a["entity"]
            where = a.get("where", {})
            ignore = _get_ignore_sets(
                self.spec, entity, a.get("ignore_fields", a.get("ignore", []))
            )

            if diff_type == "added":
                rows = [
                    r
                    for r in (diff.get("inserts", []) or [])
                    if r.get("__table__") == entity
                ]
                logger.debug(f"assertion#{idx} added {entity}: found {len(rows)} total inserts, where_keys={list(where.keys())}")
                for r in rows:
                    row_id = r.get("id")
                    match_result = _row_matches_where(r, where)
                    logger.debug(f"assertion#{idx} insert row id={row_id}: match={match_result}")
                matched = [r for r in rows if _row_matches_where(r, where)]
                mismatched = [r for r in rows if not _row_matches_where(r, where)]
                self._check_count(
                    a,
                    len(matched),
                    failures,
                    failed_indexes,
                    idx,
                    entity,
                    diff_type,
                    where=where,
                    matched_rows=matched,
                    mismatched_rows=mismatched,
                    total_rows=len(rows),
                )

            elif diff_type == "removed":
                rows = [
                    r
                    for r in (diff.get("deletes", []) or [])
                    if r.get("__table__") == entity
                ]
                logger.debug(f"assertion#{idx} removed {entity}: found {len(rows)} total deletes, where_keys={list(where.keys())}")
                for r in rows:
                    row_id = r.get("id")
                    match_result = _row_matches_where(r, where)
                    logger.debug(f"assertion#{idx} delete row id={row_id}: match={match_result}")
                matched = [r for r in rows if _row_matches_where(r, where)]
                mismatched = [r for r in rows if not _row_matches_where(r, where)]
                self._check_count(
                    a,
                    len(matched),
                    failures,
                    failed_indexes,
                    idx,
                    entity,
                    diff_type,
                    where=where,
                    matched_rows=matched,
                    mismatched_rows=mismatched,
                    total_rows=len(rows),
                )

            elif diff_type == "changed":
                updates = [
                    r
                    for r in (diff.get("updates", []) or [])
                    if r.get("__table__") == entity
                ]
                logger.debug(f"assertion#{idx} changed {entity}: found {len(updates)} updates, where_keys={list(where.keys())}, ignore_count={len(ignore)}")
                matched_updates = []
                where_mismatches = []
                change_mismatches: list[tuple[Mapping[str, Any], list[str]]] = []
                strict_mismatches: list[tuple[Mapping[str, Any], list[str]]] = []
                for r in updates:
                    before = r.get("before", {})
                    after = r.get("after", {})
                    row_id = after.get("id") or before.get("id")
                    where_match_after = _row_matches_where(after, where)
                    where_match_before = _row_matches_where(before, where)
                    logger.debug(f"assertion#{idx} row {row_id}: where_match_after={where_match_after}, where_match_before={where_match_before}")
                    if not (where_match_after or where_match_before):
                        where_mismatches.append(r)
                        continue
                    changed = _changed_keys(before, after, ignore)
                    expected_changes: dict = a.get("expected_changes", {})
                    expected_keys = set(expected_changes.keys())
                    logger.debug(f"assertion#{idx} row {row_id}: changed_count={len(changed)}, expected_count={len(expected_keys)}")
                    if self.strict:
                        if not changed.issubset(expected_keys):
                            logger.debug(f"assertion#{idx} row {row_id}: STRICT FAIL - extra fields changed")
                            reasons = [
                                f"changed fields {sorted(changed)} not subset of expected {sorted(expected_keys)}"
                            ]
                            strict_mismatches.append((r, reasons))
                            change_mismatches.append((r, reasons))
                            continue
                    mismatch_reasons = _change_expectation_failures(
                        before, after, changed, expected_changes
                    )
                    if not mismatch_reasons:
                        logger.debug(f"assertion#{idx} row {row_id}: MATCHED")
                        matched_updates.append(r)
                    else:
                        logger.debug(f"assertion#{idx} row {row_id}: NOT MATCHED")
                        change_mismatches.append((r, mismatch_reasons))
                count_ok = self._check_count(
                    a,
                    len(matched_updates),
                    failures,
                    failed_indexes,
                    idx,
                    entity,
                    diff_type,
                    where=where,
                    matched_rows=[
                        (r.get("after", {}) or r.get("before", {}) or {})
                        for r in matched_updates
                    ],
                    total_rows=len(updates),
                    change_mismatches=change_mismatches,
                    where_mismatch_updates=where_mismatches,
                )
                if count_ok and strict_mismatches:
                    self._add_failure(
                        failures,
                        failed_indexes,
                        idx,
                        (
                            f"assertion#{idx} {entity} strict change mismatch: "
                            f"{_format_change_mismatch_rows(strict_mismatches)}"
                        ),
                    )

            else:
                self._add_failure(
                    failures,
                    failed_indexes,
                    idx,
                    f"assertion#{idx} has unknown diff_type: {diff_type}",
                )

        total = len(assertions_list)
        failed_count = len(failed_indexes)
        passed_count = max(total - failed_count, 0)
        percent = float(passed_count) / total * 100.0 if total else 100.0

        return {
            "passed": failed_count == 0,
            "failures": failures,
            "score": {
                "passed": passed_count,
                "total": total,
                "percent": percent,
            },
        }

    @staticmethod
    def _count_matches(expected: Any, actual: int) -> bool:
        if isinstance(expected, int):
            return actual == expected
        if isinstance(expected, Mapping):
            mn = expected.get("min")
            mx = expected.get("max")
            if mn is not None and actual < mn:
                return False
            if mx is not None and actual > mx:
                return False
            return True
        return False

    @staticmethod
    def _count_failure_context(
        *,
        entity: str,
        kind: str,
        actual: int,
        where: Mapping[str, Any] | None = None,
        matched_rows: Sequence[Mapping[str, Any]] | None = None,
        mismatched_rows: Sequence[Mapping[str, Any]] | None = None,
        total_rows: int | None = None,
        change_mismatches: Sequence[tuple[Mapping[str, Any], list[str]]] | None = None,
        where_mismatch_updates: Sequence[Mapping[str, Any]] | None = None,
    ) -> str:
        parts: list[str] = []
        where = where or {}
        matched_rows = matched_rows or []
        mismatched_rows = mismatched_rows or []
        total_rows = total_rows if total_rows is not None else 0

        if total_rows == 0:
            parts.append(f"no {kind} {entity} rows were found")

        if kind in ("added", "removed"):
            if actual > 0 and matched_rows:
                parts.append(
                    "matching rows: " + _format_matching_rows(matched_rows)
                )
            if mismatched_rows:
                parts.append(
                    f"non-matching {entity} rows: "
                    f"{_format_where_mismatch_rows(mismatched_rows, where)}"
                )
        elif kind == "changed":
            if actual > 0 and matched_rows:
                parts.append(
                    "matching updated rows: " + _format_matching_rows(matched_rows)
                )
            if change_mismatches:
                parts.append(
                    "updated rows that matched where but failed expected changes: "
                    + _format_change_mismatch_rows(change_mismatches)
                )
            if where_mismatch_updates:
                parts.append(
                    "updated rows that did not match where: "
                    + _format_update_where_mismatch_rows(where_mismatch_updates, where)
                )

        return "; " + "; ".join(parts) if parts else ""

    def _check_count(
        self,
        a: Mapping[str, Any],
        actual: int,
        failures: list[str],
        failed_indexes: set[int],
        idx: int,
        entity: str,
        kind: str,
        *,
        where: Mapping[str, Any] | None = None,
        matched_rows: Sequence[Mapping[str, Any]] | None = None,
        mismatched_rows: Sequence[Mapping[str, Any]] | None = None,
        total_rows: int | None = None,
        change_mismatches: Sequence[tuple[Mapping[str, Any], list[str]]] | None = None,
        where_mismatch_updates: Sequence[Mapping[str, Any]] | None = None,
    ) -> bool:
        expected = a.get("expected_count")
        expected_too_few = False
        if isinstance(expected, int):
            expected_too_few = actual > expected
        elif isinstance(expected, Mapping) and expected.get("max") is not None:
            expected_too_few = actual > expected["max"]

        context = self._count_failure_context(
            entity=entity,
            kind=kind,
            actual=actual,
            where=where,
            matched_rows=matched_rows if expected_too_few else None,
            mismatched_rows=mismatched_rows,
            total_rows=total_rows,
            change_mismatches=change_mismatches,
            where_mismatch_updates=where_mismatch_updates,
        )
        if expected is None:
            if kind in ("added", "removed", "changed") and actual < 1:
                self._add_failure(
                    failures,
                    failed_indexes,
                    idx,
                    f"assertion#{idx} {entity} expected at least 1 match but got {actual}{context}",
                )
                return False
            return True
        if not self._count_matches(expected, actual):
            self._add_failure(
                failures,
                failed_indexes,
                idx,
                f"assertion#{idx} {entity} expected count {expected} but got {actual}{context}",
            )
            return False
        return True

    @staticmethod
    def _add_failure(
        failures: list[str], failed_indexes: set[int], idx: int, message: str
    ) -> None:
        failed_indexes.add(idx)
        failures.append(message)
