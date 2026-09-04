# Pond skimmer v2 for a 150 mm OD PVC pipe (ID 143-145) -- "fish fence" layout.
# PLAN B, never printed.
#
# v1 put a slotted crown ON the pipe mouth and turned a 450 mm free weir into
# ~85 mm of effective crest: the pond rose over the crown. v2 leaves the pipe
# rim untouched as the weir and surrounds it with a large slotted fence
# (3 mm fish gate, ~13000 mm2 submerged inlet area). Two parts:
#   corpo: fence (dia 191) + slotted floor ring + sleeve over the pipe OD,
#          6 small L-tabs hook over the rim to set the height
#   cesto: basket hanging inside the pipe from 3 thin hooks, fine slots +
#          sunburst cone floor + lifting knob
# z = 0 is the pipe-rim plane. Units mm.

import math
import numpy as np
from manifold3d import Manifold, CrossSection
import trimesh

SEG = 200

# ---------------- pipe (measured) ----------------
PIPE_OD_MAX = 151.0                 # wall 3 mm, ID 143-145
PIPE_ID_MIN = 143.0

# ---------------- corpo: fence ----------------
FENCE_R_OUT = 95.5                  # dia 191 (fits a 256 mm bed)
FENCE_WALL  = 2.4
FENCE_Z0, FENCE_Z1 = -45.0, 40.0    # 45 below water, 40 above
N_FENCE     = 100
FENCE_SLOT_W = 3.0                  # fish gate (perpendicular width)
FENCE_TILT  = 20.0                  # mild slant: ribs stay ~2.5 mm wide
RING_T      = 3.0                   # stiffening rings (top, bottom, 2 mid)
MID_RINGS   = (-22.0, 18.0)         # never at z=0 (surface skimming line)

FLOOR_T     = 3.0                   # slotted floor ring at FENCE_Z0
FLOOR_SLOT_W = 3.0
N_FLOOR     = 60

SLEEVE_R_IN = 76.0                  # dia 152 over the 149-151 pipe
SLEEVE_WALL = 2.0
SLEEVE_Z1   = -5.0                  # ends below the rim: the rim stays the weir
N_TABS      = 6
TAB_W       = 6.0                   # L-tabs resting on the rim (z 0..2)
TAB_T       = 2.0
TAB_R_IN    = 71.3                  # overlaps the rim for ID 143 and 145

# ---------------- cesto: basket ----------------
BASK_R_OUT  = 63.0
BASK_WALL   = 2.0
BASK_Z1     = 3.0                   # wall top (hooks attach here)
BASK_BOTTOM_Z = -60.0
FINE_SLOT_W = 2.0                   # < fence gate: whatever gets in stays in
N_FINE      = 36
FINE_Z0, FINE_Z1 = -52.0, -8.0
FINE_TILT   = 30.0
N_HOOKS     = 3
HOOK_W      = 8.0
HOOK_R_OUT  = 76.5                  # reaches past the rim (r 71.5..74.5)
HOOK_T      = 3.0

CONE_R_RIM, CONE_Z_RIM = 62.5, -58.0
CONE_R_HUB  = 11.0
CONE_T_Z    = 3.4
CONE_SLOT_W = 2.0
CONE_OUTER  = (48, 40.0, 57.0)
CONE_INNER  = (24, 18.0, 36.0)


def tube(r_out, r_in, z0, z1, seg=SEG):
    h = z1 - z0
    return (Manifold.cylinder(h, r_out, r_out, seg).translate([0, 0, z0])
            - Manifold.cylinder(h + 2, r_in, r_in, seg).translate([0, 0, z0 - 1]))


def radial_cuts(n, width, r_in, r_out, z0, z1, phase=0.0, tilt=0.0):
    if tilt == 0.0:
        cut = Manifold.cube([r_out - r_in, width, z1 - z0]).translate([r_in, -width / 2, z0])
    else:
        t = math.radians(tilt)
        L = (z1 - z0) / math.cos(t) + width * math.tan(t) + 2.0
        cut = (Manifold.cube([r_out - r_in, width, L])
               .translate([r_in, -width / 2, -L / 2])
               .rotate([tilt, 0, 0])
               .translate([0, 0, (z0 + z1) / 2]))
    out = None
    for k in range(n):
        c = cut.rotate([0, 0, math.degrees(2 * math.pi * k / n) + phase])
        out = c if out is None else out + c
    if tilt != 0.0:
        out = out ^ Manifold.cylinder(z1 - z0, r_out + 5, r_out + 5, 32).translate([0, 0, z0])
    return out


