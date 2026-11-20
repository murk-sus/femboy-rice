#!/usr/bin/env python3
"""Узор темы на клавиатуре EVision 320F:505B через OpenRGB SDK. Аргумент: rgb.json темы."""
import json, sys
from openrgb import OpenRGBClient
from openrgb.utils import RGBColor
spec = json.load(open(sys.argv[1]))
P = {k: tuple(v) for k, v in spec["palette"].items()}; ART = spec["rows"]
c = OpenRGBClient("127.0.0.1", 6742, "rice-kbd")
dev = next(d for d in c.devices if "EVision" in d.name)
dev.set_mode("Custom")
z = dev.zones[0]
cols = [RGBColor(*P[spec.get("bg", ART[0][0])])] * len(z.leds)
for r, row in enumerate(z.matrix_map):
    for col, idx in enumerate(row):
        if idx is not None and idx < len(cols) and r < len(ART) and col < len(ART[r]):
            cols[idx] = RGBColor(*P[ART[r][col]])
z.set_colors(cols)
print("ok: узор на клавиатуре")
