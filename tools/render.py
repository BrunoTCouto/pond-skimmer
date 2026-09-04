#!/usr/bin/env python
"""Render the documentation figures from the STLs in stl/ into docs/images/.

    python tools/render.py            # run from the repo root

Figures: shaded 3D views (matplotlib, no GPU needed), (r, z) cross-sections
with the pipe overlaid, and the "same water level" hydraulics sketch.
"""
import math
import os

import numpy as np
import trimesh
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from mpl_toolkits.mplot3d.art3d import Poly3DCollection  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STL = os.path.join(ROOT, "stl")
OUT = os.path.join(ROOT, "docs", "images")
BLUE, ORANGE, GRAY = "#4a90d9", "#e07b54", "#9a9a9a"
LBLUE, LORANGE = "#1668dc", "#d4380d"
# the README shows the latest version; bump these when a new version folder is added
LATEST, LATEST_CORPO, LATEST_CESTO = "v2.3-petg-45-folga", "corpo150_v2.3.stl", "cesto150_v2.3.stl"


def load(version, name):
    return trimesh.load(os.path.join(STL, version, name))


def pipe(od=150.0, id_=143.0, depth=120.0):
    p = trimesh.creation.annulus(r_min=id_ / 2, r_max=od / 2, height=depth)
    p.apply_translation([0, 0, -depth / 2])
    return p


def show3d(ax, meshes, title, elev=18, azim=-60):
    pts = []
    for m, fc in meshes:
        tri = m.vertices[m.faces]
        n = m.face_normals
        light = np.array([0.4, -0.5, 0.75])
        light /= np.linalg.norm(light)
        lum = np.clip(n @ light, 0.15, 1.0)
        base = np.array(matplotlib.colors.to_rgb(fc))
        pc = Poly3DCollection(tri, edgecolor="none")
        pc.set_facecolor(np.c_[base[0] * lum, base[1] * lum, base[2] * lum])
        ax.add_collection3d(pc)
        pts.append(m.vertices)
    p = np.vstack(pts)
    c = (p.min(0) + p.max(0)) / 2
    r = (p.max(0) - p.min(0)).max() / 2
    ax.set_xlim(c[0] - r, c[0] + r)
    ax.set_ylim(c[1] - r, c[1] + r)
    ax.set_zlim(c[2] - r, c[2] + r)
    ax.view_init(elev=elev, azim=azim)
    ax.set_axis_off()
    ax.set_title(title)


def section(ax, meshes, angle_deg, title, xlim=(-100, 100), ylim=(-80, 95), water=True):
    a = math.radians(angle_deg)
    nrm = [math.sin(a), -math.cos(a), 0]
    u = np.array([math.cos(a), math.sin(a), 0])
    for m, color, lbl in meshes:
        sec = m.section(plane_origin=[0, 0, 0], plane_normal=nrm)
        if sec is None:
            continue
        for poly in sec.discrete:
            ax.plot(poly @ u, poly[:, 2], color=color, lw=1.2)
        ax.plot([], [], color=color, label=lbl)
    for sx in (1, -1):
        ax.fill_betweenx([ylim[0], 0], sx * 71.5, sx * 74.5, color="gray", alpha=0.5)
    if water:
        ax.fill_between(xlim, [0, 0], [ylim[0], ylim[0]], color="deepskyblue", alpha=0.07)
    ax.axhline(0, color="deepskyblue", ls="--", lw=1)
    ax.text(xlim[1] - 2, 2, "borda do cano = nível de referência", ha="right", color="#0958d9", fontsize=9)
    ax.set_aspect("equal")
    ax.grid(alpha=0.3)
    ax.legend(loc="lower left")
    ax.set_title(title)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)


def fig_turbo(corpo, v4):
    seated = v4.copy()
    seated.apply_translation([0, 0, -1.2])
    fig = plt.figure(figsize=(18, 12))
    show3d(fig.add_subplot(2, 3, 1, projection="3d"), [(corpo, BLUE)],
           "Corpo turbo — coroa 80 mm, 80 fendas de 3 mm", elev=15)
    show3d(fig.add_subplot(2, 3, 2, projection="3d"), [(v4, ORANGE)],
           "Cesto v4 — fendas 2 mm, cone, botão", elev=15)
    show3d(fig.add_subplot(2, 3, 3, projection="3d"), [(corpo, BLUE), (seated, ORANGE), (pipe(), GRAY)],
           "Montado no cano de 150 mm", elev=15)
    section(fig.add_subplot(2, 1, 2), [(corpo, LBLUE, "corpo"), (seated, LORANGE, "cesto v4 (assentado)")],
            30, "Corte — saia dentro do cano, flange na borda, coroa acima; cesto assenta no chanfro da saia")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "turbo_montado.png"), dpi=100)
    plt.close(fig)


