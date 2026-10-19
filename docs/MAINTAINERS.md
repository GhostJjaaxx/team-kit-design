# 仓库维护说明

仓库：<https://github.com/GhostJjaaxx/team-kit-design>。归属个人账号 `GhostJjaaxx`，其他设计成员使用 collaborator 身份参与。

## 邀请同学

1. 收集同学的 GitHub 用户名。
2. 仓库负责人打开 **Settings → Collaborators → Add people**，核对账号后发送邀请。
3. 同学接受邀请后即可创建分支、提交设计、评审和合并 PR。

个人仓库不能设置多位 owner。若将来需要多人管理仓库设置，可迁移到 Organization 并设置适合的仓库角色。

## main 分支规则

管理员按以下要求配置保护规则，当前生效的设置可在 GitHub **Settings → Branches** 中查看：

- 所有变更通过 PR 合并。
- 至少 1 位非作者、具有写入权限的成员批准。
- 新提交导致旧批准失效，需要重新评审。
- 合并前解决所有评审对话。
- 规则适用于管理员，禁止直接推送、强制推送及删除 `main`。

初始内容由负责人首次提交后再开启保护。在第一位协作者接受邀请前，负责人自己的 PR 会等待其他有写入权限的成员评审。

## 日常收录

- 对照 PR 模板检查预览、说明、来源、贡献记录和实际源文件状态。
- 合并只是候选库收录，不是最终采用决定。
- 推荐 squash merge，一次方案变更形成一条记录；合并后可自动删除已合并的工作分支。
- 纯图片设计不要求代码 CI；修改合成脚本或配置时需实际运行并检查输出，结果记录在 PR 中。设计评审在 PR 中完成；二进制冲突由贡献者明确选择版本。

## GitHub 文档

- [个人仓库的权限](https://docs.github.com/en/account-and-profile/reference/permission-levels-for-a-personal-account-repository)
- [受保护分支](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
