"""Tests du Code Analyzer."""

import pytest
from dev_assist_mcp.modules.code_analyzer.service import analyze_code


@pytest.mark.asyncio
async def test_analyze_code_detects_todo():
    """L'analyse signale la présence de TODO."""
    result = await analyze_code("def foo():\n    # TODO: implement\n    pass", "python")
    assert "TODO" in result