# ============================ CORPO ============================
def build_corpo():
    fence = tube(FENCE_R_OUT, FENCE_R_OUT - FENCE_WALL, FENCE_Z0, FENCE_Z1)
    slots = radial_cuts(N_FENCE, FENCE_SLOT_W, FENCE_R_OUT - 35, FENCE_R_OUT + 3,
                        FENCE_Z0 + FLOOR_T + 2, FENCE_Z1 - RING_T, tilt=FENCE_TILT)
    # confine to the fence wall annulus (tilted boxes reach inward)
    slots = slots ^ tube(FENCE_R_OUT + 3, FENCE_R_OUT - FENCE_WALL - 1, FENCE_Z0, FENCE_Z1)
    fence = fence - slots
    for zc in MID_RINGS:
        fence += tube(FENCE_R_OUT, FENCE_R_OUT - FENCE_WALL - 0.8, zc - RING_T / 2, zc + RING_T / 2)

    floor = tube(FENCE_R_OUT - 0.5, SLEEVE_R_IN + 0.5, FENCE_Z0, FENCE_Z0 + FLOOR_T)
    floor -= radial_cuts(N_FLOOR, FLOOR_SLOT_W, SLEEVE_R_IN + SLEEVE_WALL + 4,
                         FENCE_R_OUT - FENCE_WALL - 3, FENCE_Z0 - 1, FENCE_Z0 + FLOOR_T + 1)

    sleeve = tube(SLEEVE_R_IN + SLEEVE_WALL, SLEEVE_R_IN, FENCE_Z0, SLEEVE_Z1)

    # L-tabs: continue the sleeve up past the rim, then a 2 mm lip inward over it
    tab = (Manifold.cube([SLEEVE_WALL + 0.5, TAB_W, TAB_T + 2 - SLEEVE_Z1])
           .translate([SLEEVE_R_IN, -TAB_W / 2, SLEEVE_Z1 - 1])
           + Manifold.cube([SLEEVE_R_IN + SLEEVE_WALL - TAB_R_IN, TAB_W, TAB_T])
           .translate([TAB_R_IN, -TAB_W / 2, 0.0]))
    tabs = None
    for k in range(N_TABS):
        t = tab.rotate([0, 0, 360.0 * k / N_TABS])
        tabs = t if tabs is None else tabs + t

    return fence + floor + sleeve + tabs


# ============================ CESTO ============================
def build_cesto():
    wall = tube(BASK_R_OUT, BASK_R_OUT - BASK_WALL, BASK_BOTTOM_Z, BASK_Z1)

    def z_out(r):
        return CONE_Z_RIM + (CONE_R_RIM - 0.5 - r)
    A = (CONE_R_HUB, z_out(CONE_R_HUB))
    B = (CONE_R_RIM, CONE_Z_RIM)
    C = (CONE_R_RIM, BASK_BOTTOM_Z)
    D = (CONE_R_HUB, z_out(CONE_R_HUB) - CONE_T_Z)
    cone = Manifold.revolve(CrossSection([[A, D, C, B]]), SEG)
    hub_top = z_out(CONE_R_HUB)

    z0 = hub_top - CONE_T_Z - 0.5
    knob = (Manifold.cylinder(hub_top + 1.5 - z0, 13.0, 13.0, 64).translate([0, 0, z0])
            + Manifold.cylinder(18.0, 7.0, 7.0, 64).translate([0, 0, hub_top])
            + Manifold.cylinder(7.0, 7.0, 14.0, 64).translate([0, 0, hub_top + 17.0])
            + Manifold.cylinder(7.0, 14.0, 14.0, 64).translate([0, 0, hub_top + 24.0])
            + Manifold.sphere(14.0, 64).translate([0, 0, hub_top + 31.0]))
    knob = knob ^ Manifold.cylinder(80.0, 15.0, 15.0, 64).translate([0, 0, z0])

    # 3 hooks over the pipe rim + 45-deg gusset kept inside the bore (r < 71):
    # gusset = wedge, triangle in (r,z): (62.5,-8) (71,0) (62.5,0)
    g = CrossSection([[(BASK_R_OUT - 0.5, -8.0), (71.0, 0.0), (BASK_R_OUT - 0.5, 0.0)]])
    gusset = Manifold.extrude(g, HOOK_W).rotate([90, 0, 0]).translate([0, HOOK_W / 2, 0])
    hook = (Manifold.cube([HOOK_R_OUT - (BASK_R_OUT - BASK_WALL), HOOK_W, HOOK_T])
            .translate([BASK_R_OUT - BASK_WALL, -HOOK_W / 2, 0.0]) + gusset)
    hooks = None
    for k in range(N_HOOKS):
        h = hook.rotate([0, 0, 360.0 * k / N_HOOKS + 30.0])
        hooks = h if hooks is None else hooks + h

    cesto = wall + cone + knob + hooks

    fine = radial_cuts(N_FINE, FINE_SLOT_W, 50.0, BASK_R_OUT + 2, FINE_Z0, FINE_Z1,
                       phase=5.0, tilt=FINE_TILT)
    fine = fine ^ tube(BASK_R_OUT + 3, BASK_R_OUT - BASK_WALL - 1.0, FINE_Z0 - 1, FINE_Z1 + 1)
    n, ri, ro = CONE_OUTER
    cone_outer = radial_cuts(n, CONE_SLOT_W, ri, ro, BASK_BOTTOM_Z - 1, hub_top + 1)
    n, ri, ro = CONE_INNER
    cone_inner = radial_cuts(n, CONE_SLOT_W, ri, ro, BASK_BOTTOM_Z - 1, hub_top + 1,
                             phase=360.0 / n / 2)
    return cesto - fine - cone_outer - cone_inner


def export(m, path):
    mesh = m.to_mesh()
    tm = trimesh.Trimesh(vertices=np.asarray(mesh.vert_properties)[:, :3],
                         faces=np.asarray(mesh.tri_verts))
    tm.export(path)
    print(f"{path}: {len(tm.faces)} faces, watertight={tm.is_watertight}, "
          f"bbox={np.round(tm.bounds, 1).tolist()}")


if __name__ == "__main__":
    export(build_corpo(), "corpo150_v2.stl")
    export(build_cesto(), "cesto150_v2.stl")
