# 白浅蓝 v2 · 符号编辑工程

这里把衣服底图、小符号和 EECS 大字分开，便于继续改字、调位置和复现效果。当前小符号有 **1,150 项排布、168 种文本片段、105 种字符**，全部使用真实文本与固定字体。日常渲染只读取保存的 JSON 和图层，不随机排布、不调用 AI，也不需要 Python。

画布是 1536 × 1024 的正反面效果图。前图右侧和背图左侧对应穿着者左侧；背面的 `PKU EECS` 与 `PLAYER NAME` 保持原样。EECS 保留原颗粒纹理，两个 E 仅补底横，C/S 仍为原位图。此工程包含矢量符号和位图图层，并非全矢量图或成衣纸样。

## 文件与图层

| 文件 | 用途 |
| --- | --- |
| [reference-original.png](reference-original.png) | 首批原图，用于对照与追溯 |
| [blank-garment.png](blank-garment.png) | 已固定的清理底图，保留服装明暗和背部两行字 |
| [cleanup-mask.png](cleanup-mask.png) | 原纹样清理范围记录，不参与日常渲染 |
| [lettering.png](lettering.png) | 独立透明 EECS 颗粒大字，作为最上层叠加 |
| [lettering-layout.json](lettering-layout.json) | 原字形轮廓与 E 补笔参数的过程记录；不会由日常渲染器重新构建大字 |
| [symbols-layout.json](symbols-layout.json) | 固定文本和排布，是日常修改的主要输入 |
| [fonts/SourceCodePro-Regular.ttf](fonts/SourceCodePro-Regular.ttf) | 固定 Source Code Pro Regular 2.038 字体，无需安装到系统 |
| [fonts/SOURCE.md](fonts/SOURCE.md) · [fonts/LICENSE.md](fonts/LICENSE.md) | 字体来源、SHA-256 及 SIL OFL 1.1 许可 |
| [symbols-text.svg](symbols-text.svg) | 真实文字版符号，内嵌字体，便于在支持 SVG 文字的工具中查看和编辑 |
| [symbols-outlined.svg](symbols-outlined.svg) | 转曲符号层，文字已变为路径，接收方无需安装字体 |
| [symbols.png](symbols.png) | 透明符号层，1536 × 1024 |
| [master.svg](master.svg) | 内嵌图层的独立总图：`blank-garment` → `outlined-symbols` → `lettering` |
| [report.json](report.json) | 数量统计、输入/输出 SHA-256、字体和渲染环境 |

`master.svg` 将底图和大字作为内嵌 PNG，将符号作为转曲路径。它可以单独打开查看完整效果；直接改动导出的 SVG 不会自动同步回 JSON，下次运行渲染器也不会读取这些改动。需要可复现修改时，请以 JSON 和独立图层为准。

## 按当前材料复现

从仓库根目录运行：

```shell
npm ci --prefix scripts/white-blue-renderer
node scripts/render-white-blue.cjs
```

渲染依赖已由 `scripts/white-blue-renderer/package-lock.json` 锁定。记录环境为 **Node v24.19.0、@napi-rs/canvas 0.1.100、sharp 0.35.5**。渲染器读取本目录的固定字体，不依赖系统字体；完整平台与底层库版本见 `report.json`。要比较字节级 SHA-256，请使用相同的运行环境与输入文件。

默认输出到 `generated/white-blue-symbols/`，包含 `symbols-text.svg`、`symbols-outlined.svg`、`symbols.png`、`master.svg`、`preview.png` 和 `report.json`，不会自动替换仓库预览。已有同名输出时脚本停止；确认重新生成后运行：

```shell
node scripts/render-white-blue.cjs --force
```

也可将试做结果保存到另一目录：

```shell
node scripts/render-white-blue.cjs --output-dir generated/white-blue-tryout
```

## 修改一个符号

在 `symbols-layout.json` 的 `items` 数组中找到目标项。例如：

```json
{
  "id": "code-0001",
  "text": "<<",
  "x": 556.653,
  "y": 108.107,
  "fontSize": 8.37,
  "fill": "#72B4DB",
  "opacity": 0.659,
  "rotate": 2.096,
  "scaleX": 1.0,
  "strokeWidth": 0.07,
  "clip": "front"
}
```

| 字段 | 如何修改 |
| --- | --- |
| `id` | 每项唯一标识；新增项使用新的标识，不与已有项重复 |
| `text` | 要显示的真实文本片段；更换后检查字体覆盖和显示宽度 |
| `x` / `y` | 文本基线起点，单位像素；原点是整张画布左上角，向右/向下增大 |
| `fontSize` | 字号，单位为画布像素 |
| `fill` / `opacity` | 颜色和透明度；通过不同透明度控制疏密渐变，透明度范围 0–1 |
| `rotate` / `scaleX` | 旋转角度和水平缩放；小幅调整可呼应衣服曲面 |
| `strokeWidth` | 同色描边宽度，用于调整细线显示效果 |
| `clip` | `front` 或 `back`，对应顶层 `clipPaths` 中的衣服裁切区域 |

新增项复制现有结构后修改 `id` 和内容；删除项直接从数组移除。保持合法 JSON，不添加注释或多余尾逗号。更改长文本后检查重叠和裁切。渲染器会检查字符支持情况，遇到不支持的字符会报错，不会静默替换为系统字体。

固定排布意味着每次渲染使用相同位置。更改清理底图或大字时，要保留 1536 × 1024 画布，并让 `lettering.png` 保持透明通道。修改 `lettering-layout.json` 只是更新过程记录，日常渲染仍使用已保存的 `lettering.png`；两者需要有意同步维护。

## 检查并更新方案

1. 运行渲染器，在完整图和放大图中检查符号、裁切、衣服边缘与大字颗粒，确认前后纹样都对应穿着者左侧。
2. 对比新的 `report.json`。未修改输入且环境一致时，可核对输出 SHA-256；有意改动 JSON 或图层后，哈希变化是预期结果。数量变化也应与新增、删除的项目对应。
3. 确认效果后，将生成的 `preview.png` 同步复制到方案的 `preview.png` 和 `source/base.png`。将生成的两份符号 SVG、`symbols.png`、`master.svg` 和 `report.json` 同步回本目录，确保导出文件与源配置一致。
4. 在方案 [README](../../README.md) 补充变更记录，在 PR 中附修改前后效果与运行命令，提交 JSON、相关图层、导出文件和说明。`generated/` 为本地试做目录，不提交。

如果需要机器人胸标，在更新后的 `source/base.png` 上按[通用修改教程](../../../../docs/EDITING.md)使用 PowerShell 合成。胸标是独立的可选素材，不在上述符号渲染器的输出中。

## 历史初稿构建过程

[build-white-blue-layout.py](../../../../scripts/build-white-blue-layout.py) 保留排布构建过程，记录环境为 Python 3.12.14、Pillow 12.3.0、NumPy 2.3.5。它从原图提取大字材料、补全 E 并生成排布，会写入工程文件；不会重建清理底图。**日常编辑不要运行该脚本覆盖已保存的 JSON 和图层。** 正常复现只运行上文 Node 渲染器。

首批 AI 概念图和机器人素材的来源见 [SOURCE.md](../SOURCE.md)，历史提示词及 v2 改版记录见 [PROMPTS.md](../PROMPTS.md)。字体 OFL 许可仅针对字体，不代表整套队服设计已获得同样授权；生产前仍需确认其他素材及实际印制尺寸。
