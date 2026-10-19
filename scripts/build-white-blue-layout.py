# Name: QiuCheng Zhen
# Nickname: HuangXiaoYunMeiMei WoXiHuanNi
# ID: 2400012917

"""Build the editable, frozen code-print layout; normal rendering uses the saved JSON."""

from collections import deque
import json
import math
from pathlib import Path
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "designs/03-white-blue-code/source/symbols"
WIDTH, HEIGHT = 1536, 1024
SEED = 20261019

TOKENS = {
    "types": ["int n;", "bool ok;", "float x;", "double y;", "char c;", "uint8_t", "auto v;", "void f()", "size_t", "const T", "enum E", "struct S"],
    "flow": ["if(x)", "else{}", "for(i)", "while(x)", "break;", "return;", "switch(n)", "case 0:", "try{}", "catch(e)", "yield x", "def f(x)", "in range", "do{}"],
    "arithmetic": ["x+=1;", "n-=1;", "i++;", "j--;", "x*y", "a/b", "n%2", "x<<1", "y>>2", "a&b", "a|b", "a^b", "~x", "x+y", "a-b", "x**2", "x//=2"],
    "compare": ["x==0", "a!=b", "x<=n", "y>=0", "x>0", "k<n", "a&&b", "p||q", "!ok", "is None", "x in A"],
    "data": ["a[i]", "v[j]", "buf[k]", "map[k]", "set(x)", "len(a)", "push(x)", "pop()", "head->x", "p->y", "a.b", "vec<T>", "arr[N]", "q.front", "s.size"],
    "functions": ["f(x)", "g(y)", "sum(v)", "min(a,b)", "max(x,y)", "sqrt(x)", "abs(x)", "log(n)", "sin(x)", "cos(y)", "pow(x,2)", "sort(a)", "FFT(x)", "BFS(g)", "DFS(g)", "hash(k)", "zip(a,b)"],
    "syntax": ["{x}", "[i]", "(x+y)", "<T>", "::", "// code", "/* */", "x?y:z", "@fn", "#define", "a:=b", "x=>y", "{k:v}", "a[0:n]", "(a,b)", "()", "[]", "{}", "&&", "||", "!=", "<=", ">=", "++", "--", "->", "<<", ">>", "**", "+=", "-=", "0x", "x", "n", "i", "j"],
    "literals": ["0x1F", "0xFF", "0b1010", "1e-3", "3.14", "true", "false", "null", "'A'", '"EECS"', "NaN", "0x2A", "1024", "256", "64bit"],
    "mathematics": ["α+β", "λ(x)", "π*r^2", "∑x", "∏n", "∫f(x)", "∂f", "∞", "√n", "a≤b", "x≥0", "a≠b", "x≈y", "a≡b", "A∩B", "∀x", "∃y", "¬p", "x→y", "a←b", "x↔y", "p⇒q", "x×y", "a÷b", "±x", "μ=0", "σ=1", "δx", "γ(t)", "Σx", "Πn"],
}

FRONT = "M137 166 L289 103 L293 116 L311 151 L339 171 L391 185 L451 182 L500 164 L529 135 L535 104 L685 164 L718 221 L750 321 L779 407 L651 452 L633 405 L623 529 L628 694 L657 917 Q418 968 165 918 L195 750 L207 620 L207 556 L193 425 L180 338 L157 238 Z"
BACK = "M853 166 L1001 103 Q1120 118 1245 103 L1395 166 L1423 222 L1460 324 L1497 407 L1364 451 L1345 404 L1334 493 L1332 641 L1368 916 Q1125 969 888 917 L911 758 L921 632 L917 483 L906 404 L899 452 L766 408 L795 318 L824 221 Z"
LETTER_BOXES = {"E1": (500, 239, 640, 377), "E2": (491, 375, 635, 514), "C": (480, 510, 636, 678), "S": (473, 665, 644, 838)}


