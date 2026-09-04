# "v1 turbo": crown on the pipe mouth + hanging basket, tuned for FLOW.
#   - 80 slots x 3 mm, ribs ~2.4 mm  -> ~55% of the perimeter open
#   - crown 80 mm tall, 4 mm wall, 2 bracing rings, rim notches every other slot
#   - cesto v3: 3 posts with tabs on the crown top (the PLA one)
#   - cesto v4: seats on the skirt's bore bevel, nothing above the rim (PETG reprint)
# z = 0 is the pipe-rim plane. Units mm.  (reconstructed after the scratchpad was wiped)

import math
import numpy as np
from manifold3d import Manifold, CrossSection
import trimesh

SEG = 200

# ---------------- corpo (as printed) ----------------
SKIRT_LEN, SKIRT_R_TOP, SKIRT_R_BOT, SKIRT_WALL = 45.0, 71.0, 68.0, 2.4
FLANGE_T, FLANGE_R_IN, FLANGE_R_OUT = 3.5, 70.0, 79.0
CROWN_R_IN, CROWN_R_OUT = 70.0, 74.0
BRACE_T = 2.0
CROWN_TOP, CROWN_SLOT_TOP = 80.0, 70.0
N_SLOTS, CROWN_SLOT_W, SLOT_TILT = 80, 3.0, 20.0

# ---------------- cesto (shared) ----------------
COLLAR_R_OUT = 69.3
COLLAR_WALL = 2.2
N_POSTS, POST_W, POST_T = 3, 8.0, 3.0
TAB_R_OUT, TAB_T = 72.0, 4.0
GUSSET_H = 14.0
BASK_R_OUT, BASK_WALL, BASK_BOTTOM_Z = 63.0, 2.0, -60.0
FINE_SLOT_W, N_FINE, FINE_Z0, FINE_Z1, FINE_TILT = 2.0, 36, -52.0, -10.3, 30.0
LIP_Z0 = 80.0
CONE_R_RIM, CONE_Z_RIM, CONE_R_HUB, CONE_T_Z = 62.5, -58.0, 11.0, 3.4
CONE_SLOT_W, CONE_OUTER, CONE_INNER = 2.0, (48, 40.0, 57.0), (24, 18.0, 36.0)
KNOB_EXTRA = 20.0

# ---------------- cesto v4: bevel seat ----------------
# printed corpo has a 13-deg bevel in the skirt bore: r 68 @ z-10 -> 70.3 @ z0.
# a matching cone 0.3 mm inside it seats with area contact and self-centers.
SEAT_Z0, SEAT_Z1 = -13.0, -3.0
SEAT_R0, SEAT_R1 = 67.0, 69.3           # slope 0.23 = parallel to the bevel
SEAT_WALL = 2.4
COLLAR4_R, COLLAR4_Z1 = 69.2, 3.0       # centering collar, 0.8 mm to the flange bore
FINE4_Z0, FINE4_Z1 = -52.0, -20.0

# ---------------- PETG set: corpo with an internal 45-deg seat + cesto v5 ----------------
# The skirt gets a solid ledge inside; its top face is a 45-deg cone (prints as
# a 45-deg overhang with the corpo upside-down). The basket's top flares 45 deg
# and lands on it: positive stop, self-centering, does NOT self-lock (unlike
# the 13-deg bevel seat of v4). No bevel cut in this corpo.
SEAT5_R_IN  = 64.5                      # ledge reaches inward to here
SEAT5_Z_BOT = -9.0                      # flat underside of the ledge
SEAT5_R_TOP = 68.7                      # where the 45-deg face meets the skirt bore
V5_TOP_R    = 68.0                      # basket collar radius (0.6 mm to the skirt bore)
V5_TOP_Z    = -3.0                      # nothing above this (rim is z=0)
FINE5_Z0, FINE5_Z1 = -52.0, -16.0
N_FINE5 = 72                            # 2x the v3/v4 slot count: ribs ~2.8 mm, ~42% open


def tube(r_out, r_in, z0, z1, seg=SEG):
    h = z1 - z0
    return (Manifold.cylinder(h, r_out, r_out, seg).translate([0, 0, z0])
            - Manifold.cylinder(h + 2, r_in, r_in, seg).translate([0, 0, z0 - 1]))


def cone_tube(r0, r1, wall, z0, z1, seg=SEG):
    h = z1 - z0
    return (Manifold.cylinder(h, r0, r1, seg).translate([0, 0, z0])
            - Manifold.cylinder(h + 2, r0 - wall, r1 - wall, seg).translate([0, 0, z0 - 1]))


