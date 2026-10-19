# 03 · 白浅蓝代码渐变

![白浅蓝代码渐变队服正反面](preview.png)

| 项目 | 内容 |
| --- | --- |
| 初始提交者 | [@GhostJjaaxx](https://github.com/GhostJjaaxx)，负责选定并提供首批图片 |
| 原始设计署名 | 待补充；初始提交者不等同于全部素材的原作者 |
| 贡献者 | [@GhostJjaaxx](https://github.com/GhostJjaaxx)：整理来源与符号编辑工程 |
| 方案状态 | v2 可编辑符号概念稿，讨论中 |
| 衍生自 | 既有白浅蓝代码渐变探索；本仓库以本次选定附件为起点 |
| 制作材料 | 固定文本排布、可编辑/转曲 SVG、SVG 分层总图、位图底图与大字、可选机器人胸标 |

## 设计想法

白色圆领与主体搭配浅蓝色代码和数学符号，在正面图像右侧形成由密到疏的纹样，侧向 `EECS` 保留原图的颗粒质感。背面纹样对应图像左侧；正面图像右侧与背面图像左侧都对应穿着者左侧。背面原有的 `PKU EECS` 与 `PLAYER NAME` 两行字保持不变。

v2 将周围的小符号改为 1,150 项真实文本，含 168 种文本片段、105 种字符，可逐项编辑位置、大小、颜色、透明度和旋转。两个 E 仅补全底横，C/S 及其余大字保留原始位图纹理。符号是装饰用代码与数学片段，不构成完整可执行程序；1536 × 1024 效果图也不等同于成衣纸样或印花生产稿。

## 文件清单

| 文件 | 用途 |
| --- | --- |
| [preview.png](preview.png) | 当前 v2 正反面概念效果图，1536 × 1024，无胸标 |
| [source/base.png](source/base.png) | 与当前预览对应的无胸标成图，供可选胸标合成使用 |
| [source/symbols/README.md](source/symbols/README.md) | 符号工程的文件说明、编辑与复现教程 |
| [source/symbols/master.svg](source/symbols/master.svg) | 内嵌底图、转曲符号和颗粒大字的分层总图 |
| [source/symbols/symbols-text.svg](source/symbols/symbols-text.svg) | 真实可编辑文本版符号，内嵌固定字体 |
| [source/symbols/symbols-outlined.svg](source/symbols/symbols-outlined.svg) | 已转曲符号，可保持字形而无需接收方安装字体 |
| [source/symbols/symbols-layout.json](source/symbols/symbols-layout.json) | 固定 1,150 项文本与排布；日常修改的主要入口 |
| [source/symbols/reference-original.png](source/symbols/reference-original.png) | 首批原图，保留用于比对 |
| [source/robot-navy.png](source/robot-navy.png) | 可选独立透明机器人胸标 |
| [source/robot-original.jpg](source/robot-original.jpg) | 胸标参考原图，保留来源线索 |
| [source/composition.json](source/composition.json) | 胸标位置、大小及默认关闭的叠加配置 |
| [source/PROMPTS.md](source/PROMPTS.md) | 设计提示词 |
| [source/SOURCE.md](source/SOURCE.md) | 原始材料来源与制作过程 |

按[符号工程教程](source/symbols/README.md)运行 Node 渲染器，输出到 `generated/white-blue-symbols/`。日常渲染读取固定 JSON，不使用随机排布或 AI，也不需要 Python。确认效果后再同步 `preview.png`、`source/base.png` 与工程导出文件并提交 PR。

可选机器人胸标仍可按[通用修改教程](../../docs/EDITING.md)叠加；它不包含在当前 v2 预览中。SVG 总图按底图、符号、大字分层，衣服、背部两行文字与大字纹理仍含位图，并非全矢量设计。

## 素材与来源

- 图片来源：仓库负责人于 2026-10-19 选定的第三张附件。
- AI 辅助情况：首批概念图通过内置 `image_gen` 工具制作；v2 使用固定排布和脚本制作真实字符层，日常渲染不调用 AI。原图和改版来源见 [SOURCE.md](source/SOURCE.md)。
- 机器人参考原图带有“豆包 AI”标记，透明胸标来自对原图的线条提取；参考图与提取结果不据此声明为原创。
- 原图、图案及参考素材的完整作者、授权及生产适用范围：待确认。新增符号使用 Source Code Pro Regular 2.038，附有[字体来源](source/symbols/fonts/SOURCE.md)和 [OFL 许可](source/symbols/fonts/LICENSE.md)。
- 当前已有包含矢量符号的混合分层工程，尚非全矢量印花生产稿。

## 变更记录

| 日期 | 贡献者 | 修改内容 |
| --- | --- | --- |
| 2026-10-19 | @GhostJjaaxx | 选定并原样收录首批方案，建立说明与迭代入口 |
| 2026-10-19 | @GhostJjaaxx | 补充底图、机器人胸标及参考原图、合成配置、提示词与来源说明，保留首批预览原样 |
| 2026-10-19 | @GhostJjaaxx | v2：补全两个 E 的底横；保留 C/S 与原大字颗粒纹理；小符号改为固定真实文本排布；将背面纹样对应到穿着者左侧；补充字体、SVG 工程和可复现渲染材料，更新预览与胸标用底图 |
