"""
Charge mmm.py SANS exécuter le bloc principal (lignes 143+).
Permet d'utiliser IC, RIS, animate_* sans modifier mmm.py.
"""
from pathlib import Path


def load_mmm():
    path = Path(__file__).parent / "mmm.py"
    text = path.read_text(encoding="utf-8")

    # Tout ce qui est avant la création du graphe de démo = définitions uniquement
    marker = "\nD = nx.barabasi"
    if marker not in text:
        raise RuntimeError("Impossible de séparer les fonctions du main dans mmm.py")
    code = text.split(marker)[0]

    namespace = {"__name__": "mmm_loaded", "__file__": str(path)}
    exec(compile(code, str(path), "exec"), namespace)
    return namespace