def radial_cuts(n, width, r_in, r_out, z0, z1, phase=0.0, tilt=0.0):
    if tilt == 0.0:
        cut = Manifold.cube([r_out - r_in, width, z1 - z0]).translate([r_in, -width / 2, z0])
    else:
        t = math.radians(tilt)
        L = (z1 - z0) / math.cos(t) + width * math.tan(t) + 2.0
        cut = (Manifold.cube([r_out - r_in, width, L])
               .translate([r_in, -width / 2, -L / 2]).rotate([tilt, 0, 0])
               .translate([0, 0, (z0 + z1) / 2]))
    out = None
    for k in range(n):
        c = cut.rotate([0, 0, math.degrees(2 * math.pi * k / n) + phase])
        out = c if out is None else out + c
    if tilt != 0.0:
        out = out ^ Manifold.cylinder(z1 - z0, r_out + 5, r_out + 5, 32).translate([0, 0, z0])
    return out


def build_corpo():
    skirt = cone_tube(SKIRT_R_BOT, SKIRT_R_TOP, SKIRT_WALL, -SKIRT_LEN, 0.0)
    flange = tube(FLANGE_R_OUT, FLANGE_R_IN, 0.0, FLANGE_T)
    cham = (Manifold.cylinder(FLANGE_R_OUT - CROWN_R_OUT, FLANGE_R_OUT, CROWN_R_OUT, SEG)
            .translate([0, 0, FLANGE_T])
            - Manifold.cylinder(10.0, CROWN_R_IN, CROWN_R_IN, SEG).translate([0, 0, FLANGE_T - 1]))
    crown = tube(CROWN_R_OUT, CROWN_R_IN, FLANGE_T, CROWN_TOP)
    fuse = tube(SKIRT_R_TOP, 70.2, -2.0, FLANGE_T)
    body = skirt + flange + cham + crown + fuse
    body -= Manifold.cylinder(10.0, 68.0, 70.3, SEG).translate([0, 0, -10.0])   # skirt bore bevel
    slots = radial_cuts(N_SLOTS, CROWN_SLOT_W, 58.0, FLANGE_R_OUT + 3,
                        FLANGE_T, CROWN_SLOT_TOP, tilt=SLOT_TILT)
    notches = radial_cuts(N_SLOTS // 2, CROWN_SLOT_W, 68.0, FLANGE_R_OUT + 3, -0.5, FLANGE_T)
    body = body - slots - notches
    for f in (1 / 3, 2 / 3):
        zc = FLANGE_T + f * (CROWN_SLOT_TOP - FLANGE_T)
        body += tube(CROWN_R_OUT, CROWN_R_IN, zc - BRACE_T / 2, zc + BRACE_T / 2)
    return body


def _cone_and_knob():
    def z_out(r):
        return CONE_Z_RIM + (CONE_R_RIM - 0.5 - r)
    A, B = (CONE_R_HUB, z_out(CONE_R_HUB)), (CONE_R_RIM, CONE_Z_RIM)
    C, D = (CONE_R_RIM, BASK_BOTTOM_Z), (CONE_R_HUB, z_out(CONE_R_HUB) - CONE_T_Z)
    cone = Manifold.revolve(CrossSection([[A, D, C, B]]), SEG)
    hub_top = z_out(CONE_R_HUB)
    z0 = hub_top - CONE_T_Z - 0.5
    st = 18.0 + KNOB_EXTRA
    knob = (Manifold.cylinder(hub_top + 1.5 - z0, 13.0, 13.0, 64).translate([0, 0, z0])
            + Manifold.cylinder(st, 7.0, 7.0, 64).translate([0, 0, hub_top])
            + Manifold.cylinder(7.0, 7.0, 14.0, 64).translate([0, 0, hub_top + st - 1.0])
            + Manifold.cylinder(7.0, 14.0, 14.0, 64).translate([0, 0, hub_top + st + 6.0])
            + Manifold.sphere(14.0, 64).translate([0, 0, hub_top + st + 13.0]))
    knob = knob ^ Manifold.cylinder(100.0, 15.0, 15.0, 64).translate([0, 0, z0])
    return cone, knob, hub_top


def _basket_cuts(hub_top, fz0, fz1, n_fine=N_FINE):
    fine = radial_cuts(n_fine, FINE_SLOT_W, 50.0, BASK_R_OUT + 2, fz0, fz1,
                       phase=5.0, tilt=FINE_TILT)
    fine = fine ^ tube(BASK_R_OUT + 3, BASK_R_OUT - BASK_WALL - 1.0, fz0 - 1, fz1 + 1)
    n, ri, ro = CONE_OUTER
    cone_outer = radial_cuts(n, CONE_SLOT_W, ri, ro, BASK_BOTTOM_Z - 1, hub_top + 1)
    n, ri, ro = CONE_INNER
    cone_inner = radial_cuts(n, CONE_SLOT_W, ri, ro, BASK_BOTTOM_Z - 1, hub_top + 1,
                             phase=360.0 / n / 2)
    return fine + cone_outer + cone_inner


def build_cesto_v3():
    trans = cone_tube(BASK_R_OUT, COLLAR_R_OUT, COLLAR_WALL + 0.5, -(COLLAR_R_OUT - BASK_R_OUT), 0.0)
    collar = tube(COLLAR_R_OUT, COLLAR_R_OUT - COLLAR_WALL, -0.5, 2.0)
    post = Manifold.cube([POST_T, POST_W, LIP_Z0 + TAB_T - 1.0]) \
        .translate([COLLAR_R_OUT - POST_T, -POST_W / 2, 1.0])
    tab = Manifold.cube([TAB_R_OUT - (COLLAR_R_OUT - POST_T), POST_W, TAB_T]) \
        .translate([COLLAR_R_OUT - POST_T, -POST_W / 2, LIP_Z0])
    gus = CrossSection([[(POST_W / 2, 1.0), (POST_W / 2 + GUSSET_H, 1.0), (POST_W / 2, 1.0 + GUSSET_H)]])
    gus = gus + CrossSection([[(-POST_W / 2, 1.0), (-POST_W / 2, 1.0 + GUSSET_H), (-POST_W / 2 - GUSSET_H, 1.0)]])
    gusset = (Manifold.extrude(gus, POST_T).rotate([90, 0, 90])
              .translate([COLLAR_R_OUT - POST_T, 0, 0]))
    gusset = gusset ^ tube(69.3, 50.0, 0.0, 30.0)
    unit = post + tab + gusset
    posts = None
    for k in range(N_POSTS):
        p = unit.rotate([0, 0, 360.0 * k / N_POSTS + 30.0])
        posts = p if posts is None else posts + p
    wall = tube(BASK_R_OUT, BASK_R_OUT - BASK_WALL, BASK_BOTTOM_Z, -(COLLAR_R_OUT - BASK_R_OUT) + 0.5)
    cone, knob, hub_top = _cone_and_knob()
    cesto = trans + collar + posts + wall + cone + knob
    return cesto - _basket_cuts(hub_top, FINE_Z0, FINE_Z1)


def build_cesto_v4():
    trans = cone_tube(BASK_R_OUT, SEAT_R0, BASK_WALL + 0.4,
                      SEAT_Z0 - (SEAT_R0 - BASK_R_OUT), SEAT_Z0 + 0.01)      # 45 deg, 63 -> 67
    seat = cone_tube(SEAT_R0, SEAT_R1, SEAT_WALL, SEAT_Z0, SEAT_Z1 + 0.01)   # 13 deg, 67 -> 69.3
    collar = tube(COLLAR4_R, COLLAR4_R - SEAT_WALL, SEAT_Z1, COLLAR4_Z1)
    wall = tube(BASK_R_OUT, BASK_R_OUT - BASK_WALL, BASK_BOTTOM_Z,
                SEAT_Z0 - (SEAT_R0 - BASK_R_OUT) + 0.5)
    cone, knob, hub_top = _cone_and_knob()
    cesto = trans + seat + collar + wall + cone + knob
    return cesto - _basket_cuts(hub_top, FINE4_Z0, FINE4_Z1)


def build_corpo_petg():
    """Turbo corpo + internal 45-deg seat ledge, no bore bevel (PETG reprint)."""
    skirt = cone_tube(SKIRT_R_BOT, SKIRT_R_TOP, SKIRT_WALL, -SKIRT_LEN, 0.0)
    flange = tube(FLANGE_R_OUT, FLANGE_R_IN, 0.0, FLANGE_T)
    cham = (Manifold.cylinder(FLANGE_R_OUT - CROWN_R_OUT, FLANGE_R_OUT, CROWN_R_OUT, SEG)
            .translate([0, 0, FLANGE_T])
            - Manifold.cylinder(10.0, CROWN_R_IN, CROWN_R_IN, SEG).translate([0, 0, FLANGE_T - 1]))
    crown = tube(CROWN_R_OUT, CROWN_R_IN, FLANGE_T, CROWN_TOP)
    fuse = tube(SKIRT_R_TOP, 70.2, -2.0, FLANGE_T)
    # seat ledge: (r, z) profile -> flat bottom, 45-deg top face, welded 1 mm into the skirt wall
    z_top = SEAT5_Z_BOT + (SEAT5_R_TOP - SEAT5_R_IN)
    prof = CrossSection([[(SEAT5_R_IN, SEAT5_Z_BOT), (SEAT5_R_TOP + 1.0, SEAT5_Z_BOT),
                          (SEAT5_R_TOP + 1.0, z_top), (SEAT5_R_IN, SEAT5_Z_BOT)]])
    seat = Manifold.revolve(prof, SEG)
    body = skirt + flange + cham + crown + fuse + seat
    slots = radial_cuts(N_SLOTS, CROWN_SLOT_W, 58.0, FLANGE_R_OUT + 3,
                        FLANGE_T, CROWN_SLOT_TOP, tilt=SLOT_TILT)
    notches = radial_cuts(N_SLOTS // 2, CROWN_SLOT_W, 68.0, FLANGE_R_OUT + 3, -0.5, FLANGE_T)
    body = body - slots - notches
    for f in (1 / 3, 2 / 3):
        zc = FLANGE_T + f * (CROWN_SLOT_TOP - FLANGE_T)
        body += tube(CROWN_R_OUT, CROWN_R_IN, zc - BRACE_T / 2, zc + BRACE_T / 2)
    return body


def build_cesto_v5():
    """Basket for the PETG corpo: 45-deg flare lands on the seat ledge."""
    # flare outer line r = 63 + (z - z1) must coincide with the seat face
    # r = SEAT5_R_IN + (z - SEAT5_Z_BOT)  ->  z1 = SEAT5_Z_BOT - (SEAT5_R_IN - BASK_R_OUT)
    z1 = SEAT5_Z_BOT - (SEAT5_R_IN - BASK_R_OUT)
    z2 = z1 + (V5_TOP_R - BASK_R_OUT)
    flare = cone_tube(BASK_R_OUT, V5_TOP_R, BASK_WALL + 0.4, z1, z2 + 0.01)
    collar = tube(V5_TOP_R, V5_TOP_R - BASK_WALL - 0.4, z2, V5_TOP_Z)
    wall = tube(BASK_R_OUT, BASK_R_OUT - BASK_WALL, BASK_BOTTOM_Z, z1 + 0.5)
    cone, knob, hub_top = _cone_and_knob()
    cesto = flare + collar + wall + cone + knob
    return cesto - _basket_cuts(hub_top, FINE5_Z0, FINE5_Z1, n_fine=N_FINE5)


def export(m, path):
    mesh = m.to_mesh()
    tm = trimesh.Trimesh(vertices=np.asarray(mesh.vert_properties)[:, :3],
                         faces=np.asarray(mesh.tri_verts))
    tm.export(path)
    print(f"{path}: {len(tm.faces)} faces, watertight={tm.is_watertight}, "
          f"bbox={np.round(tm.bounds, 1).tolist()}")


if __name__ == "__main__":
    import os
    ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    V1 = os.path.join(ROOT, "stl", "v1.0-instalado")   # what is in the pond (ABS corpo + PLA cesto v3)
    V2 = os.path.join(ROOT, "stl", "v2.0-petg")        # PETG reprint set
    os.makedirs(V1, exist_ok=True)
    os.makedirs(V2, exist_ok=True)
    export(build_corpo(), os.path.join(V1, "corpo150_turbo.stl"))      # PRINTED (ABS) - do not change
    export(build_cesto_v3(), os.path.join(V1, "cesto150_v3.stl"))      # PRINTED (PLA)
    export(build_cesto_v4(), os.path.join(V1, "cesto150_v4.stl"))      # fits the printed corpo (bevel seat)
    export(build_corpo_petg(), os.path.join(V2, "corpo150_petg.stl"))  # corpo with internal 45-deg seat
    export(build_cesto_v5(), os.path.join(V2, "cesto150_v5.stl"))      # basket for corpo150_petg ONLY
