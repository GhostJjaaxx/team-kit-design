# 奶油白酒红 v02 · 制作材料与来源

本目录从 PR #3 的完整方案副本迁移。原 PR 提交：`e2ba141ba16e539dc099301eaf768ed773e3fe17`；父版目录：[designs/02-cream-burgundy/](../../02-cream-burgundy/README.md)；原始目标分支基线：`44c05a5334981224ed1ad8425428aa8527af5860`。

- `pr3-artwork.png`：PR #3 中 `designs/02-cream-burgundy/preview.png` 的逐字节副本，包含本版服装、文字、纹样和羽毛球图案；未作图像修改。
- `composition.json`：默认输入改为 `pr3-artwork.png`，关闭额外胸标，默认输出与本版预览一致。胸标位置参数继承父版，未经新版校准，不是新版羽毛球图案的制作参数。
- `base.png` 及全部独立素材：从父版原样继承，用于参考与继续探索，不是生成本版纹样的分层源文件。
- `composition-parent.json`：父版原合成配置的逐字节副本；其 `base.png` 路径在本目录内仍有效。
- `SOURCE-parent.md`：父版来源原文的逐字节副本，描述父版材料。
- `PROMPTS.md`：父版历史提示词原文，描述父版 `base.png`，不是本版实际提示词。

原 PR 声明使用 ChatGPT 辅助构思与图像生成，未提供本版生成提示词、独立羽毛球图案、字体或分层工程。现有新版材料支持平面位图编辑；不能单独修改已合成的文字和纹样，不能凭历史提示词确定性地重新生成。具体素材署名与授权仍待确认；父版原记录见 [SOURCE-parent.md](SOURCE-parent.md)。

在仓库根运行 `./scripts/render-design.ps1 -Design 02-cream-burgundy-v02-wangtongyue-pku`，输出到 `generated/02-cream-burgundy-v02-wangtongyue-pku/preview.png`，默认原样复制本版位图。继续设计时遵循[版本规则](../../../docs/VERSIONING.md)，不回写父版本。
