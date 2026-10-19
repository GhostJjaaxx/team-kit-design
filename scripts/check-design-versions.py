# Name: QiuCheng Zhen
# Nickname: HuangXiaoYunMeiMei WoXiHuanNi
# ID: 2400012917

"""Check that a proposal preserves every design directory at the base branch tip.

Run from anywhere inside the repository. --base is the current target branch tip,
not the merge base; --head selects a committed proposal, otherwise inspect the
working tree including non-ignored untracked files. No Git state is modified.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
import os
from pathlib import Path
import stat
import subprocess
import sys


PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
REGULAR_MODES = {b"100644", b"100755"}


class CheckError(Exception):
    """Repository state could not be inspected safely."""


@dataclass(frozen=True)
class Entry:
    mode: bytes
    oid: bytes


def display(path: bytes) -> str:
    # Quote control characters so even a newline in a filename stays on one line.
    return json.dumps(os.fsdecode(path), ensure_ascii=False)


def git(root: Path, *args: str, input_data: bytes | None = None) -> bytes:
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        input=input_data,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        raise CheckError(f"Git inspection failed: {detail}")
    return result.stdout


def repository_root() -> Path:
    output = git(Path.cwd(), "rev-parse", "--show-toplevel")
    # Remove Git's one record terminator, not whitespace belonging to the path.
    return Path(os.fsdecode(output.removesuffix(b"\n")))


def commit_id(root: Path, ref: str) -> str:
    return git(
        root, "rev-parse", "--verify", "--end-of-options", f"{ref}^{{commit}}"
    ).decode("ascii").strip()


def committed_entries(root: Path, commit: str) -> dict[bytes, Entry]:
    records = git(root, "ls-tree", "-r", "-z", "--full-tree", commit, "--", "designs")
    entries = {}
    for record in records.split(b"\0"):
        if not record:
            continue
        metadata, path = record.split(b"\t", 1)
        mode, _kind, oid = metadata.split(b" ")
        entries[path] = Entry(mode, oid)
    return entries


def unsafe_ancestor(root: Path, path: bytes) -> bytes | None:
    """Never follow directory links, including Windows junctions, to inspect art."""
    components = path.split(b"/")
    for count in range(1, len(components) + 1):
        partial = b"/".join(components[:count])
        target = root / os.fsdecode(partial)
        try:
            info = target.lstat()
        except (FileNotFoundError, NotADirectoryError):
            return None
        if stat.S_ISLNK(info.st_mode) or (
            getattr(info, "st_file_attributes", 0)
            & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
        ):
            return partial
    return None


def working_entries(root: Path) -> dict[bytes, Entry]:
    tracked = {}
    records = git(root, "ls-files", "--stage", "-z", "--", "designs")
    for record in records.split(b"\0"):
        if not record:
            continue
        metadata, path = record.split(b"\t", 1)
        mode, oid, stage = metadata.split(b" ")
        if stage != b"0":
            raise CheckError(f"Resolve the merge conflict before checking {display(path)}.")
        tracked[path] = Entry(mode, oid)
    untracked = git(root, "ls-files", "--others", "--exclude-standard", "-z", "--", "designs")
    paths = set(tracked) | {path for path in untracked.split(b"\0") if path}
    # Git's default is true, but Windows checkouts commonly set this to false.
    file_mode = git(root, "config", "--type=bool", "--default=true", "--get", "core.filemode")
    trust_executable_bit = file_mode.strip() == b"true"
    entries = {}
    for path in sorted(paths):
        linked_path = unsafe_ancestor(root, path)
        if linked_path is not None:
            entries[linked_path] = Entry(b"120000", b"")
            continue
        target = root / os.fsdecode(path)
        try:
            info = target.lstat()
        except (FileNotFoundError, NotADirectoryError):
            continue
        if path in tracked and tracked[path].mode not in REGULAR_MODES:
            # With core.symlinks=false a Git symlink appears on disk as a plain
            # file containing its destination. Its index mode still matters.
            entries[path] = tracked[path]
            continue
        if not stat.S_ISREG(info.st_mode):
            # A tracked file replaced by a directory is absent from this snapshot;
            # any new files inside it are separately discovered by ls-files.
            if not stat.S_ISDIR(info.st_mode):
                entries[path] = Entry(b"unsupported", b"")
            continue
        if trust_executable_bit:
            mode = b"100755" if info.st_mode & stat.S_IXUSR else b"100644"
        else:
            previous_mode = tracked.get(path, Entry(b"100644", b"")).mode
            mode = previous_mode if previous_mode in REGULAR_MODES else b"100644"
        # Ask Git to apply the same clean/line-ending filters as an eventual
        # commit; a CRLF checkout of an unchanged LF blob must not be rejected.
        with target.open("rb") as stream:
            result = subprocess.run(
                ["git", "-C", str(root), "hash-object", f"--path={os.fsdecode(path)}", "--stdin"],
                stdin=stream,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
        if result.returncode:
            raise CheckError(f"Cannot hash {display(path)}: {result.stderr.decode('utf-8', errors='replace').strip()}")
        entries[path] = Entry(mode, result.stdout.strip())
    return entries


def design_directories(entries: dict[bytes, Entry]) -> set[bytes]:
    return {
        b"/".join(path.split(b"/")[:2])
        for path in entries
        if path.startswith(b"designs/") and len(path.split(b"/")) >= 3
    }


def check(
    root: Path,
    base: dict[bytes, Entry],
    proposed: dict[bytes, Entry],
    committed_head: bool,
) -> list[str]:
    errors = []
    for path, entry in sorted(proposed.items()):
        if entry.mode not in REGULAR_MODES:
            errors.append(f"Unsupported link/submodule/file mode in designs: {display(path)}. Use regular files.")
    existing = design_directories(base)
    for directory in sorted(existing):
        prefix = directory + b"/"
        old_paths = {path for path in base if path.startswith(prefix)}
        new_paths = {path for path in proposed if path.startswith(prefix)}
        readme = prefix + b"README.md"
        for path in sorted(old_paths | new_paths):
            if path == readme and path in proposed and proposed[path].mode in REGULAR_MODES:
                continue
            if base.get(path) == proposed.get(path):
                continue
            change = "added" if path not in base else "deleted" if path not in proposed else "changed"
            errors.append(f"Existing design {change}: {display(path)}. Keep the old version and put the full iteration in a NEW sibling design directory.")
    for directory in sorted(design_directories(proposed) - existing):
        readme = directory + b"/README.md"
        preview = directory + b"/preview.png"
        if readme not in proposed or proposed[readme].mode not in REGULAR_MODES:
            errors.append(f"New design needs a regular README.md: {display(readme)}.")
        if preview not in proposed or proposed[preview].mode not in REGULAR_MODES:
            errors.append(f"New design needs a regular PNG preview: {display(preview)}.")
            continue
        if committed_head:
            signature = git(root, "cat-file", "blob", proposed[preview].oid.decode("ascii"))[:8]
        else:
            with (root / os.fsdecode(preview)).open("rb") as stream:
                signature = stream.read(8)
        if signature != PNG_SIGNATURE:
            errors.append(f"Preview is not a PNG (invalid signature): {display(preview)}.")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", required=True, help="Current target-branch tip, e.g. origin/main; NOT merge-base")
    parser.add_argument("--head", help="Proposed commit/ref; omit to inspect the full working tree")
    args = parser.parse_args()
    try:
        root = repository_root()
        base_commit = commit_id(root, args.base)
        base = committed_entries(root, base_commit)
        if args.head is not None:
            proposed = committed_entries(root, commit_id(root, args.head))
        else:
            proposed = working_entries(root)
        errors = check(root, base, proposed, args.head is not None)
    except (CheckError, OSError, ValueError) as error:
        print(f"Design version check could not run: {error}", file=sys.stderr)
        return 2
    if errors:
        print("Design version check FAILED:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        print(
            "Use a new designs/<new-id>/ folder containing the complete preview, editable sources and ancestry README. "
            "Only an existing design's root README.md may be edited or added (never deleted). "
            "If the branch is behind, merge the latest base branch first so its designs are retained.",
            file=sys.stderr,
        )
        return 1
    print(f"Design version check passed against base tip {base_commit[:12]}: existing versions retained.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
