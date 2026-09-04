#!/usr/bin/env python
"""Fit/print sanity check for a basket against a (printed) body.

    python tools/check_fit.py corpo.stl cesto.stl [--out preview.png]

Checks: single watertight body, basket-vs-body collision when seated and while
being inserted, seating drop (how far the basket falls before touching the
body), open perimeter in the slot zone (both walls in series), and writes an
(r, z) cross-section PNG with the pipe overlaid. z = 0 is the pipe rim.
"""
import argparse
import math

import numpy as np
import trimesh


def bodies(m):
    return len(m.split(only_watertight=False))


def inside_count(body, part, dz=0.0, step=4):
    p = part.copy()
    if dz:
        p.apply_translation([0, 0, dz])
    return int(body.contains(p.vertices[::step]).sum()), len(p.vertices[::step])


def open_fraction(body, basket, z0=5.0, z1=68.0, r_body=72.0, r_basket=68.2):
    th = np.linspace(0, 2 * math.pi, 720, endpoint=False)
    zz = np.linspace(z0, z1, 20)
    T, Z = np.meshgrid(th, zz)

    def opn(m, r):
        return ~m.contains(np.c_[r * np.cos(T).ravel(), r * np.sin(T).ravel(), Z.ravel()])

    oc = opn(body, r_body)
    ob = opn(basket, r_basket)
    return oc.mean(), (oc & ob).mean()


def seating_drop(body, basket, max_drop=6.0, step=0.2):
    dz = 0.0
    while dz < max_drop:
        n, _ = inside_count(body, basket, -dz, step=2)
        if n:
            return dz - step
        dz += step
    return None


def section_png(body, basket, path, angle_deg=30.0):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    a = math.radians(angle_deg)
    nrm = [math.sin(a), -math.cos(a), 0]
    u = np.array([math.cos(a), math.sin(a), 0])
    fig, ax = plt.subplots(figsize=(13, 8))
    for m, color, lbl in [(body, "#1668dc", "corpo"), (basket, "#d4380d", "cesto")]:
        sec = m.section(plane_origin=[0, 0, 0], plane_normal=nrm)
        if sec is None:
            continue
        for poly in sec.discrete:
            ax.plot(poly @ u, poly[:, 2], color=color, lw=1.2)
        ax.plot([], [], color=color, label=lbl)
    for sx in (1, -1):  # pipe: ID 143 / OD 150
        ax.fill_betweenx([-95, 0], sx * 71.5, sx * 75, color="gray", alpha=0.5)
    ax.axhline(0, color="deepskyblue", ls="--", lw=1)
    ax.set_aspect("equal")
    ax.grid(alpha=0.3)
    ax.legend(loc="lower left")
    ax.set_title(f"corte a {angle_deg:.0f} deg — z=0 = borda do cano")
    fig.tight_layout()
    fig.savefig(path, dpi=100)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("corpo")
    ap.add_argument("cesto")
    ap.add_argument("--out", default="check_fit.png")
    ap.add_argument("--angle", type=float, default=30.0, help="section plane angle (deg)")
    args = ap.parse_args()

    body = trimesh.load(args.corpo)
    basket = trimesh.load(args.cesto)
    print(f"corpo: {bodies(body)} body(ies), watertight={body.is_watertight}")
    print(f"cesto: {bodies(basket)} body(ies), watertight={basket.is_watertight}, "
          f"z {basket.bounds[0][2]:.1f}..{basket.bounds[1][2]:.1f}")
    for dz in (0.0, 20.0, 50.0):
        n, tot = inside_count(body, basket, dz)
        print(f"  cesto @ +{dz:.0f} mm: {n}/{tot} vertices inside corpo  {'OK' if n == 0 else 'COLLISION'}")
    drop = seating_drop(body, basket)
    print(f"  seating drop: {'%.1f mm' % drop if drop is not None else 'none within 6 mm (hangs from above?)'}")
    fc, fboth = open_fraction(body, basket)
    print(f"  open perimeter in slot zone: corpo {fc*100:.0f}%, corpo+cesto {fboth*100:.0f}% "
          f"-> weir eq. {fboth*2*math.pi*74:.0f} mm (bare pipe 450)")
    section_png(body, basket, args.out, args.angle)
    print(f"  section -> {args.out}")


if __name__ == "__main__":
    main()
