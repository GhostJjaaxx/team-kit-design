# 01 · 炭灰琥珀橙

![炭灰琥珀橙队服正反面](preview.png)

| 项目 | 内容 |
| --- | --- |
| 初始提交者 | [@GhostJjaaxx](https://github.com/GhostJjaaxx)，负责选定并提供首批图片 |
| 原始设计署名 | 待补充；初始提交者不等同于全部素材的原作者 |
| 贡献者 | 待后续 PR 补充 |
| 方案状态 | 起始概念稿，讨论中 |
| 衍生自 | 既有炭灰与琥珀橙电路风格探索；本仓库以本次选定附件为起点 |
| 制作材料 | 已附底图、独立透明队徽、合成配置和提示词；暂无 PSD/AI/SVG 分层工程 |

## 设计想法

以炭灰为主色，琥珀橙点缀领口、肩线和侧身，袖口与下摆使用电路线条。正面胸部留白，背面使用白色 `PKU EECS` 和琥珀橙 `PLAYER NAME`。

可以继续探索胸标位置、电路线条密度、橙色对比度和背面文字比例。图中姓名为占位，最终印制内容另定。

## 文件清单

| 文件 | 用途 |
| --- | --- |
| [preview.png](preview.png) | 正反面概念效果图，1536 × 1024，按提供的附件原样保存 |
| [source/base.png](source/base.png) | 无胸标底图，供继续编辑与合成 |
| [source/lion-v6.png](source/lion-v6.png) | 可选独立透明队徽 |
| [source/composition.json](source/composition.json) | 队徽位置、大小及默认关闭的叠加配置 |
| [source/PROMPTS.md](source/PROMPTS.md) | 设计提示词 |
| [source/SOURCE.md](source/SOURCE.md) | 原始材料来源与制作过程 |

按[修改教程](../../docs/EDITING.md)运行合成脚本，可以调整或替换胸标。当前 `preview.png` 保持无胸标原稿；试做结果默认保存到 `generated/01-charcoal-amber/`，确认后再更新预览并提交 PR。底图中的文字、纹样和面料质感未独立分层。

## 素材与来源

- 图片来源：仓库负责人于 2026-10-19 选定的第一张附件。
- AI 辅助情况：通过内置 `image_gen` 工具制作的概念效果图；本次补充本地保存的底图、独立素材与提示词，详见 [SOURCE.md](source/SOURCE.md)。
- 图案与字体的完整作者、授权及生产适用范围：待确认。
- 当前材料支持位图编辑和胸标叠加，尚无分层工程、矢量图或印花生产稿。

## 变更记录

| 日期 | 贡献者 | 修改内容 |
| --- | --- | --- |
| 2026-10-19 | @GhostJjaaxx | 选定并原样收录首批方案，建立说明与迭代入口 |
| 2026-10-19 | @GhostJjaaxx | 补充底图、独立队徽、合成配置、提示词与来源说明，保留首批预览原样 |

## 后续版本

- [v02 · @wangtongyue-pku](../01-charcoal-amber-v02-wangtongyue-pku/README.md)：保留炭灰与琥珀橙配色，调整电路线条和斜向运动纹样，加入羽毛球胸部图案。[查看新版预览](../01-charcoal-amber-v02-wangtongyue-pku/preview.png)。本目录的预览与源文件保留原样。
