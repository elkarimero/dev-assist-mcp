"""Génération de docstrings pour fonctions/classes Python (squelette : template ; LLM plus tard)."""

import ast
import textwrap


async def generate_docs(code: str) -> str:
    """
    Génère une proposition de documentation pour le code Python fourni.
    Squelette : extrait signature et noms ; à enrichir avec un LLM pour le contenu.
    """
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return f"Erreur de syntaxe : {e}"

    parts = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            args = [arg.arg for arg in node.args.args if arg.arg != "self"]
            args_str = ", ".join(args)
            parts.append(
                f"def {node.name}({args_str}):\n"
                f'    """TODO: décrire la fonction et les paramètres."""\n'
            )
        if isinstance(node, ast.AsyncFunctionDef):
            args = [arg.arg for arg in node.args.args if arg.arg != "self"]
            args_str = ", ".join(args)
            parts.append(
                f"async def {node.name}({args_str}):\n"
                f'    """TODO: décrire la fonction et les paramètres."""\n'
            )
        if isinstance(node, ast.ClassDef):
            parts.append(
                f"class {node.name}:\n"
                f'    """TODO: décrire la classe."""\n'
            )

    if not parts:
        return "Aucune fonction ou classe trouvée dans le code. Envisager d'appeler un LLM pour du code plus complexe."
    return (
        "# Proposition de documentation (squelette)\n\n"
        "Enrichir ce module avec un LLM pour générer des docstrings complètes.\n\n"
        + "\n".join(parts)
    )
