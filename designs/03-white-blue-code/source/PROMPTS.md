# 白浅蓝代码渐变 · 生成与修改提示词

工具：内置 image_gen。下文是首批图制作丰富代码纹样与侧向 EECS 时使用的实际提示词，要求保留空白胸部。该阶段原图现保存在 `symbols/reference-original.png`；当前 `base.png` 已更新为下文记录的 v2。

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

## 2026-10-19 · v2 符号编辑工程

贡献者：@GhostJjaaxx。本次改版先用内置 `image_gen` 辅助清理旧印花，再通过本地脚本整理可继续修改的图层与固定排布。清理底图已经保存，日常渲染不再依赖提示词或 AI 生成。

底图清理提示词要点（整理）：以首批 1536 × 1024 白浅蓝正反面图为编辑目标；去除两件上衣的浅蓝小符号和前身大 EECS，恢复白色织物，保持原服装轮廓、皱褶、缝线、领口、光影、背景与画面尺寸。背部 `PKU EECS` 和 `PLAYER NAME` 保持原拼写、位置、形状和颜色；不添加 logo 或裤子。生成结果只在原印花清理蒙版内合成，其余部分沿用原图。

- 保留原图为 `symbols/reference-original.png`，保存清理后的 `blank-garment.png` 与清理范围记录 `cleanup-mask.png`。
- 保留 EECS 的原颗粒纹理和 C/S 字形，仅补两个 E 的底横。透明大字保存为 `lettering.png`，原轮廓与补笔记录保存为 `lettering-layout.json`。
- 将小符号替换为真实的代码与数学文本，固定在 `symbols-layout.json` 中：1,150 项排布、168 种文本片段、105 种字符。前图右侧与背图左侧对应同一穿着者左侧；背部原两行字保持不变。
- 固定使用 Source Code Pro Regular 2.038，并随工程保存字体及 OFL 许可。Node 渲染器生成可编辑文字 SVG、转曲 SVG、透明符号 PNG，以及按底图 → 符号 → 大字顺序内嵌的 `master.svg`。
- 日常修改以已保存的 JSON 和图层为准。运行命令、依赖版本与检查方式见[符号工程教程](symbols/README.md)；历史 Python 构建脚本仅供追溯初稿过程，不能直接覆盖后续手改排布。

当前 `preview.png` 与 `base.png` 使用 v2 无胸标成图。图中的代码和数学片段用于纹样，仍需结合实际印制尺寸检查可读性；混合位图与矢量的概念工程不等同于生产稿。
