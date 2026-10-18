"""Suporte de parede com placa e carreador deslizante removível; dimensões em mm."""
from build123d import Align, Box, Cylinder, Polygon, Pos, Rot, extrude


def build(params):
    p = params["mount"]
    w, h, t = p["plate_width"], p["plate_height"], p["plate_thickness"]
    z0, z1 = p["rail_z0"], p["rail_z1"]
    wn, wh, rd = p["rail_neck_width"], p["rail_head_width"], p["rail_depth"]
    clr = p["slide_clearance"]
    cw = p["carrier_width"]
    by, bd = p["carrier_back_y"], p["carrier_back_depth"]
    cz0, cz1 = p["carrier_z0"], p["carrier_z1"]
    td, tt, tz = p["tray_depth"], p["tray_thickness"], p["tray_z"]
    lip = p["side_lip"]
    if min(w, h, t, wn, wh, rd, clr, cw, bd, td, tt, lip) <= 0:
        raise ValueError("Todas as dimensões e folgas devem ser positivas")
    if wh <= wn or z1 <= z0 or cw >= w:
        raise ValueError("Geometria do trilho ou dimensões incompatíveis")

    # Base vertical encostada à parede (plano y=0); trilho macho em cauda-de-andorinha.
    plate = Box(w, t, h, align=(Align.CENTER, Align.MIN, Align.MIN))
    # Quatro rasgos verticais para acomodar variação de padrão; fixadores definidos após medir parede.
    slot_radius = 2.8
    slot_low, slot_high = 10.0, h - 10.0
    for x in (-30.0, 30.0):
        for z in (slot_low, slot_high):
            cutter = Pos(x, t/2, z) * Rot(90, 0, 0) * Cylinder(
                slot_radius, t + 2.0, align=(Align.CENTER, Align.CENTER, Align.CENTER)
            )
            plate = plate - cutter
        bridge = Pos(x, -1.0, (slot_low+slot_high)/2) * Box(
            slot_radius*2, t+2.0, slot_high-slot_low,
            align=(Align.CENTER, Align.MIN, Align.CENTER)
        )
        plate = plate - bridge
    rail_section = Polygon(
        (-wn/2, t), (wn/2, t), (wh/2, t+rd), (-wh/2, t+rd), align=None
    )
    rail = Pos(0, 0, z0) * extrude(rail_section, amount=z1-z0)
    wall_plate = plate + rail

    # Painel do carreador. Canal fêmea é maior que o macho pela folga nominal.
    panel = Pos(0, by, cz0) * Box(cw, bd, cz1-cz0,
                                  align=(Align.CENTER, Align.MIN, Align.MIN))
    half_base = wn/2 + clr
    half_head = wh/2 + clr
    # Estende o canal para além das extremidades do perfil, evitando faces de tampa.
    channel = Polygon(
        (-half_base, t-0.5), (half_base, t-0.5),
        (half_head, t+rd+0.5), (-half_head, t+rd+0.5), align=None
    )
    groove = Pos(0, 0, cz0-0.5) * extrude(channel, amount=cz1-cz0+1.0)
    carrier_back = panel - groove

    # Bandeja com abas laterais baixas, para apoio; dimensões do equipamento são desconhecidas.
    tray = Pos(0, by+bd-0.2, tz) * Box(cw, td, tt,
                                      align=(Align.CENTER, Align.MIN, Align.MIN))
    lip_height = 8.0
    lip_x = cw/2 - lip/2
    left_lip = Pos(-lip_x, by+bd-0.2, tz+tt) * Box(lip, td, lip_height,
                                                    align=(Align.CENTER, Align.MIN, Align.MIN))
    right_lip = Pos(lip_x, by+bd-0.2, tz+tt) * Box(lip, td, lip_height,
                                                    align=(Align.CENTER, Align.MIN, Align.MIN))
    equipment_carrier = carrier_back + tray + left_lip + right_lip
    return {"wall_plate": wall_plate, "equipment_carrier": equipment_carrier}
