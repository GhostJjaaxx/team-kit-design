# Name: QiuCheng Zhen
# Nickname: HuangXiaoYunMeiMei WoXiHuanNi
# ID: 2400012917

"""Integration tests for append-only design proposals using disposable Git repos."""

from pathlib import Path
import os
import shutil
import subprocess
import sys
import tempfile
import unittest


CHECKER = Path(__file__).resolve().parents[1] / "scripts" / "check-design-versions.py"
PNG = bytes.fromhex(
    "89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c489"
    "0000000b49444154789c636000020000050001a5f645400000000049454e44ae426082"
)


class DesignVersionsTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="design-versions-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.git("init", "-q")
        self.git("config", "user.name", "Design Test")
        self.git("config", "user.email", "design-test@example.invalid")
        self.git("config", "core.autocrlf", "false")
        self.make_design("01-original")
        (self.root / ".gitignore").write_text("generated/\n", encoding="utf-8")
        self.commit("Initial design")
        self.base = self.git("rev-parse", "HEAD").strip()

    def git(self, *args):
        result = subprocess.run(
            ["git", "-C", str(self.root), *args],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True,
        )
        return result.stdout.decode("utf-8")

    def commit(self, message):
        self.git("add", "-A")
        self.git("commit", "-q", "-m", message)

    def make_design(self, name):
        directory = self.root / "designs" / name
        (directory / "source").mkdir(parents=True)
        (directory / "README.md").write_text("# Design\n", encoding="utf-8")
        (directory / "preview.png").write_bytes(PNG)
        (directory / "source" / "art.svg").write_text("<svg/>\n", encoding="utf-8")
        return directory

    def check_result(self, expected=0, *args):
        result = subprocess.run(
            [sys.executable, str(CHECKER), "--base", self.base, *args],
            cwd=self.root, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        )
        output = (result.stdout + result.stderr).decode("utf-8")
        self.assertEqual(result.returncode, expected, output)
        return output

    def test_clean_worktree_and_committed_head_pass(self):
        self.check_result()
        self.check_result(0, "--head", "HEAD")

    def test_new_variant_with_copied_assets_passes_untracked_and_committed(self):
        shutil.copytree(self.root / "designs/01-original", self.root / "designs/01-original-v02-alice")
        self.check_result()
        self.commit("Add retained version")
        self.check_result(0, "--head", "HEAD")

    def test_existing_root_readme_navigation_edit_passes(self):
        (self.root / "designs/01-original/README.md").write_text("# Design\nNext: ../01-v02\n", encoding="utf-8")
        self.check_result()
        self.commit("Navigation")
        self.check_result(0, "--head", "HEAD")

    def test_existing_root_readme_may_be_added_but_not_deleted(self):
        readme = self.root / "designs/01-original/README.md"
        readme.unlink()
        self.check_result(1)
        self.commit("Legacy base missing readme")
        self.base = self.git("rev-parse", "HEAD").strip()
        readme.write_text("# Documentation\n", encoding="utf-8")
        self.check_result()

    def test_overwrite_preview_rejected(self):
        (self.root / "designs/01-original/preview.png").write_bytes(PNG + b"changed")
        self.assertIn("Existing design changed", self.check_result(1))
        self.commit("Overwrite")
        self.check_result(1, "--head", "HEAD")

    def test_source_deletion_rejected(self):
        (self.root / "designs/01-original/source/art.svg").unlink()
        self.assertIn("Existing design deleted", self.check_result(1))

    def test_whole_design_rename_rejected(self):
        (self.root / "designs/01-original").rename(self.root / "designs/01-renamed")
        self.assertIn("Existing design deleted", self.check_result(1))

    def test_new_file_inside_existing_source_rejected(self):
        (self.root / "designs/01-original/source/new.svg").write_text("<svg/>\n", encoding="utf-8")
        self.assertIn("Existing design added", self.check_result(1))

    def test_nested_readme_is_immutable(self):
        (self.root / "designs/01-original/source/README.md").write_text("new\n", encoding="utf-8")
        self.check_result(1)

    def test_stale_head_missing_newer_base_design_rejected(self):
        stale = self.base
        self.make_design("02-added-on-base")
        self.commit("New base design")
        self.base = self.git("rev-parse", "HEAD").strip()
        self.assertIn("02-added-on-base", self.check_result(1, "--head", stale))

    def test_new_design_requires_readme_and_valid_png(self):
        directory = self.make_design("02-new")
        (directory / "README.md").unlink()
        self.assertIn("regular README.md", self.check_result(1))
        (directory / "README.md").write_text("# Design\n", encoding="utf-8")
        (directory / "preview.png").unlink()
        self.assertIn("regular PNG preview", self.check_result(1))
        (directory / "preview.png").write_text("not a png", encoding="utf-8")
        self.assertIn("invalid signature", self.check_result(1))
        self.commit("Invalid PNG")
        self.check_result(1, "--head", "HEAD")

    def test_committed_symlink_rejected_without_os_symlink_privileges(self):
        self.make_design("02-new")
        self.git("add", "-A")
        oid = subprocess.run(
            ["git", "-C", str(self.root), "hash-object", "-w", "--stdin"],
            input=b"../01-original/source/art.svg", stdout=subprocess.PIPE, check=True,
        ).stdout.decode("ascii").strip()
        self.git("update-index", "--add", "--cacheinfo", f"120000,{oid},designs/02-new/source/link.svg")
        self.git("commit", "-q", "-m", "Symlink")
        self.assertIn("Unsupported link/submodule", self.check_result(1, "--head", "HEAD"))

    def test_git_symlink_mode_rejected_even_when_windows_uses_plain_file(self):
        self.make_design("02-new")
        self.git("config", "core.symlinks", "false")
        self.git("add", "-A")
        target = b"../01-original/source/art.svg"
        oid = subprocess.run(
            ["git", "-C", str(self.root), "hash-object", "-w", "--stdin"],
            input=target, stdout=subprocess.PIPE, check=True,
        ).stdout.decode("ascii").strip()
        self.git("update-index", "--add", "--cacheinfo", f"120000,{oid},designs/02-new/source/link.svg")
        (self.root / "designs/02-new/source/link.svg").write_bytes(target)
        self.assertIn("Unsupported link/submodule", self.check_result(1))

    def test_worktree_symlink_rejected_when_supported(self):
        directory = self.make_design("02-new")
        try:
            (directory / "source/link.svg").symlink_to("art.svg")
        except OSError as error:
            self.skipTest(f"OS does not permit creating symlinks: {error}")
        self.assertIn("Unsupported link/submodule", self.check_result(1))

    def test_paths_with_unicode_and_spaces(self):
        name = "02-浅蓝 新款"
        self.make_design(name)
        self.check_result()
        self.commit("Unicode directory")
        self.check_result(0, "--head", "HEAD")
        self.base = self.git("rev-parse", "HEAD").strip()
        path = self.root / "designs" / name / "source" / "空 格.svg"
        path.write_text("<svg/>\n", encoding="utf-8")
        self.assertIn("空 格.svg", self.check_result(1))

    @unittest.skipIf(os.name == "nt", "Windows filenames cannot contain newlines/tabs")
    def test_newline_and_tab_in_filename_are_not_split(self):
        directory = self.make_design("02-new\nversion")
        (directory / "source" / "art\tnew\n.svg").write_text("<svg/>\n", encoding="utf-8")
        self.check_result()
        self.commit("Unusual paths")
        self.check_result(0, "--head", "HEAD")
        self.base = self.git("rev-parse", "HEAD").strip()
        (directory / "source" / "art\tnew\n.svg").write_text("changed\n", encoding="utf-8")
        self.assertIn("art\\tnew\\n.svg", self.check_result(1))

    def test_ignored_generated_files_are_not_new_design_changes(self):
        path = self.root / "designs/01-original/generated"
        path.mkdir()
        (path / "scratch.svg").write_text("temporary\n", encoding="utf-8")
        self.check_result()

    def test_crlf_checkout_is_compared_using_git_normalization(self):
        (self.root / ".gitattributes").write_text("*.svg text eol=lf\n", encoding="utf-8")
        self.commit("Normalize source endings")
        self.base = self.git("rev-parse", "HEAD").strip()
        (self.root / "designs/01-original/source/art.svg").write_bytes(b"<svg/>\r\n")
        self.check_result()

    def test_base_required_and_invalid_ref_does_not_pass(self):
        self.check_result(2, "--head", "does-not-exist")
        result = subprocess.run([sys.executable, str(CHECKER)], cwd=self.root, capture_output=True)
        self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()
