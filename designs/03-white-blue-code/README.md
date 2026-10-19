# 03 · 白浅蓝代码渐变

![白浅蓝代码渐变队服正反面](preview.png)

| 项目 | 内容 |
| --- | --- |
| 初始提交者 | [@GhostJjaaxx](https://github.com/GhostJjaaxx)，负责选定并提供首批图片 |
| 原始设计署名 | 待补充；初始提交者不等同于全部素材的原作者 |
| 贡献者 | 待后续 PR 补充 |
| 方案状态 | 起始概念稿，讨论中 |
| 衍生自 | 既有白浅蓝代码渐变探索；本仓库以本次选定附件为起点 |
| 制作材料 | 已附底图、独立透明机器人胸标、合成配置和提示词；暂无 PSD/AI/SVG 分层工程 |

## 设计想法

白色圆领与主体搭配浅蓝色代码碎片，在正面图像右侧形成由密到疏的纹样，并组成侧向 `EECS`。背面使用浅蓝色 `PKU EECS` 与 `PLAYER NAME`，代码纹样呼应正面。

可以继续探索代码纹样的疏密和可读性、侧向字形、胸标位置与印花对比度。微小字符目前是概念纹理，并非已校对的代码或生产稿。

## 文件清单

| 文件 | 用途 |
| --- | --- |
| [preview.png](preview.png) | 正反面概念效果图，1536 × 1024，按提供的附件原样保存 |
| [source/base.png](source/base.png) | 无胸标底图，供继续编辑与合成 |
| [source/robot-navy.png](source/robot-navy.png) | 可选独立透明机器人胸标 |
| [source/robot-original.jpg](source/robot-original.jpg) | 胸标参考原图，保留来源线索 |
| [source/composition.json](source/composition.json) | 胸标位置、大小及默认关闭的叠加配置 |
| [source/PROMPTS.md](source/PROMPTS.md) | 设计提示词 |
| [source/SOURCE.md](source/SOURCE.md) | 原始材料来源与制作过程 |

按[修改教程](../../docs/EDITING.md)运行合成脚本，可以调整或替换胸标。当前 `preview.png` 保持无胸标原稿；试做结果默认保存到 `generated/03-white-blue-code/`，确认后再更新预览并提交 PR。底图中的文字、纹样和面料质感未独立分层。

## 素材与来源

- 图片来源：仓库负责人于 2026-10-19 选定的第三张附件。
- AI 辅助情况：通过内置 `image_gen` 工具制作的概念效果图；本次补充本地保存的底图、独立素材与提示词，详见 [SOURCE.md](source/SOURCE.md)。
- 机器人参考原图带有“豆包 AI”标记，透明胸标来自对原图的线条提取；参考图与提取结果不据此声明为原创。
- 图案与字体的完整作者、授权及生产适用范围：待确认。
- 当前材料支持位图编辑和胸标叠加，尚无分层工程、矢量图或印花生产稿。

## 变更记录

| 日期 | 贡献者 | 修改内容 |
| --- | --- | --- |
| 2026-10-19 | @GhostJjaaxx | 选定并原样收录首批方案，建立说明与迭代入口 |
| 2026-10-19 | @GhostJjaaxx | 补充底图、机器人胸标及参考原图、合成配置、提示词与来源说明，保留首批预览原样 |

## 后续版本

- [v02 · @wangtongyue-pku](../03-white-blue-code-v02-wangtongyue-pku/README.md)：延续白蓝方向，采用蓝色 V 领、斜向运动线条、像素与网格纹样，加入羽毛球图案；新版未沿用原版侧向 EECS 与密集微代码字形。[查看新版预览](../03-white-blue-code-v02-wangtongyue-pku/preview.png)。本目录的预览与源文件保留原样。