def largest_component(binary):
    seen = np.zeros_like(binary, dtype=bool)
    largest = []
    height, width = binary.shape
    for y, x in np.argwhere(binary):
        if seen[y, x]:
            continue
        queue = deque([(int(x), int(y))])
        seen[y, x] = True
        component = []
        while queue:
            px, py = queue.popleft()
            component.append((px, py))
            for nx, ny in ((px - 1, py), (px + 1, py), (px, py - 1), (px, py + 1)):
                if 0 <= nx < width and 0 <= ny < height and binary[ny, nx] and not seen[ny, nx]:
                    seen[ny, nx] = True
                    queue.append((nx, ny))
        if len(component) > len(largest):
            largest = component
    result = np.zeros_like(binary, dtype=bool)
    for x, y in largest:
        result[y, x] = True
    return result


def outline_path(binary, offset_x, offset_y):
    """Trace pixel-boundary loops, retaining the original C/S silhouettes."""
    height, width = binary.shape
    edges = {}
    for y, x in np.argwhere(binary):
        x, y = int(x), int(y)
        if y == 0 or not binary[y - 1, x]:
            edges[(x, y)] = (x + 1, y)
        if x == width - 1 or not binary[y, x + 1]:
            edges[(x + 1, y)] = (x + 1, y + 1)
        if y == height - 1 or not binary[y + 1, x]:
            edges[(x + 1, y + 1)] = (x, y + 1)
        if x == 0 or not binary[y, x - 1]:
            edges[(x, y + 1)] = (x, y)
    paths = []
    while edges:
        first = min(edges)
        point = first
        points = []
        while point in edges:
            points.append(point)
            point = edges.pop(point)
            if point == first:
                break
        if len(points) < 20:
            continue
        corners = []
        for index, current in enumerate(points):
            before = points[index - 1]
            after = points[(index + 1) % len(points)]
            if (current[0] - before[0], current[1] - before[1]) != (after[0] - current[0], after[1] - current[1]):
                corners.append(current)
        paths.append("M" + " L".join(f"{x + offset_x} {y + offset_y}" for x, y in corners) + " Z")
    return " ".join(paths)


