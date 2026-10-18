"""Módulo de circulação passiva em três câmaras, dimensões em mm."""
from build123d import Align, Box, Cylinder, Mode, Pos, Rot


def build(params):
    p = params["module"]
    L, W, H = p["length"], p["width"], p["body_height"]
    t = p["wall"]
    chamber_len = (L - 2*t) / 3
    slot_w, slot_h, slot_z = p["slot_width"], p["slot_height"], p["slot_bottom"]
    hose_od, hose_id, barb_len = p["hose_od"], p["hose_id"], p["barb_length"]
    if L > 160 or W > 100 or H + p["lid_height"] > 90:
        raise ValueError("Envelope excedido")
    if 3*chamber_len <= 0 or slot_w >= W-2*t or slot_h+slot_z >= H-t:
        raise ValueError("Passagem ou câmaras incompatíveis")

    outer = Box(L, W, H, align=(Align.CENTER, Align.CENTER, Align.MIN))
    cavity = Pos(0, 0, t) * Box(L-2*t, W-2*t, H,
                                align=(Align.CENTER, Align.CENTER, Align.MIN))
    body = outer - cavity

    # Duas divisórias com passagens largas junto ao fundo; topo aberto para purga e limpeza.
    for x in (-chamber_len/2, chamber_len/2):
        wall = Pos(x, 0, t) * Box(t, W-2*t, H-t,
                                  align=(Align.CENTER, Align.CENTER, Align.MIN))
        body = body + wall
        slot = Pos(x, 0, slot_z) * Box(t+2, slot_w, slot_h,
                                       align=(Align.CENTER, Align.CENTER, Align.MIN))
        body = body - slot

    # Espigões integrais coaxiais ao comprimento; furo contínuo liga a câmara terminal.
    for sign in (-1, 1):
        x = sign * (L/2 + barb_len/2)
        boss = Pos(x, 0, H/2) * Rot(0, 90, 0) * Cylinder(
            hose_od/2, barb_len, align=(Align.CENTER, Align.CENTER, Align.CENTER))
        body = body + boss
        bore_x = sign * (L/2 + barb_len/2 - t/2)
        bore = Pos(bore_x, 0, H/2) * Rot(0, 90, 0) * Cylinder(
            hose_id/2, barb_len+t+2, align=(Align.CENTER, Align.CENTER, Align.CENTER))
        body = body - bore

    lid = Box(L, W, p["lid_height"], align=(Align.CENTER, Align.CENTER, Align.MIN))
    return {"body": body, "lid": lid}
