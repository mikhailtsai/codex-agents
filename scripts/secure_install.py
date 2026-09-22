#!/usr/bin/env python3
"""Install the harness using directory file descriptors and no-follow opens."""

import os
import shutil
import stat
import sys
import uuid
from pathlib import Path


PAYLOAD_DIRECTORIES = (
    ".codex",
    ".agents",
    ".codex-evals",
    "docs/exec-plans/active",
    "docs/exec-plans/completed",
)
PAYLOAD_FILES = (
    "AGENTS.md",
    ".github/workflows/harness-check.yml",
    "scripts/check-harness.py",
    "scripts/eval-report.py",
    "scripts/eval_schema.py",
    "tests/test_harness.py",
    "docs/agent/README.md",
)
DIRECTORY_FLAGS = os.O_RDONLY | os.O_DIRECTORY | getattr(os, "O_NOFOLLOW", 0)
NOFOLLOW = getattr(os, "O_NOFOLLOW", 0)


class Installer:
    def __init__(self, source_root, target_root):
        source_path = os.path.abspath(source_root)
        target_path = os.path.abspath(target_root)
        common_path = os.path.commonpath((source_path, target_path))
        if common_path in {source_path, target_path}:
            raise ValueError("source and target paths must not contain one another")
        self.source_root = Path(source_path)
        self.source_fd = self.open_absolute_directory(source_path)
        self.target_root = Path(target_path)
        try:
            self.root_fd = self.open_absolute_directory(target_path)
        except Exception:
            os.close(self.source_fd)
            raise
        self.created_files = []
        self.created_directories = []

    @staticmethod
    def open_absolute_directory(path):
        parts = Path(path).parts
        fd = os.open(os.sep, DIRECTORY_FLAGS)
        try:
            for component in parts[1:]:
                next_fd = os.open(component, DIRECTORY_FLAGS, dir_fd=fd)
                os.close(fd)
                fd = next_fd
            return fd
        except Exception:
            os.close(fd)
            raise

    def close(self):
        for parent_fd, _, file_fd, _, _ in self.created_files:
            os.close(file_fd)
            os.close(parent_fd)
        for parent_fd, _, _, _ in self.created_directories:
            os.close(parent_fd)
        os.close(self.root_fd)
        os.close(self.source_fd)

    @staticmethod
    def exists(parent_fd, name):
        try:
            os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
        except FileNotFoundError:
            return False
        return True

    def open_target_directory(self, relative_parts, create=False):
        fd = os.dup(self.root_fd)
        try:
            for component in relative_parts:
                if component in {"", ".", ".."}:
                    raise ValueError(f"invalid target component: {component!r}")
                created_stat = None
                existing_stat = None
                if create:
                    try:
                        os.mkdir(component, 0o755, dir_fd=fd)
                    except FileExistsError:
                        existing_stat = os.stat(component, dir_fd=fd, follow_symlinks=False)
                    else:
                        created_stat = os.stat(component, dir_fd=fd, follow_symlinks=False)
                        self.created_directories.append(
                            (os.dup(fd), component, created_stat.st_dev, created_stat.st_ino)
                        )
                        os.chmod(component, 0o755, dir_fd=fd, follow_symlinks=False)
                else:
                    existing_stat = os.stat(component, dir_fd=fd, follow_symlinks=False)
                next_fd = os.open(component, DIRECTORY_FLAGS, dir_fd=fd)
                opened_stat = os.fstat(next_fd)
                expected_stat = created_stat or existing_stat
                if (opened_stat.st_dev, opened_stat.st_ino) != (expected_stat.st_dev, expected_stat.st_ino):
                    os.close(next_fd)
                    raise RuntimeError(f"target directory changed during install: {component}")
                os.close(fd)
                fd = next_fd
            return fd
        except Exception:
            os.close(fd)
            raise

    def open_source_directory(self, relative_parts):
        fd = os.dup(self.source_fd)
        try:
            for component in relative_parts:
                if component in {"", ".", ".."}:
                    raise ValueError(f"invalid source component: {component!r}")
                expected_stat = os.stat(component, dir_fd=fd, follow_symlinks=False)
                next_fd = os.open(component, DIRECTORY_FLAGS, dir_fd=fd)
                opened_stat = os.fstat(next_fd)
                if (opened_stat.st_dev, opened_stat.st_ino) != (expected_stat.st_dev, expected_stat.st_ino):
                    os.close(next_fd)
                    raise RuntimeError(f"source directory changed during install: {component}")
                os.close(fd)
                fd = next_fd
            return fd
        except Exception:
            os.close(fd)
            raise

    def copy_file(self, source_parent_fd, source_name, target_parent_fd, target_name):
        source_fd = os.open(source_name, os.O_RDONLY | NOFOLLOW, dir_fd=source_parent_fd)
        temporary_name = None
        temporary_fd = None
        try:
            source_stat = os.fstat(source_fd)
            if not stat.S_ISREG(source_stat.st_mode):
                raise ValueError(f"source is not a regular file: {source_name}")
            source_mode = stat.S_IMODE(source_stat.st_mode)
            while True:
                candidate = f".codex-agents-file-{uuid.uuid4().hex}"
                try:
                    temporary_fd = os.open(
                        candidate,
                        os.O_WRONLY | os.O_CREAT | os.O_EXCL,
                        source_mode,
                        dir_fd=target_parent_fd,
                    )
                    temporary_name = candidate
                    break
                except FileExistsError:
                    continue
            os.fchmod(temporary_fd, source_mode)
            with os.fdopen(source_fd, "rb", closefd=False) as source, os.fdopen(
                temporary_fd, "wb", closefd=False
            ) as temporary:
                shutil.copyfileobj(source, temporary)
                temporary.flush()
            os.fsync(temporary_fd)
            installed_fd = os.dup(temporary_fd)
            installed_stat = os.fstat(installed_fd)
            self.created_files.append(
                (os.dup(target_parent_fd), target_name, installed_fd, installed_stat.st_dev, installed_stat.st_ino)
            )
            os.link(
                temporary_name,
                target_name,
                src_dir_fd=target_parent_fd,
                dst_dir_fd=target_parent_fd,
                follow_symlinks=False,
            )
            os.close(temporary_fd)
            temporary_fd = None
            os.unlink(temporary_name, dir_fd=target_parent_fd)
            temporary_name = None
        finally:
            os.close(source_fd)
            if temporary_fd is not None:
                os.close(temporary_fd)
            if temporary_name is not None:
                try:
                    os.unlink(temporary_name, dir_fd=target_parent_fd)
                except FileNotFoundError:
                    pass

    def copy_tree_entry(self, source_parent_fd, source_name, target_parent_fd, target_name):
        source_stat = os.stat(source_name, dir_fd=source_parent_fd, follow_symlinks=False)
        if stat.S_ISLNK(source_stat.st_mode):
            raise ValueError(f"source contains a symlink: {source_name}")
        if stat.S_ISREG(source_stat.st_mode):
            if self.exists(target_parent_fd, target_name):
                raise FileExistsError(target_name)
            self.copy_file(source_parent_fd, source_name, target_parent_fd, target_name)
            return
        if not stat.S_ISDIR(source_stat.st_mode):
            raise ValueError(f"unsupported source entry: {source_name}")

        source_directory_fd = None
        directory_fd = None
        try:
            source_directory_fd = os.open(source_name, DIRECTORY_FLAGS, dir_fd=source_parent_fd)
            opened_source_stat = os.fstat(source_directory_fd)
            if (opened_source_stat.st_dev, opened_source_stat.st_ino) != (source_stat.st_dev, source_stat.st_ino):
                raise RuntimeError(f"source directory changed during install: {source_name}")

            if self.exists(target_parent_fd, target_name):
                target_stat = os.stat(target_name, dir_fd=target_parent_fd, follow_symlinks=False)
                if not stat.S_ISDIR(target_stat.st_mode):
                    raise FileExistsError(target_name)
            else:
                source_mode = stat.S_IMODE(source_stat.st_mode)
                os.mkdir(target_name, source_mode, dir_fd=target_parent_fd)
                target_stat = os.stat(target_name, dir_fd=target_parent_fd, follow_symlinks=False)
                self.created_directories.append(
                    (os.dup(target_parent_fd), target_name, target_stat.st_dev, target_stat.st_ino)
                )
                os.chmod(target_name, source_mode, dir_fd=target_parent_fd, follow_symlinks=False)
            directory_fd = os.open(target_name, DIRECTORY_FLAGS, dir_fd=target_parent_fd)
            opened_target_stat = os.fstat(directory_fd)
            if (opened_target_stat.st_dev, opened_target_stat.st_ino) != (
                target_stat.st_dev,
                target_stat.st_ino,
            ):
                raise RuntimeError(f"target directory changed during install: {target_name}")

            for child_name in sorted(os.listdir(source_directory_fd)):
                self.copy_tree_entry(source_directory_fd, child_name, directory_fd, child_name)
        finally:
            if directory_fd is not None:
                os.close(directory_fd)
            if source_directory_fd is not None:
                os.close(source_directory_fd)

    def install(self):
        for relative_path in PAYLOAD_DIRECTORIES:
            path = Path(relative_path)
            source_parent_fd = self.open_source_directory(path.parent.parts)
            target_parent_fd = self.open_target_directory(path.parent.parts, create=True)
            try:
                if relative_path.startswith("docs/exec-plans/") and self.exists(target_parent_fd, path.name):
                    existing_stat = os.stat(path.name, dir_fd=target_parent_fd, follow_symlinks=False)
                    if not stat.S_ISDIR(existing_stat.st_mode):
                        raise ValueError(f"target is not a regular directory: {relative_path}")
                else:
                    self.copy_tree_entry(source_parent_fd, path.name, target_parent_fd, path.name)
            finally:
                os.close(source_parent_fd)
                os.close(target_parent_fd)

        for relative_path in PAYLOAD_FILES:
            path = Path(relative_path)
            source_parent_fd = self.open_source_directory(path.parent.parts)
            target_parent_fd = self.open_target_directory(path.parent.parts, create=True)
            try:
                if relative_path == "docs/agent/README.md" and self.exists(target_parent_fd, path.name):
                    existing_stat = os.stat(path.name, dir_fd=target_parent_fd, follow_symlinks=False)
                    if not stat.S_ISREG(existing_stat.st_mode):
                        raise ValueError(f"target is not a regular file: {relative_path}")
                    continue
                self.copy_tree_entry(source_parent_fd, path.name, target_parent_fd, path.name)
            finally:
                os.close(source_parent_fd)
                os.close(target_parent_fd)

    def rollback(self):
        for parent_fd, name, file_fd, device, inode in reversed(self.created_files):
            try:
                current = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
                installed = os.fstat(file_fd)
                if (current.st_dev, current.st_ino) == (device, inode) and (installed.st_dev, installed.st_ino) == (device, inode):
                    os.unlink(name, dir_fd=parent_fd)
            except FileNotFoundError:
                pass
        for parent_fd, name, device, inode in reversed(self.created_directories):
            try:
                current = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
                if (current.st_dev, current.st_ino) == (device, inode):
                    os.rmdir(name, dir_fd=parent_fd)
            except (FileNotFoundError, OSError):
                pass


def main():
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} SOURCE_ROOT TARGET_ROOT", file=sys.stderr)
        return 2
    try:
        installer = Installer(sys.argv[1], sys.argv[2])
    except Exception as error:
        print(f"secure installation failed: {error}", file=sys.stderr)
        return 1
    try:
        installer.install()
    except Exception as error:
        installer.rollback()
        print(f"secure installation failed: {error}", file=sys.stderr)
        return 1
    finally:
        installer.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