def fig_cestos(v3, v4):
    fig = plt.figure(figsize=(16, 7))
    show3d(fig.add_subplot(1, 2, 1, projection="3d"), [(v3, ORANGE)],
           "Cesto v3 — 3 pilares com abinha (pendura no topo da coroa)", elev=15)
    show3d(fig.add_subplot(1, 2, 2, projection="3d"), [(v4, ORANGE)],
           "Cesto v4 — sem pilares, assenta no chanfro da saia", elev=15)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "cesto_v3_vs_v4.png"), dpi=100)
    plt.close(fig)


def fig_petg(corpo, v5):
    fig = plt.figure(figsize=(18, 12))
    show3d(fig.add_subplot(2, 3, 1, projection="3d"), [(corpo, BLUE)],
           f"{LATEST} — corpo: coroa turbo + anel de assento interno a 45°", elev=15)
    show3d(fig.add_subplot(2, 3, 2, projection="3d"), [(v5, ORANGE)],
           "cesto: borda a 45° que assenta no anel; 72 fendas; folga 0,7 mm", elev=15)
    show3d(fig.add_subplot(2, 3, 3, projection="3d"), [(corpo, BLUE), (v5, ORANGE), (pipe(), GRAY)],
           "conjunto PETG montado no cano", elev=15)
    section(fig.add_subplot(2, 1, 2), [(corpo, LBLUE, "corpo PETG"), (v5, LORANGE, "cesto v5")], 30,
            "Corte — o cesto encosta no anel de 45° dentro da saia: batente positivo, autocentrante, não trava")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "petg_montado.png"), dpi=100)
    plt.close(fig)


def fig_nivel():
    """Two crowns, same pump: only the submerged slot length works, so the
    level settles at the same height — extra crown height is dry wall."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=True)
    for ax, top, title in [(axes[0], 55, "Coroa de 55 mm"), (axes[1], 120, "Coroa de 120 mm")]:
        level = 45
        ax.fill_between([-100, 100], -60, level, color="deepskyblue", alpha=0.15)
        for sx in (1, -1):
            ax.fill_betweenx([-60, 0], sx * 71.5, sx * 74.5, color="gray", alpha=0.6)   # pipe
            # crown wall drawn as dashes = slots
            zs = np.arange(2, top - 2, 6)
            for z in zs:
                col = "#1668dc" if z < level else "#b0b0b0"
                ax.plot([sx * 72, sx * 72], [z, z + 3.5], color=col, lw=6, solid_capstyle="butt")
            for z in (10, 22, 34):
                ax.annotate("", xy=(sx * 68, z), xytext=(sx * 92, z),
                            arrowprops=dict(arrowstyle="->", color="#0958d9", lw=1.5))
        ax.axhline(level, color="#0958d9", ls="--", lw=1.2)
        ax.text(0, level + 3, f"nível: {level} mm acima da borda", ha="center", color="#0958d9")
        if top > 60:
            ax.text(0, 95, "fenda seca = parede\n(0 de vazão)", ha="center", color="#777")
        ax.set_xlim(-100, 100)
        ax.set_ylim(-60, 130)
        ax.set_aspect("equal")
        ax.set_title(title)
        ax.set_xticks([])
        ax.set_ylabel("mm acima da borda do cano")
    fig.suptitle("Mesma bomba → mesma área submersa necessária → mesmo nível. Altura não é vazão.")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "nivel_altura_nao_ajuda.png"), dpi=100)
    plt.close(fig)


def main():
    os.makedirs(OUT, exist_ok=True)
    V1, V2 = "v1.0-instalado", LATEST
    corpo, v3, v4 = load(V1, "corpo150_turbo.stl"), load(V1, "cesto150_v3.stl"), load(V1, "cesto150_v4.stl")
    fig_turbo(corpo, v4)
    fig_cestos(v3, v4)
    fig_petg(load(V2, LATEST_CORPO), load(V2, LATEST_CESTO))
    fig_nivel()
    print("figures ->", OUT)


if __name__ == "__main__":
    main()
