# 修改现有设计

**先完整复制已有方案到新的同级目录，再编辑新副本。** 已收录版本中的预览、源图、字体和配置都要保留。新目录首次合并前，可在同一 PR 中反复修改；首次合并后，再次迭代需要另建目录。完整要求见[版本保留规则](VERSIONING.md)。

旧方案目录中的工程教程用于说明原版本的制作方法，可能带有默认旧路径。迭代时以本教程的新目录命令为准，不要把结果回写父版本。仅查看旧版的复现结果时，可以继续输出到本地 `generated/`。

## 先认识这些文件

| 文件 | 用途与限制 |
| --- | --- |
| `source/base.png` | 无胸标底图；轮廓、文字、纹样和质感合成在一张图中 |
| `source/lion-v6.png` / `source/robot-navy.png` | 可选叠加的独立透明胸标 |
| `source/composition.json` | 底图、胸标、坐标、大小和默认启用状态 |
| `source/PROMPTS.md` | 历史提示词，不保证再次 AI 生成得到相同图片 |
| `source/SOURCE.md` | 材料来源和制作过程 |

当前三款提供位图底图和独立透明素材，尚无可单独编辑衣服文字和纹样的分层工程。修改底图需要图像编辑工具或重新绘制相应部分；最终生产仍需厂家纸样与规格。

## 第一步：复制完整版本

先保存当前未提交工作，再按[投稿教程](../CONTRIBUTING.md)同步目标分支、创建自己的工作分支。如果已经有会覆盖旧版的 PR，请先看[迁移步骤](VERSIONING.md#已有-pr-会覆盖旧版怎么办)，避免丢失现有修改。

在仓库根目录打开 PowerShell。下面以白浅蓝为例，将 `yourname` 换成自己的 GitHub 用户名的小写形式；也可以选择其他父版本：

```powershell
$parentDesign = '03-white-blue-code'
$newDesign = '03-white-blue-code-v02-yourname'
$newDesignPath = Join-Path .\designs $newDesign
if (Test-Path -LiteralPath $newDesignPath) {
    throw "目标目录已存在，请换一个唯一名称：$newDesignPath"
}
Copy-Item -LiteralPath (Join-Path .\designs $parentDesign) -Destination $newDesignPath -Recurse
git rev-parse origin/main
```

该命令复制整个目录，不是只复制预览。核对新目录包含旧版全部素材和说明后，再修改其中的文件。把输出的完整提交 SHA、父版本路径及链接和本次版本标签写入新目录 `README.md`，保留原作者及贡献记录。Fork 的目标远程如果叫 `upstream`，使用 `git rev-parse upstream/main`。

后文继续使用 `$newDesign` 和 `$newDesignPath`；若换了 PowerShell 窗口，请重新设置这两个变量。

## 第二步：编辑新版本

### 位图或胸标

只编辑 `$newDesignPath/source/` 中的材料。更换底图时保存为真正的 PNG，保留来源记录；画布尺寸改变后同步调整胸标坐标。PowerShell 合成需要 Windows PowerShell 5.1 或 PowerShell 7，使用系统的 `System.Drawing`。

```powershell
& .\scripts\render-design.ps1 -Design $newDesign
```

默认输出到 `generated/<新目录名>/preview.png`，不会自动覆盖方案预览。需要比较带胸标效果时：

```powershell
& .\scripts\render-design.ps1 -Design $newDesign -WithLogo -OutputPath ".\generated\$newDesign\with-logo.png"
```

默认存在输出文件时会停止。确认重做后添加 `-Force`，或换一个 `-OutputPath`。脚本只叠加胸标，不会修改底图中的姓名、文字或纹样。

`source/composition.json` 中的坐标以底图左上角为原点，单位为像素：`x` 向右、`y` 向下，`width` 和 `height` 为胸标尺寸。默认 `enabled: false` 保留无胸标效果；`-WithLogo` 可临时启用。素材和配置路径都相对于新版本的 `source/`，不要改成父版本路径。

## 第三步：检查并同步新目录

打开生成图片，检查正反面、边缘、文字、渐变和 EECS。确认效果后，将输出复制到**新目录**：

```powershell
Copy-Item -LiteralPath ".\generated\$newDesign\preview.png" -Destination (Join-Path $newDesignPath 'preview.png')
```

以上命令会更新尚未合并的新副本，不应将 `$newDesignPath` 设为父版本。新副本中保留用于生成预览的底图、独立素材和配置；不要把带胸标的成图回写成底图，以免再次合成时重复叠加。`generated/` 仅为本地试做目录，不提交。新版本 README 中记录实际使用的编辑命令、来源和变更，并修正复制过来但仍指向旧目录的命令。

在首页图库追加新版本预览及说明链接，保留旧版入口。可以在旧版根 `README.md` 增加“后续版本”链接，不能改动旧目录中的其他文件。所有相对链接都要实际打开检查。

## 第四步：检查并提交 PR

```powershell
git fetch origin main
python scripts/check-design-versions.py --base origin/main
```

默认检查本地工作目录，包括尚未跟踪的新文件；只检查已提交内容可加 `--head HEAD`。目标分支已有新提交时，先保存工作、合并最新目标分支并解决冲突，再检查。Fork 按目标远程名改用 `upstream/main`。

自动检查通过后仍要打开 PNG、核对完整源文件和链接。按[PR 模板](../.github/pull_request_template.md)附新旧预览、父版本、版本标签、基线 SHA、生成命令及结果。如果修改了合成脚本，应实际检查受影响方案的默认输出、带胸标输出和覆盖保护。只提交本次新目录及必要文档、工具变更，不提交旧设计素材的覆盖。
