"""Módulo passivo de três câmaras, tampa removível e bocais acessíveis.

As dimensões dos bocais e folgas de vedação são provisórias até conhecer
mangueira, junta, material e processo de fabricação.
"""
from build123d import Align, Box, Cylinder, Pos, Rot


def build(params):
    p = params["module"]
    L, W, H = p["length"], p["width"], p["height"]
    wall, floor = p["wall"], p["floor"]
    port_d, port_outer_d, port_len = p["port_diameter"], p["port_outer_diameter"], p["port_length"]
    chamber_len = (L - 2 * wall - 2 * p["baffle_thickness"]) / 3
    if min(L, W, H, wall, floor, port_d, port_outer_d, port_len) <= 0:
        raise ValueError("Todos os parâmetros dimensionais precisam ser positivos")
    if L > 160 or W > 100 or H > 90:
        raise ValueError("Envelope máximo permitido: 160 x 100 x 90 mm")
    if 2 * wall >= W or floor >= H or port_d >= W - 2 * wall:
        raise ValueError("Dimensões incompatíveis com paredes/câmaras")
    if port_outer_d <= port_d:
        raise ValueError("O diâmetro externo do bocal precisa exceder o furo")

    # Corpo oco aberto por cima; fundo e paredes unidos como um único sólido.
    outer = Box(L, W, H, align=(Align.MIN, Align.MIN, Align.MIN))
    cavity = Pos(wall, wall, floor) * Box(
        L - 2 * wall, W - 2 * wall, H,
        align=(Align.MIN, Align.MIN, Align.MIN),
    )
    body = outer - cavity

    # Duas divisórias transversais, cada uma com vão inferior amplo para transferência.
    t = p["baffle_thickness"]
    gap_w, gap_h = p["transfer_width"], p["transfer_height"]
    for x in (wall + chamber_len, wall + chamber_len + t + chamber_len):
        baffle = Pos(x, wall, floor) * Box(t, W - 2 * wall, H - floor - wall,
                                            align=(Align.MIN, Align.MIN, Align.MIN))
        opening = Pos(x - 0.1, (W - gap_w) / 2, floor - 0.01) * Box(
            t + 0.2, gap_w, gap_h, align=(Align.MIN, Align.MIN, Align.MIN)
        )
        body += baffle - opening

    # Bocais curtos com parede anular nas duas faces de extremidade.
    zc, yc = p["port_z"], W / 2
    inlet = Pos(-port_len, yc, zc) * Rot(0, 90, 0) * Cylinder(
        port_outer_d / 2, port_len + 3, align=(Align.CENTER, Align.CENTER, Align.MIN))
    outlet = Pos(L - 3, yc, zc) * Rot(0, 90, 0) * Cylinder(
        port_outer_d / 2, port_len + 3, align=(Align.CENTER, Align.CENTER, Align.MIN))
    body += inlet + outlet
    # Cut a 16 mm bore through the walls, collars and baffle transfer zones.
    bore_len = L + 2 * port_len + 4
    bore = Pos(-port_len - 1, yc, zc) * Rot(0, 90, 0) * Cylinder(
        port_d / 2, bore_len, align=(Align.CENTER, Align.CENTER, Align.MIN))
    body -= bore

    # Tampa plana removível com três furos de enchimento/purga sobre câmaras.
    lid_t = p["cover_thickness"]
    cover = Pos(0, 0, H) * Box(L, W, lid_t,
        align=(Align.MIN, Align.MIN, Align.MIN))
    vent_d = p["vent_diameter"]
    for cx in (L / 6, L / 2, 5 * L / 6):
        hole = Pos(cx, W / 2, H + lid_t / 2) * Cylinder(vent_d / 2, lid_t + 0.2,
            align=(Align.CENTER, Align.CENTER, Align.CENTER))
        cover -= hole
    return {"body": body, "cover": cover}
