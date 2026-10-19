# 修改现有设计

三个方案的 `source/` 都保存了底图、独立胸标、合成配置、提示词及来源说明。你可以直接调整胸标，也可以在图像编辑器或 AI 图像工具中继续修改底图，再通过 PR 分享。

首批 `preview.png` 是无胸标的选定效果图，保持原样。合成脚本默认输出到 `generated/`，先查看效果，再决定是否更新公开预览。

## 先认识这些文件

| 文件 | 用途与限制 |
| --- | --- |
| `source/base.png` | 无胸标底图；衣服轮廓、文字、纹样和质感已经合成在一张图片中 |
| `source/lion-v6.png` | 前两款的独立透明队徽，可选叠加 |
| `source/robot-navy.png` | 白浅蓝款的独立透明机器人胸标，可选叠加 |
| `source/robot-original.jpg` | 白浅蓝款机器人胸标的参考原图，用于追溯来源 |
| `source/composition.json` | 底图路径、胸标路径、坐标、大小和默认启用状态 |
| `source/PROMPTS.md` | 设计提示词，供继续编辑或生成时参考；不保证重复生成完全相同的图片 |
| `source/SOURCE.md` | 材料来源和制作过程说明 |

这些是可继续加工的位图材料，尚无 PSD、AI、SVG 等分层工程。合成脚本只叠加胸标，不能单独修改底图中的姓名、衣服纹样或文字；需要使用图像编辑工具、AI 编辑，或重新绘制相应部分。最终印花生产稿需另行制作。

## 本地生成预览

需要 Windows，以及 Windows PowerShell 5.1 或 PowerShell 7。脚本使用 `System.Drawing`，没有额外的 Python 或 Node 依赖。打开 PowerShell，进入仓库根目录，运行以下命令。

按原样输出炭灰款底图：

```powershell
& .\scripts\render-design.ps1 -Design 01-charcoal-amber
```

默认生成 `generated/01-charcoal-amber/preview.png`。三款的配置都将胸标设为默认关闭；以下命令为奶油白款生成带队徽的比较图：

```powershell
& .\scripts\render-design.ps1 -Design 02-cream-burgundy -WithLogo
```

白浅蓝款使用机器人胸标：

```powershell
& .\scripts\render-design.ps1 -Design 03-white-blue-code -WithLogo
```

默认输出文件已经存在时，脚本会停止，避免意外覆盖。确认重做时添加 `-Force`，或用 `-OutputPath` 指定另一个文件：

```powershell
& .\scripts\render-design.ps1 -Design 01-charcoal-amber -WithLogo -OutputPath .\generated\01-charcoal-amber\with-logo.png
& .\scripts\render-design.ps1 -Design 01-charcoal-amber -WithLogo -Force
```

如果 Windows 阻止执行下载的脚本，请先检查脚本内容，再按你的电脑或学校的执行策略处理，无需为本仓库全局修改执行策略。

## 调整胸标

编辑对应方案的 `source/composition.json`。例如炭灰款：

```json
{
  "base": "base.png",
  "overlay": {
    "enabled": false,
    "file": "lion-v6.png",
    "x": 452,
    "y": 203,
    "width": 186,
    "height": 190
  }
}
```

`base` 和 `file` 指向该方案 `source/` 中的文件。坐标单位为像素，原点是整张底图左上角：`x` 向右增大，`y` 向下增大，`width` 和 `height` 是胸标绘制尺寸。调整尺寸时尽量保持原始宽高比，避免胸标变形。

默认 `enabled: false` 保留无胸标效果，运行时加 `-WithLogo` 可临时启用胸标。若决定把胸标作为方案的默认组成部分，再将 `enabled` 改为 `true`，并在 PR 中说明。更换素材时，把新素材放入 `source/`，更新 `file`，并补充来源说明。

## 修改配色、文字或纹样

1. 打开 `source/base.png`，参考 `source/PROMPTS.md` 继续编辑。使用 AI 工具时同时提供底图和具体修改要求。
2. 将确认后的新底图保存为真正的 PNG；需要比较的版本先放进 `previews/` 或本地 `generated/`。
3. 保留原方案的贡献者与来源记录。新增素材、工具和提示词写入相应说明；来源或授权不确定时标注“待确认”。
4. 如果画布尺寸发生变化，同步调整胸标坐标与尺寸，重新运行合成命令检查效果。

白浅蓝款的 `robot-original.jpg` 带有“豆包 AI”标记；透明胸标来自对参考图的线条提取。它们的完整作者、授权和生产适用范围仍待确认，不应把参考图或提取结果直接声明为原创。

## 把确认的结果提交为 PR

先按[投稿教程](../CONTRIBUTING.md)创建自己的分支。打开生成图片，检查正反面、胸标透明边缘、文字和尺寸；确认要让它成为方案新首图后，手动复制：

```powershell
Copy-Item -LiteralPath .\generated\01-charcoal-amber\preview.png -Destination .\designs\01-charcoal-amber\preview.png
```

将示例路径替换为自己的方案与实际输出文件。同步更新该方案 `README.md` 的变更记录，并提交相关 `source/` 材料。`generated/` 只是本地试做目录，不应作为投稿内容提交。

PR 中附修改前后的预览，说明改了什么、为什么改，以及使用的命令或编辑工具。若修改了脚本，运行受影响方案的默认与带胸标合成，并检查已有文件的覆盖保护，将结果写进 PR。合并流程仍按仓库约定进行评审。
