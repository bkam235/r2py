"""Tests for the static structural audit (r2py/harness/audit.py)."""
from __future__ import annotations

from unittest.mock import patch

import pytest

from r2py.harness.audit import (
    AuditFinding,
    CATEGORIES,
    _parse_response,
    format_audit_for_agent,
    static_audit,
)


# ---------------------------------------------------------------------------
# _parse_response
# ---------------------------------------------------------------------------

class TestParseResponse:
    def test_valid_findings(self):
        raw = '{"findings": [{"category": "control_flow", "entity_id": "e1", "severity": "high", "description": "missing branch"}]}'
        result = _parse_response(raw)
        assert len(result) == 1
        assert result[0].category == "control_flow"
        assert result[0].entity_id == "e1"
        assert result[0].severity == "high"
        assert result[0].description == "missing branch"

    def test_empty_findings(self):
        assert _parse_response('{"findings": []}') == []

    def test_malformed_json(self):
        assert _parse_response("not json at all") == []

    def test_markdown_wrapped(self):
        raw = '```json\n{"findings": [{"category": "error_handling", "entity_id": "", "severity": "medium", "description": "no try/except"}]}\n```'
        result = _parse_response(raw)
        assert len(result) == 1
        assert result[0].category == "error_handling"

    def test_invalid_category_skipped(self):
        raw = '{"findings": [{"category": "bogus", "entity_id": "", "severity": "high", "description": "x"}, {"category": "side_effects", "entity_id": "", "severity": "low", "description": "missing print"}]}'
        result = _parse_response(raw)
        assert len(result) == 1
        assert result[0].category == "side_effects"

    def test_missing_description_skipped(self):
        raw = '{"findings": [{"category": "control_flow", "entity_id": "", "severity": "high", "description": ""}, {"category": "control_flow", "entity_id": "", "severity": "high", "description": "real issue"}]}'
        result = _parse_response(raw)
        assert len(result) == 1
        assert result[0].description == "real issue"

    def test_invalid_severity_defaults_to_medium(self):
        raw = '{"findings": [{"category": "library_mapping", "entity_id": "", "severity": "critical", "description": "bad pkg"}]}'
        result = _parse_response(raw)
        assert result[0].severity == "medium"

    def test_missing_findings_key(self):
        assert _parse_response('{"issues": []}') == []

    def test_non_dict_items_skipped(self):
        raw = '{"findings": ["not a dict", {"category": "control_flow", "entity_id": "", "severity": "high", "description": "ok"}]}'
        result = _parse_response(raw)
        assert len(result) == 1

    def test_max_10_findings(self):
        items = [
            {"category": "control_flow", "entity_id": "", "severity": "low", "description": f"issue {i}"}
            for i in range(15)
        ]
        import json
        raw = json.dumps({"findings": items})
        result = _parse_response(raw)
        assert len(result) == 10


# ---------------------------------------------------------------------------
# format_audit_for_agent
# ---------------------------------------------------------------------------

class TestFormatAuditForAgent:
    def test_empty_list(self):
        assert format_audit_for_agent([]) == ""

    def test_single_finding(self):
        f = AuditFinding("control_flow", "e1", "high", "missing branch")
        text = format_audit_for_agent([f])
        assert "1 issue" in text
        assert "[HIGH]" in text
        assert "e1" in text
        assert "control_flow" in text
        assert "missing branch" in text

    def test_multiple_findings_sorted_by_severity(self):
        findings = [
            AuditFinding("side_effects", "", "low", "minor"),
            AuditFinding("control_flow", "e1", "high", "critical"),
            AuditFinding("error_handling", "e2", "medium", "moderate"),
        ]
        text = format_audit_for_agent(findings)
        assert "3 issue" in text
        lines = text.split("\n")
        severity_lines = [l for l in lines if l.strip().startswith("[")]
        assert "[HIGH]" in severity_lines[0]
        assert "[MEDIUM]" in severity_lines[1]
        assert "[LOW]" in severity_lines[2]

    def test_empty_entity_id_omitted(self):
        f = AuditFinding("control_flow", "", "high", "desc")
        text = format_audit_for_agent([f])
        assert "[HIGH] (control_flow)" in text


# ---------------------------------------------------------------------------
# static_audit (mocked LLM)
# ---------------------------------------------------------------------------

class TestStaticAudit:
    @patch("r2py.harness.audit._llm.call")
    def test_llm_failure_returns_empty(self, mock_call):
        mock_call.side_effect = RuntimeError("API down")
        result = static_audit("x <- 1", "x = 1")
        assert result == []

    @patch("r2py.harness.audit._llm.call")
    def test_returns_parsed_findings(self, mock_call):
        mock_call.return_value = '{"findings": [{"category": "return_structure", "entity_id": "e3", "severity": "medium", "description": "dict keys wrong"}]}'
        result = static_audit("x <- list(a=1)", "x = {'b': 1}")
        assert len(result) == 1
        assert result[0].category == "return_structure"
        assert result[0].entity_id == "e3"

    @patch("r2py.harness.audit._llm.call")
    def test_no_findings(self, mock_call):
        mock_call.return_value = '{"findings": []}'
        result = static_audit("x <- 1", "x = 1")
        assert result == []
