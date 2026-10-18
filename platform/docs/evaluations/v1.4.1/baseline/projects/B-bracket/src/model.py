"""Suporte de parede com carro removível em guia vertical."""
from build123d import Align, Box, Cylinder, Pos, Rot


def build(params):
    p = params["mount"]
    plate_w = float(p["plate_width"])
    plate_h = float(p["plate_height"])
    plate_t = float(p["plate_thickness"])
    hole_x = float(p["wall_hole_pitch_x"])
    hole_y = float(p["wall_hole_pitch_vertical"])
    hole_r = float(p["wall_hole_diameter"]) / 2
    projection = float(p["shelf_projection"])
    clearance = float(p["guide_clearance"])
    rail_center, rail_width, wall_width = 14.0, 4.0, 1.6
    rail_left = -rail_center - rail_width / 2
    rail_right = rail_center - rail_width / 2
    carriage_outer_left = rail_left - clearance - wall_width
    carriage_inner_left = rail_left + rail_width + clearance
    carriage_inner_right = rail_right - clearance - wall_width
    carriage_outer_right = rail_right + rail_width + clearance
    # Datum da construção local: face posterior em Z=0, eixo vertical Y.
    plate = Box(plate_w, plate_h, plate_t, align=(Align.CENTER, Align.CENTER, Align.MIN))
    # Furos passantes genéricos Ø5.5 para parafusos, 70 x 50 mm. Fixação à
    # parede requer seleção de bucha/parafuso após identificação do substrato.
    for x in (-hole_x / 2, hole_x / 2):
        for y in (-hole_y / 2, hole_y / 2):
            plate -= Pos(x, y, 0) * Cylinder(hole_r, plate_t, align=(Align.CENTER, Align.CENTER, Align.MIN))

    # Guia central estreita, extrudada verticalmente no plano da placa.
    # Dois trilhos laterais de 4 mm e uma alma traseira definem canal aberto.
    plate += Pos(rail_left, -29, plate_t) * Box(rail_width, 58, 6, align=(Align.MIN, Align.MIN, Align.MIN))
    plate += Pos(rail_right, -29, plate_t) * Box(rail_width, 58, 6, align=(Align.MIN, Align.MIN, Align.MIN))
    # Batente transversal inferior: impede que o carro saia por gravidade para
    # baixo; manutenção continua sendo feita levantando-o pela extremidade livre.
    carriage_outer_left = rail_left - clearance - wall_width
    carriage_outer_right = rail_right + rail_width + clearance
    plate += Pos(carriage_outer_left, -31, plate_t) * Box(
        carriage_outer_right + wall_width - carriage_outer_left, 2.4, 6,
        align=(Align.MIN, Align.MIN, Align.MIN))

    # Carro em U: a travessa fica à frente dos trilhos; quatro paredes formam
    # canais laterais com folga de 0,4 mm sem interseção com os trilhos.
    carriage = Pos(carriage_outer_left, -28.6, plate_t + 6 + clearance) * Box(
        carriage_outer_right + wall_width - carriage_outer_left, 57.2, 4,
        align=(Align.MIN, Align.MIN, Align.MIN))
    for x in (carriage_outer_left, carriage_inner_left, carriage_inner_right, carriage_outer_right):
        carriage += Pos(x, -28.6, plate_t + clearance) * Box(wall_width, 57.2, 6, align=(Align.MIN, Align.MIN, Align.MIN))
    # Prateleira horizontal: X=largura, Y=espessura vertical, Z=projeção da parede.
    web_z = plate_t + 6 + clearance
    carriage += Pos(-25, -2.5, web_z + 4) * Box(50, 5, projection, align=(Align.MIN, Align.MIN, Align.MIN))
    # Duas nervuras diagonais distribuem a flexão da prateleira para o carro.
    rib_angle = -26.6
    for x in (-12.5, 12.5):
        carriage += Pos(x, -10.25, web_z + 4 + projection / 2) * Rot(rib_angle, 0, 0) * Box(4, 4, projection + 5)
    # Rasgos de amarração simplificados como furos passantes Ø5, espaçados.
    for x in (-16, 16):
        carriage -= Pos(x, 0, web_z + projection * 0.75) * Rot(90, 0, 0) * Cylinder(2.5, 7)
    # Envelope montado: 100 x 80 x 46,4 mm.
    # Produto montado: Z vertical, X largura, Y projeção para fora da parede.
    # A rotação posiciona a placa no plano XZ e a plataforma horizontal X/Y.
    return {"wall_plate": Rot(90, 0, 0) * plate,
            "removable_carriage": Rot(90, 0, 0) * carriage}
