"""Logique métier Snippet Manager (stockage en mémoire pour le squelette ; DB plus tard)."""

from typing import Optional
import uuid

# Stockage en mémoire pour démarrer (remplacer par SQLite + embeddings plus tard)
_snippets: dict[str, dict] = {}


class SnippetService:
    """Service de gestion des snippets."""

    async def save(self, title: str, content: str, tags: list[str]) -> str:
        """Enregistre un snippet et retourne un message (pour MCP)."""
        sid = str(uuid.uuid4())
        _snippets[sid] = {
            "id": sid,
            "title": title,
            "content": content,
            "tags": tags,
        }
        return f"Snippet enregistré : id={sid}, title={title!r}"

    async def save_and_return_id(self, title: str, content: str, tags: list[str]) -> str:
        """Enregistre un snippet et retourne son id (pour l'API REST)."""
        sid = str(uuid.uuid4())
        _snippets[sid] = {
            "id": sid,
            "title": title,
            "content": content,
            "tags": tags,
        }
        return sid

    async def search(self, query: str, limit: int = 10) -> str:
        """Recherche par mots-clés dans titre, contenu et tags (sémantique à venir)."""
        q = query.lower().strip()
        results = []
        for s in _snippets.values():
            if not q or (
                q in s["title"].lower()
                or q in s["content"].lower()
                or any(q in t.lower() for t in s["tags"])
            ):
                results.append(s)
            if len(results) >= limit:
                break
        if not results:
            return "Aucun snippet trouvé."
        lines = [
            f"- [{r['title']}] id={r['id']} tags={r['tags']}\n  {r['content'][:200]}..."
            for r in results
        ]
        return "\n".join(lines)

    async def get(self, snippet_id: str) -> Optional[dict]:
        """Récupère un snippet par id."""
        return _snippets.get(snippet_id)

    async def delete(self, snippet_id: str) -> bool:
        """Supprime un snippet."""
        if snippet_id in _snippets:
            del _snippets[snippet_id]
            return True
        return False


snippet_service = SnippetService()
