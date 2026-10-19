# 炭灰琥珀橙 · 生成与修改提示词

工具：内置 image_gen。下文保留此前实际使用的英文提示词，作为继续编辑的参考。

## 第一阶段：原始配色探索

这一阶段的提示词包含攻城狮胸标。当前 base.png 采用第二阶段的无胸标底图；若只想调整现有方案，可直接以 base.png 为输入描述修改内容，无需重新执行全部历史步骤。

```text
Use case: precise-object-edit
Asset type: alternative harmonious colorway for the Peking University EECS badminton team jersey, full front/back presentation.

Input image 1 is the BASE GARMENT DESIGN to preserve: its athletic V neck, raglan cut, ergonomic side panels, sparse printed circuit paths on sleeves/lower sides, angular side accents, fabric texture, front-left/back-right layout, garment size, grey studio backdrop, lighting and framing.
Input image 2 is the CURRENT EXACT ENGINEERING-LION EMBLEM. Use this emblem in place of the older one on the source garment. Treat it as fixed supplied print artwork. Preserve its complete silhouette, BOTH articulated elbows and current upper/forearm proportions, raised non-racket paw, bent legs, cute yellow lion/orange mane, head-top duck, red cape, green waveform, blue racket and single shuttlecock. No reinterpreting the logo into another pose, no recoloring it. Same compact wearer's-left-chest placement (viewer right on front), roughly 8–9 cm tall.
Primary request: change the garment colorway as specified below to harmonize tastefully with the colorful emblem. Keep the electric-circuit motif and sporting structure. The garment palette must be restrained so the emblem is the focal point. Printed circuit traces remain crisp and visible but are secondary, located only at sleeve edges and lower sides; do not cross the emblem or back lettering.
Preserve EXACTLY TWO lines on the upper back: "PKU EECS" large bold slightly condensed athletic sans-serif, and "PLAYER NAME" smaller uppercase beneath it. Keep spelling, positions, line spacing, size hierarchy and alignment. No sponsor logo, numbers, slogans or additional garment text.
Retain the small labels "FRONT" and "BACK" under the garments. Show both complete jerseys with all sleeves and hems visible, same scale as source. Premium matte breathable fabric with natural subtle dimensionality, clean light-grey studio background and soft shadows. No extra panels, swatches, large background mascot or page headings.

COLORWAY: CHARCOAL AND MUTED AMBER, a clean competitive technical sports mood. Main body and sleeves charcoal grey #25292D, not pure black. Side mesh panels slightly lighter graphite #3B4248. Collar edging, shoulder piping and narrow side angular accents warm muted amber #D7993E. Circuit traces mainly medium slate grey #626970 with a few selected thin amber paths and nodes. First back line "PKU EECS" warm white #F4F0E7; second "PLAYER NAME" muted amber #D7993E. Limit amber to about 5–10% of the visible garment; it subtly echoes the orange mane without competing with the bright yellow lion. Preserve the unchanged full-color emblem and add only a very fine warm-white perimeter keyline if needed on dark fabric. No flame patterns, neon colors, red side panels or massive orange blocks.
```

## 第二阶段：清除原胸标，得到当前底图

```text
Use case: precise-object-edit
Prepare a clean garment mockup for subsequent placement of a supplied print asset.
Edit ONLY the small printed chest emblem area on the FRONT jersey, which is the left jersey in this image and the viewer's RIGHT side of its chest.
Completely REMOVE the entire small colorful lion badge, its red cape, blue racket, separate small white shuttlecock above-left, white/dark perimeter outlines and every part of that chest illustration. Fill that area with clean uninterrupted fabric matching the exact local garment color, lighting, subtle folds and fine weave. Do not leave a ghost outline, color stain, rectangular patch, blurred patch or embroidery residue. The entire upper chest should now be blank fabric.
Everything else must remain identical: both jersey silhouettes, collar, sleeves, seams, shadows, colors, circuit paths, side panels, all fabric outside the small removed-emblem region, gray backdrop, framing, and the two views. Preserve the BACK lettering exactly: "PKU EECS" above "PLAYER NAME". Preserve "FRONT" and "BACK" beneath the garments.
Do not insert a replacement emblem, text, mark or any new object. Output the same-size complete front/back product image with only the old chest emblem cleanly removed.
```

后续可使用仓库合成脚本叠加独立 lion-v6.png，位置与尺寸由 composition.json 控制。AI 重新生成会产生变化，提示词不保证逐像素复现。
