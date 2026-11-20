#!/usr/bin/env python3
"""NERV / Eva-02 узор на клавиатуре EVision 320F:505B через OpenRGB SDK (сервер на 127.0.0.1:6742)."""
from openrgb import OpenRGBClient
from openrgb.utils import RGBColor
P = {
 'H': (255, 70, 0),    # волосы
 'C': (255, 0, 0),     # заколки A10
 'S': (255, 160, 110), # кожа
 'E': (0, 80, 255),    # глаза
 'R': (255, 0, 12),    # плагсьют / Ева-02
 'G': (0, 255, 40),    # зелёные элементы
 'O': (255, 110, 0),   # NERV orange
 'D': (40, 0, 2),      # тёмно-красный фон
 'K': (0, 0, 0),
}
# абстрактный узор в палитре Евы-02: полосы предупреждения NERV | красный корпус с зелёной линией | градиент
def _art():
    rows = []
    for r in range(6):
        left = "".join("O" if (c + r) % 4 < 2 else "K" for c in range(8))
        mid = "G" * 7 if r in (2, 3) else "R" * 7
        right = "".join("RRHOOOO"[min(6, max(0, c + r - 2))] for c in range(7))
        rows.append(left + "D" + mid + right)
    return rows
ART = _art()
assert all(len(r) == 23 for r in ART)
c = OpenRGBClient("127.0.0.1", 6742, "asuka-kbd")
dev = next(d for d in c.devices if "EVision" in d.name)
dev.set_mode("Custom")
z = dev.zones[0]
cols = [RGBColor(*P['D'])] * len(z.leds)
for r, row in enumerate(z.matrix_map):
    for col, idx in enumerate(row):
        if idx is not None and idx < len(cols):
            cols[idx] = RGBColor(*P[ART[r][col]])
z.set_colors(cols)
print("ok: узор NERV/Eva-02 на клавиатуре")
