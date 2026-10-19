# 仓库维护说明

仓库：[GhostJjaaxx/team-kit-design](https://github.com/GhostJjaaxx/team-kit-design)。个人账号 `GhostJjaaxx` 为 owner，其他设计成员使用 collaborator 身份参与。

## 邀请同学

1. 收集同学的 GitHub 用户名。
2. 仓库负责人打开 **Settings → Collaborators → Add people**，核对账号后发送邀请。
3. 同学接受后可创建分支、提交设计及参与评审。

个人仓库不能设置多位 owner。若将来需要多人管理仓库设置，可考虑迁移到 Organization。

## main 分支与必需检查

管理员应在仓库的分支规则或 Rulesets 中为 `main` 配置以下条件，并以 GitHub 中实际生效的设置为准：

- 所有变更通过 PR 合并。
- 至少一位非作者、具有写入权限的成员批准；新增提交使旧批准失效。
- 合并前解决所有评审对话。
- 要求通过状态检查 **保留设计历史**，并启用 **Require branches to be up to date before merging**（要求分支在合并前与目标分支同步）。
- 规则适用于管理员，禁止直接推送、强制推送及删除 `main`，不留常规绕过入口。

版本检查工作流是 [.github/workflows/design-version-history.yml](../.github/workflows/design-version-history.yml)，检查脚本是 [scripts/check-design-versions.py](../scripts/check-design-versions.py)。工作流使用 `pull_request` 事件和只读仓库权限，对照运行时获取的目标分支当前版本检查 PR 内容。

**把文件写在本地不会启用 GitHub 保护。** 先将规则和工作流正常提交到远程，确认检查成功运行，再由管理员把 **保留设计历史** 加入 `main` 的必需状态检查，同时开启上述分支同步选项。目标分支有新提交时，先前通过的检查可能已过期；不能省略同步要求。PR 页面上应能看到检查结果，并且检查未通过时无法正常合并。不要把仅有文档约定或一次绿色运行当作已开启强制保护。

脚本检查旧方案素材是否被更改、添加、删除或移动；旧方案根 README 允许更新但不能删除。新目录需要常规 README 和具有 PNG 文件签名的预览。PNG 签名不是完整图像解码验证，审核人仍要打开图片。源文件完整性、图库链接和版本来源也需要人工检查。对修改工作流或检查脚本的 PR，审核人应检查这些修改本身；此工作流不是不可篡改的保护机制。

## 日常收录

- 按[版本规则](VERSIONING.md)要求迭代新增完整同级目录。旧预览和全部源文件保留，不能只依靠 Git 历史。
- 对照 PR 模板检查父版本路径及链接、版本标签、基线 SHA、新旧预览和来源记录。打开新目录核对源图、字体、图层与配置，不只看截图。
- 检查首页保留旧版入口并追加新版入口。旧版根 README 可添加新版导航或纠正来源，但不能借此移除旧版的有效说明与来源记录。
- 检查依据是目标分支的当前版本。如果目标分支已前进，要求贡献者同步，再检查；手工填写的旧基线 SHA 不能免除对后来已收录版本的保护。
- 现有 PR 如覆盖原文件，先按[迁移步骤](VERSIONING.md#已有-pr-会覆盖旧版怎么办)将完整修改另存为新版本，再恢复旧版内容。迁移前保护未提交工作，不执行盲目批量恢复。
- 合并只是候选库收录，不是最终采用决定。可使用 squash merge，合并后删除工作分支；版本目录仍保留在 `main` 中。
- 修改脚本或配置时需实际运行并检查图片，在 PR 中记录结果。二进制冲突由贡献者在新版本中整理，不删除已收录版本来消除冲突。

初始内容首次提交后再开启分支保护。在第一位有写入权限的协作者参与前，负责人的 PR 也可能需要等待其他成员审核。

## GitHub 文档

- [个人仓库的权限](https://docs.github.com/en/account-and-profile/reference/permission-levels-for-a-personal-account-repository)
- [受保护分支](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
