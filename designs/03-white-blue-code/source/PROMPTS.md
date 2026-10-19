# 白浅蓝代码渐变 · 生成与修改提示词

工具：内置 image_gen。下文是制作丰富代码纹样与侧向 EECS 时使用的实际提示词，要求保留空白胸部，输出作为当前 base.png。

```text
Use case: precise-object-edit.
Input image 1 is the EDIT TARGET: the latest white/powder-blue PKU EECS badminton jersey front/back concept, with a sideways hidden EECS in the front image-right pattern and an EMPTY front image-left chest. Refine the graphics while preserving both shirt silhouettes, the white round neck, white base fabric, same restrained light-blue palette, front/back framing, lighting, general left-to-right gradient and back wording.

CHANGE 1 — richer MICRO CODE PATTERN:
Replace the predominantly brackets-and-binary texture with varied miniature programming fragments of comparable tiny size. Use a tasteful mix of "int x;", "if(x)", "for(i)", "def f", "return", "a[i]", "x+=1", "0x1F", "&&", "!=", "1010", "i++", plus some braces and angle brackets. Mix individual short snippets with very small blocks of 2–3 short monospace lines. Short variable assignments, keywords, indexing, loops, hexadecimal and arithmetic should all be represented. Brackets are no longer the majority. Keep every code fragment SMALL, pale and subtle; don't enlarge keywords into a slogan. Codes form a loose granular scattered texture, irregular lengths and spacing, not dense long source listings. Apply this richer code vocabulary to both front and back patterned areas while preserving the existing asymmetrical gradient placement and lots of white space.

CHANGE 2 — improve the hidden front EECS typography:
The four large letter shapes currently form a sideways word down the front image-right torso. Redesign them as ONE compact, carefully kerned word "EECS" in a bold slightly condensed SPORTY ITALIC sans serif, with a gentle 10–12 degree forward italic lean when read normally. Make each letter about 15–20 percent larger and reduce the inter-letter gaps substantially, so the word feels cohesive and purposeful. Leave small clear gaps so the two E letters do not merge; use optical kerning and an aligned baseline. Fit the word comfortably between upper torso and lower hem. Do not stretch it into the neckline or onto the sleeve.
CRITICAL ORIENTATION: start from normal left-to-right horizontal italic "EECS", then rotate the ENTIRE WORD CLOCKWISE 90 degrees and place it down the right side. Top-to-bottom remains E,E,C,S, EACH rotated clockwise 90 degrees. C opens downward in the normal front view. Rotating the whole front garment COUNTERCLOCKWISE 90 degrees must reveal a normal, properly oriented italic word "EECS" from left to right. No upright stacked letters, no mirroring, no reversed letter order.
The large EECS is STILL formed by a slightly deeper and denser field of tiny code fragments, with fragmented soft edges and visible white pores through each letter stroke. Do not replace it with solid opaque type. Keep it muted medium powder-blue, the same general contrast level as the input; do not turn it navy. The italic silhouette and tighter spacing must be noticeable but the overall shirt stays light.

EMPTY CHEST: leave the front IMAGE-LEFT upper chest entirely blank for an original robot team logo to be pasted later. Do NOT draw any logo, robot, shuttle, mascot, badge, brand or other chest graphic. The future dark logo will be the small dark accent; no dark accents added elsewhere.
BACK: preserve exactly two lines "PKU EECS" and "PLAYER NAME" in their existing position and muted blue, accurately spelled. Keep back text typography unchanged; only enrich the small surrounding pattern as described.
No other modifications. Preserve the 1536x1024 landscape composition.
```

机器人胸标由另行提供的原图提取并叠加，不在这段提示词中生成。当前默认配置关闭胸标；如需添加，可使用统一脚本的 -WithLogo。以 base.png 为输入继续编辑时，只需描述本次需要改变的部分；AI 重新生成不保证逐像素复现。
