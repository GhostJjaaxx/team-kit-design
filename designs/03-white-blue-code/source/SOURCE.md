# 制作材料与来源

本目录包含当前 v2 成图、独立胸标、合成参数、原始提示词，以及 [symbols/](symbols/README.md) 中可复现的符号编辑工程。工程将衣服底图、真实字符符号与颗粒大字分开，兼有矢量和位图材料，不是全矢量成衣生产稿。

| 文件 | 内容与来源 |
| --- | --- |
| `base.png` | 当前 v2 的无胸标成图，与方案预览对应，供胸标合成脚本使用 |
| `robot-navy.png` | 从用户提供的机器人图中提取线条后改为深海军蓝 `#25445C` 的透明胸标 |
| `robot-original.jpg` | 原始机器人参考图片，保留原有“豆包 AI 生成”标记 |
| `composition.json` | 可编辑合成参数；默认关闭胸标，保持当前无胸标方案 |
| `PROMPTS.md` | 首批图的内置 image_gen 提示词，以及 v2 的底图清理与固定符号制作记录 |
| `symbols/reference-original.png` | 首批“机器人胸标／丰富代码 v14”无胸标原图，保留以供比对 |
| `symbols/blank-garment.png` | 固定的清理底图，保留服装形状、明暗及原背部两行字 |
| `symbols/cleanup-mask.png` | 清理范围记录，供检查原图与清理底图的区别；不参与日常渲染 |
| `symbols/lettering.png` | 独立透明 EECS 颗粒大字；保留原 C/S 与大字纹理，仅补两个 E 的底横 |
| `symbols/lettering-layout.json` | 原字形轮廓与补笔参数的过程记录；日常渲染直接使用已保存的 `lettering.png` |
| `symbols/symbols-layout.json` | 1,150 项固定真实文本及其位置、尺寸、颜色、透明度、旋转与裁切区域 |
| `symbols/fonts/` | 未修改的 Source Code Pro Regular 2.038、来源说明和 OFL 许可 |
| `symbols/symbols-text.svg` | 可编辑文字版符号，内嵌固定字体 |
| `symbols/symbols-outlined.svg` | 已转曲的符号路径 |
| `symbols/symbols.png` | 透明符号层，1536 × 1024 |
| `symbols/master.svg` | 内嵌分层总图，从底到顶依次为清理底图、转曲符号、大字位图 |
| `symbols/report.json` | 输入/输出 SHA-256、文本数量及渲染环境记录 |

[统一合成脚本](../../../scripts/render-design.ps1) 根据原 `composite-robot.ps1` 的透明胸标缩放与叠加部分整理，使用仓库相对路径。独立透明胸标已预先生成，可直接替换成其他透明 PNG，不依赖原图的临时文件路径。

原始胸标处理记录：从 `robot-original.jpg` 取像素矩形 `x=342, y=392, width=594, height=520`，以亮度估算透明度，再将线条设为 `#25445C`；原脚本中亮度为 `0.2126R + 0.7152G + 0.0722B`，透明度为 `round(max(0, (248 - 亮度) × 255 / 248))`。生成的透明图在当前材料中原样保存。

v2 的小符号从原 AI 纹理改为可编辑的代码与数学文本，当前共 168 种文本片段、105 种字符。前图右侧与背图左侧对应穿着者左侧，原背部的 `PKU EECS`、`PLAYER NAME` 保持不变。原大字中的 C/S 仍是位图，两个 E 的补笔也沿用原颗粒纹理；没有将整套图案声明为矢量。

日常使用 [Node 渲染器](../../../scripts/render-white-blue.cjs)读取固定 JSON 与图片，不重新随机排布、不调用 AI、不依赖 Python。已记录的环境为 Node v24.19.0、`@napi-rs/canvas` 0.1.100 和 `sharp` 0.35.5，依赖由锁文件固定；字节级复现还需要相同的运行环境，详见 `symbols/report.json`。

[历史初稿构建脚本](../../../scripts/build-white-blue-layout.py)记录了从原图提取轮廓、补笔和构建排布的过程，记录环境为 Python 3.12.14、Pillow 12.3.0、NumPy 2.3.5。它会重建大字和排布材料；日常修改不要运行它覆盖已手工编辑的 JSON。

清理底图由内置 `image_gen` 辅助去除原蓝色印花，再仅在 `cleanup-mask.png` 标记的像素范围内与原图合成，保护领口与背部两行字。该步骤没有放进 Python 构建脚本；清理结果已固定保存为 `blank-garment.png`，日常复现直接读取它，无需再次调用 AI。符号和 E 的补笔由本地脚本制作。

原始图案及参考素材的完整作者、授权与生产适用范围仍待确认。新增字体的来源及 OFL 许可保存在 [fonts/](symbols/fonts/SOURCE.md)，该字体许可不扩展为整套队服设计的授权。当前画布为 1536 × 1024 的正反面概念图，尚需另行制作成衣纸样与印花文件。

操作步骤见[符号工程教程](symbols/README.md)；可选胸标的叠加方法见[通用修改指南](../../../docs/EDITING.md)。
