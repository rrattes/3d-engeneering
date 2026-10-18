"""Three removable, open organizer trays on a shallow common base."""
from build123d import Align, Box, Cylinder, Pos


def build(params):
    p = params["organizer"]
    L, W, H = p["length"], p["width"], p["height"]
    wall, floor = p["wall"], p["floor"]
    gap, rail_h, base_h = p["clearance"], p["rail_height"], p["base_height"]
    count = int(p["module_count"])
    usable_w = W - 2 * p["rim"]
    usable_l = L - 2 * p["rim"]
    slot_w = (usable_w - (count - 1) * p["slot_gap"]) / count
    module_w = slot_w - 2 * gap
    module_l = usable_l - 2 * gap
    if min(L, W, H, wall, floor, base_h, module_w, module_l) <= 0:
        raise ValueError("Envelope and feature dimensions must be positive")
    if H < base_h + rail_h + floor + wall:
        raise ValueError("Organizer height cannot contain base, rails and trays")

    # Outer base is the envelope datum: XY centered, Z=0 on the bench.
    base = Box(L, W, base_h, align=(Align.CENTER, Align.CENTER, Align.MIN))
    # Low continuous perimeter rim and three pairs of guide rails.
    rim = p["rim"]
    perimeter = Pos(0, 0, base_h) * (Box(L, W, rail_h, align=(Align.CENTER, Align.CENTER, Align.MIN)) - Pos(0, 0, -0.1) * Box(
        L - 2 * rim, W - 2 * rim, rail_h + 0.2,
        align=(Align.CENTER, Align.CENTER, Align.MIN)))
    base = base + perimeter

    parts = {"base": base}
    for i in range(count):
        x = -usable_w / 2 + slot_w * (i + 0.5)
        z = base_h
        tray = Pos(0, 0, z) * Box(module_l, module_w, p["tray_height"], align=(Align.CENTER, Align.CENTER, Align.MIN))
        cavity = Pos(0, 0, z + floor) * Box(module_l - 2 * wall, module_w - 2 * wall,
                 p["tray_height"] + 0.1, align=(Align.CENTER, Align.CENTER, Align.MIN))
        tray = tray - cavity
        # Broad front scoop leaves a visible, finger-accessible retrieval edge.
        notch = Pos(0, -module_w / 2 - 0.01, z + p["tray_height"] + 0.1) * Cylinder(
            p["access_radius"], wall + 0.2, rotation=(-90, 0, 0), align=(Align.CENTER, Align.CENTER, Align.MIN))
        tray = tray - notch
        # Each tray is separate and can be lifted by its open front edge.
        parts[f"module_{i+1}"] = tray
    return parts
