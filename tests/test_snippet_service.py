"""Tests du Snippet Manager."""

import pytest
from dev_assist_mcp.modules.snippet_manager.service import snippet_service


@pytest.mark.asyncio
async def test_save_and_search_snippet():
    """Enregistrement et recherche d'un snippet."""
    await snippet_service.save("Test snippet", "print('hello')", ["python", "test"])
    result = await snippet_service.search("python", limit=5)
    assert "Test snippet" in result
    assert "print" in result