def main():
    reference = np.array(Image.open(SOURCE / "reference-original.png").convert("RGB"), dtype=np.int16)
    blue = np.maximum(reference[:, :, 2] - reference[:, :, 0], 0).astype(np.uint8)
    blurred = np.asarray(Image.fromarray(blue).filter(ImageFilter.GaussianBlur(3.0)))
    clips = {"front": FRONT, "back": BACK}
    lettering_mask = Image.new("L", (WIDTH, HEIGHT))
    lettering_masks = {}
    for letter, (x0, y0, x1, y1) in LETTER_BOXES.items():
        crop = largest_component(blurred[y0:y1, x0:x1] > 43)
        mask = Image.fromarray((crop * 255).astype(np.uint8))
        # Preserve the approved mosaic ink, including its irregular edges.
        mask = mask.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(0.65))
        lettering_mask.paste(mask, (x0, y0))
        lettering_masks[letter] = outline_path(crop, x0, y0)

    original = Image.fromarray(reference.astype(np.uint8))
    lettering = original.convert("RGBA")
    lettering.putalpha(lettering_mask)
    repairs = []
    # Reuse the opposite E bar's original blue mosaic, avoiding a new visual style.
    # In this rotated word, the missing bottom bars are the right-hand uprights.
    for letter, y0, y1, source_x, target_x in [("E1", 253, 367, 511, 614), ("E2", 387, 505, 503, 606)]:
        repair_mask = Image.new("L", (WIDTH, HEIGHT))
        polygon = [(target_x, y0), (target_x + 18, y0 + 3), (target_x + 14, y1), (target_x - 5, y1)]
        ImageDraw.Draw(repair_mask).polygon(polygon, fill=255)
        repair_mask = repair_mask.filter(ImageFilter.GaussianBlur(0.55))
        shifted = Image.new("RGBA", (WIDTH, HEIGHT))
        dx = target_x - source_x
        shifted.paste(original.crop((0, 0, WIDTH - dx, HEIGHT)), (dx, 0))
        shifted.putalpha(repair_mask)
        lettering = Image.alpha_composite(lettering, shifted)
        repairs.append({"letter": letter, "sourceOffsetX": dx, "polygon": polygon, "featherRadius": 0.55})
    pixels = np.array(lettering)
    pixels[pixels[:, :, 3] == 0] = 0
    Image.fromarray(pixels).save(SOURCE / "lettering.png", optimize=True)
    (SOURCE / "lettering-layout.json").write_text(json.dumps({"reference": "reference-original.png", "contours": lettering_masks, "edgeExpansion": 4, "edgeFeather": 0.65, "repairs": repairs, "policy": "Preserve original C/S and E mosaic ink; only E bottom bars are extended using original texture."}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")

    rng = random.Random(SEED)
    vocabulary = [token for group in TOKENS.values() for token in group]
    used = []
    items = []
    counter = 0

    def token():
        nonlocal used
        if not used:
            used = vocabulary[:]
            rng.shuffle(used)
        return used.pop()

    def add(text, x, y, size, fill, opacity, rotation, clip, scale_x=1.0, stroke=0.0):
        nonlocal counter
        counter += 1
        items.append({"id": f"code-{counter:04d}", "text": text, "x": round(x, 3), "y": round(y, 3), "fontSize": round(size, 3), "fill": fill, "opacity": round(opacity, 3), "rotate": round(rotation, 3), "scaleX": round(scale_x, 3), "strokeWidth": stroke, "clip": clip})

    # Reuse the reference print's low-frequency density field, mirror only the rear positions.
    density_signal = np.minimum(np.maximum(blue.astype(np.int16) - 7, 0), 40).astype(np.uint8)
    density = np.asarray(Image.fromarray(density_signal).filter(ImageFilter.GaussianBlur(16.0)), dtype=float)
    for side in ("front", "back"):
        x_start, x_stop = (192, 780) if side == "front" else (766, 1370)
        for row, y in enumerate(np.arange(109.0, 934.0, 9.8)):
            x = x_start + rng.uniform(-8, 8)
            while x < x_stop:
                text = token()
                size = rng.uniform(6.8, 10.2)
                step = max(9, len(text) * size * 0.60 + rng.uniform(4, 9))
                sample_x = x if side == "front" else 2260 - x
                q = min(1.0, density[int(y), max(0, min(1535, int(sample_x)))] / 11.0)
                if side == "back":
                    q *= math.exp(-max(0, x - 1000) / 650)
                probability = q ** 0.8
                yy = y + rng.uniform(-1.3, 1.3)
                if rng.random() < probability:
                    xx = x + rng.uniform(-3, 3)
                    target_x = xx
                    if side == "back" and 985 < target_x + step and target_x < 1286 and 225 < yy < 349:
                        x += step
                        continue
                    if side == "front" and lettering_mask.getpixel((int(max(0,min(1535,xx))), int(yy))) > 20:
                        x += step
                        continue
                    opacity = (0.30 + 0.49 * q) * rng.uniform(0.80, 1.10)
                    rotation = rng.uniform(-5.0, 5.0)
                    if yy < 450 and ((side == "front" and xx > 648) or (side == "back" and xx < 908)):
                        rotation += -15 if side == "front" else 15
                    add(text, target_x, yy, size, "#72B4DB", min(0.86, opacity), rotation, side, stroke=0.07)
                x += step

    layout = {"width": WIDTH, "height": HEIGHT, "font": "fonts/SourceCodePro-Regular.ttf", "background": "blank-garment.png", "lettering": "lettering.png", "clipPaths": clips, "items": items, "metadata": {"version": 2, "date": "2026-10-19", "wearerSide": "left", "frontPrintedSide": "image-right", "backPrintedSide": "image-left", "coordinateOrigin": "top-left; text y is the baseline", "initialPlacementSeed": SEED, "replayPolicy": "Render this explicit item list; do not regenerate positions for normal reproduction.", "letterConstruction": "Original mosaic texture preserved in lettering.png; C/S unchanged, E bottom bars repaired. See lettering-layout.json.", "vocabulary": TOKENS}}
    (SOURCE / "symbols-layout.json").write_text(json.dumps(layout, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"Frozen {len(items)} text placements; vocabulary={len(vocabulary)}; clip paths={len(clips)}")


if __name__ == "__main__":
    main()
