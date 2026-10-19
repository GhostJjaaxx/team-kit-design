# PKU EECS · 队服共创

一起设计我们的新队服。欢迎从现有方案继续打磨，也欢迎提出全新的设计。

**参与方式：新建分支 → 上传设计 → 提交 Pull Request → 讨论与评审 → 合并收录。**

[如何提交设计](CONTRIBUTING.md) · [修改现有设计](docs/EDITING.md) · [设计说明模板](templates/design/README.md) · [查看 PR](https://github.com/GhostJjaaxx/team-kit-design/pulls) · [讨论想法](https://github.com/GhostJjaaxx/team-kit-design/issues)

## 首批设计

以下三张是 2026-10-19 选定的起始效果图，原样收录；每个方案都可以独立迭代。点击图片查看完整尺寸。

| 01 · 炭灰琥珀橙 | 02 · 奶油白酒红 | 03 · 白浅蓝代码渐变 |
| :---: | :---: | :---: |
| [![炭灰琥珀橙正反面](designs/01-charcoal-amber/preview.png)](designs/01-charcoal-amber/preview.png) | [![奶油白酒红正反面](designs/02-cream-burgundy/preview.png)](designs/02-cream-burgundy/preview.png) | [![白浅蓝代码渐变正反面](designs/03-white-blue-code/preview.png)](designs/03-white-blue-code/preview.png) |
| [方案说明](designs/01-charcoal-amber/README.md) | [方案说明](designs/02-cream-burgundy/README.md) | [方案说明](designs/03-white-blue-code/README.md) |
| 深色底、琥珀橙线条、电路元素 | 浅色底、酒红线条、电路元素 | 白色底、浅蓝代码纹样、侧向 EECS |

三款现已附上原始底图、独立胸标、合成配置和设计提示词，可以调整胸标的位置与大小，或继续编辑底图。[修改教程](docs/EDITING.md)提供了可直接运行的命令。首批三张 `preview.png` 保持原样，均不带胸标；胸标是可选素材。

这些材料是平面图片与合成素材，尚无 PSD、AI、SVG 等分层工程；衣服文字、纹样和质感仍在底图中。图案用于讨论，印花生产稿需另行制作。背面的 `PLAYER NAME` 为姓名占位。

## 你可以做什么

- **迭代已有方案：** 修改对应 `designs/<方案>/`，更新预览和说明，保留原作者与变更记录。
- **新增或独立衍生方案：** 复制设计说明模板到新的方案目录，附 `preview.png`；衍生设计写清来源。
- **参与讨论：** 在 PR 中提出具体修改建议，或开 Issue 讨论配色、版型、队徽与印花。

PR 合并代表收录进候选方案库，不代表已经确定最终队服。未完成的设计也可以先提交 Draft PR 交流。

## 文件怎么放

```text
designs/
  01-charcoal-amber/       炭灰琥珀橙
  02-cream-burgundy/       奶油白酒红
  03-white-blue-code/      白浅蓝代码渐变
templates/design/         新方案说明模板
scripts/render-design.ps1  本地合成底图与可选胸标
.github/                  PR 模板
CONTRIBUTING.md            网页与 Git 投稿步骤
docs/EDITING.md            素材说明与本地修改教程
docs/MAINTAINERS.md        成员与审核管理说明
```

每个方案至少包含 `README.md` 和 `preview.png`。补充视图放入 `previews/`，底图、独立素材、合成配置或分层工程放入 `source/`，在说明中写清文件类型和编辑能力。脚本默认将试做结果输出到 `generated/`；确认后再更新方案预览并提交 PR。沿用固定文件路径，旧版本可从 Git 历史中查看。

## 成员与审核

仓库由 [@GhostJjaaxx](https://github.com/GhostJjaaxx) 管理。有兴趣参与的同学把 GitHub 用户名发给仓库负责人，接受 collaborator 邀请后即可在仓库内建分支、提交和评审 PR。尚未加入的同学也可以通过 fork 提交 PR。

团队约定：所有设计变更通过 PR，至少由一位非作者、有写入权限的成员批准，并解决评审讨论后再合并。平台规则由仓库管理员配置，详见[维护说明](docs/MAINTAINERS.md)。

## 素材说明

首批图片由仓库负责人选定并提供，属于通过内置 `image_gen` 工具制作的 AI 辅助概念设计。各方案的 `source/SOURCE.md` 记录补充素材的来源，`source/PROMPTS.md` 保存设计提示词。原始设计与素材的完整署名、授权状态仍待确认；新增素材也请注明来源及授权状态。仓库暂未指定开源许可证，公开展示不等于授予任意使用或商用许可。
