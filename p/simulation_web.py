"""
Pont entre mmm.py et l'interface web.
Utilise uniquement les fonctions de mmm.py (via mmm_loader), sans les modifier.
"""
import io
import random
import tempfile
from pathlib import Path

import networkx as nx

from mmm_loader import load_mmm

_mmm = load_mmm()
IC = _mmm["IC"]
RIS = _mmm["RIS"]
animate_propagation = _mmm["animate_propagation"]
animate_propagationbis = _mmm["animate_propagationbis"]


def _pad_arrettab(arrettab, target_len):
    """Aligne arrettab sur le nombre de frames (mmm.py démarre history avant arrettab)."""
    padded = [set() for _ in range(target_len - len(arrettab))] + list(arrettab)
    return padded[:target_len]


def _edges_to_json(edges):
    return [[int(u), int(v)] for u, v in edges]


def run_simulation(model, n, m, p, q, initial, seed):
    random.seed(seed)
    g = nx.barabasi_albert_graph(int(n), int(m), seed=int(seed))
    pos = nx.spring_layout(g, seed=int(seed))

    pos_json = {str(node): {"x": float(pos[node][0]), "y": float(pos[node][1])} for node in g.nodes()}
    edges_json = [[int(u), int(v)] for u, v in g.edges()]

    if model == "IC":
        history, arrettab = IC(g, float(p), int(initial))
        arrettab = _pad_arrettab(arrettab, len(history))
        frames = []
        for i, active in enumerate(history):
            frames.append(
                {
                    "step": i,
                    "diffuseurs": [int(x) for x in active],
                    "lasses": [],
                    "red_edges": _edges_to_json(arrettab[i]),
                }
            )
        meta = {"model": "IC", "steps": len(frames), "p": p, "initial": initial}

    elif model == "RIS":
        hit, his, arrettab = RIS(g, float(p), float(q), int(initial))
        arrettab = _pad_arrettab(arrettab, len(hit))
        frames = []
        for i in range(len(hit)):
            frames.append(
                {
                    "step": i,
                    "diffuseurs": [int(x) for x in hit[i]],
                    "lasses": [int(x) for x in his[i]],
                    "red_edges": _edges_to_json(arrettab[i]),
                }
            )
        meta = {"model": "RIS", "steps": len(frames), "p": p, "q": q, "initial": initial}

    else:
        raise ValueError(f"Modèle inconnu : {model}")

    return {
        "meta": meta,
        "graph": {"nodes": list(g.nodes()), "edges": edges_json, "positions": pos_json},
        "frames": frames,
        "_graph": g,
        "_pos": pos,
        "_history_ic": history if model == "IC" else None,
        "_arret_ic": arrettab if model == "IC" else None,
        "_hit": hit if model == "RIS" else None,
        "_his": his if model == "RIS" else None,
        "_arrettab_ris": arrettab if model == "RIS" else None,
    }


def render_gif(result, model):
    """Génère un GIF avec les fonctions animate_* de mmm.py."""
    g = result["_graph"]
    pos = result["_pos"]
    out_dir = Path(tempfile.gettempdir()) / "propagation_web"
    out_dir.mkdir(exist_ok=True)
    path = out_dir / f"{model}_{random.randint(1000, 9999)}.gif"

    if model == "IC":
        animate_propagation(g, result["_history_ic"], result["_arret_ic"], pos, str(path))
    else:
        animate_propagationbis(g, result["_his"], result["_hit"], result["_arrettab_ris"], pos, str(path))

    return path.read_bytes()
