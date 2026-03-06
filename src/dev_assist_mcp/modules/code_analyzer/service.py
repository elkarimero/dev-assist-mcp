"""Logique d'analyse de code (squelette : heuristiques simples ; LLM/outils externes plus tard)."""

from typing import Optional


async def analyze_code(code: str, language: str = "python") -> str:
    """
    Analyse le code et retourne complexité, bugs potentiels, suggestions.
    Squelette : analyse basique ; à enrichir avec ast, radon, ou appels LLM.
    """
    lines = code.strip().split("\n")
    line_count = len(lines)
    # Heuristiques minimales pour le squelette
    issues = []
    if line_count > 100:
        issues.append(f"- Fichier long ({line_count} lignes) : envisager de découper en modules.")
    if "except:" in code or "except Exception:" in code:
        issues.append("- except trop large : capturer des exceptions plus spécifiques.")
    if "print(" in code and language == "python":
        issues.append("- Utilisation de print : envisager logging pour la prod.")
    if "TODO" in code or "FIXME" in code:
        issues.append("- Présence de TODO/FIXME : à traiter.")
    if not issues:
        issues.append("- Aucun point d'attention détecté par l'analyse basique.")
    summary = [
        f"# Analyse du code ({language})",
        f"Lignes : {line_count}",
        "",
        "## Points d'attention",
        *issues,
        "",
        "Enrichir ce module avec ast/radon (complexité cyclomatique) ou un LLM pour des suggestions détaillées.",
    ]
    return "\n".join(summary)
