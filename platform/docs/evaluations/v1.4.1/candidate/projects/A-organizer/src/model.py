"""Organizador modular: base com padrão de encaixe e três cestas abertas.

As cestas são volumes genéricos. Suas dimensões não representam ferramentas reais;
meça os objetos e ajuste o arquivo de parâmetros antes de validar capacidade.
"""
from build123d import Align, Box, Cylinder, Pos


def build(params):
    p = params["organizer"]
    length, width = p["base_length"], p["base_width"]
    base_t = p["base_thickness"]
    socket_depth = p["socket_depth"]
    pin_engagement = p["pin_engagement"]
    wall, floor_t = p["module_wall"], p["module_floor"]
    pitch = p["slot_pitch"]
    pin_offset, pin_r = p["pin_offset"], p["pin_radius"]
    clearance = p["socket_clearance"]
    cols, rows = p["slot_columns"], p["slot_rows"]
    if min(length, width, base_t, socket_depth, pin_engagement, wall, floor_t, pitch, pin_r) <= 0:
        raise ValueError("Dimensões devem ser positivas")
    if socket_depth >= base_t or pin_engagement > socket_depth:
        raise ValueError("O soquete precisa ser cego e acomodar o comprimento do pino")
    if clearance < 0:
        raise ValueError("A folga não pode ser negativa")

    base = Box(length, width, base_t,
               align=(Align.CENTER, Align.CENTER, Align.MIN))
    # Soquetes cegos localizam as cestas sem perfurar a face inferior da base.
    x0 = -(cols - 1) * pitch / 2
    y0 = -(rows - 1) * pitch / 2
    for col in range(cols):
        for row in range(rows):
            cx, cy = x0 + col * pitch, y0 + row * pitch
            for sx in (-pin_offset, pin_offset):
                for sy in (-pin_offset, pin_offset):
                    socket = Pos(cx + sx, cy + sy, base_t - socket_depth) * Cylinder(
                        pin_r + clearance, socket_depth,
                        align=(Align.CENTER, Align.CENTER, Align.MIN))
                    base -= socket

    def build_module(prefix):
        module_l = p[f"{prefix}_length"]
        module_w = p[f"{prefix}_width"]
        module_h = p[f"{prefix}_height"]
        if min(module_l, module_w, module_h) <= 0 or module_l <= 2 * wall or module_w <= 2 * wall:
            raise ValueError(f"Dimensões incompatíveis para {prefix}")
        if module_h <= floor_t or pin_offset + pin_r + clearance > min(module_l, module_w) / 2:
            raise ValueError(f"Pinos ou fundo incompatíveis para {prefix}")
        if (cols - 1) * pitch + module_l > length or (rows - 1) * pitch + module_w > width:
            raise ValueError(f"Matriz de módulos excede a base para {prefix}")
        # Cesta aberta com dimensões próprias por categoria.
        outer = Box(module_l, module_w, module_h,
                    align=(Align.CENTER, Align.CENTER, Align.MIN))
        inner = Pos(0, 0, floor_t) * Box(
            module_l - 2 * wall, module_w - 2 * wall, module_h,
            align=(Align.CENTER, Align.CENTER, Align.MIN))
        module = outer - inner
        # Alívios nas quatro faces permitem apoiar os dedos e pinçar ferramentas.
        notch_w, notch_h = p["grip_notch_width"], p["grip_notch_height"]
        if notch_w <= 0 or notch_h <= 0 or notch_w >= min(module_l, module_w) - 2 * wall or notch_h >= module_h:
            raise ValueError(f"Alívio de pega incompatível para {prefix}")
        for side in (-1, 1):
            notch = Pos(side * (module_l / 2 - wall / 2), 0, module_h - notch_h) * Box(
                wall + 1.0, notch_w, notch_h + 0.1,
                align=(Align.CENTER, Align.CENTER, Align.MIN))
            module -= notch
            notch = Pos(0, side * (module_w / 2 - wall / 2), module_h - notch_h) * Box(
                notch_w, wall + 1.0, notch_h + 0.1,
                align=(Align.CENTER, Align.CENTER, Align.MIN))
            module -= notch
        for sx in (-pin_offset, pin_offset):
            for sy in (-pin_offset, pin_offset):
                pin = Pos(sx, sy, -pin_engagement) * Cylinder(
                    pin_r, pin_engagement, align=(Align.CENTER, Align.CENTER, Align.MIN))
                module += pin
        return module

    return {"base": base,
            "module_a": build_module("category_a"),
            "module_b": build_module("category_b"),
            "module_c": build_module("category_c")}
