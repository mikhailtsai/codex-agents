import os
import subprocess
import shutil
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_REPOSITORY = (ROOT / "tests/.source-repository").is_file()


class HarnessTests(unittest.TestCase):
    def run_script(self, script, cwd=ROOT):
        return subprocess.run(
            ["python3", str(ROOT / script)],
            cwd=cwd,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_self_check_and_report_pass(self):
        check = self.run_script("scripts/check-harness.py")
        report = self.run_script("scripts/eval-report.py")
        self.assertEqual(check.returncode, 0, check.stdout + check.stderr)
        self.assertEqual(report.returncode, 0, report.stdout + report.stderr)

    @unittest.skipUnless(SOURCE_REPOSITORY, "installer test is only present in the source repository")
    def test_install_is_complete_and_preserves_conflicts(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            scripts = target / "scripts"
            scripts.mkdir()
            existing = scripts / "eval-report.py"
            existing.write_text("project-owned\n")

            result = subprocess.run(
                ["bash", str(ROOT / "install.sh"), str(target)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(existing.read_text(), "project-owned\n")
            self.assertFalse((target / ".codex").exists())

            existing.unlink()
            result = subprocess.run(
                ["bash", str(ROOT / "install.sh"), str(target)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            for relative_path in (
                ".codex/config.toml",
                ".agents/skills/verify/SKILL.md",
                ".codex-evals/runs.jsonl",
                "docs/exec-plans/active",
                "docs/exec-plans/completed",
                ".github/workflows/harness-check.yml",
                "scripts/check-harness.py",
                "scripts/eval-report.py",
                "scripts/eval_schema.py",
                "tests/test_harness.py",
            ):
                self.assertTrue((target / relative_path).exists(), relative_path)
            installed_check = subprocess.run(
                ["python3", str(target / "scripts/check-harness.py")],
                cwd=target,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(installed_check.returncode, 0, installed_check.stdout + installed_check.stderr)

    @unittest.skipUnless(SOURCE_REPOSITORY, "installer test is only present in the source repository")
    def test_install_merges_compatible_directories(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            (target / ".codex/agents").mkdir(parents=True)
            (target / ".codex/agents/local.toml").write_text('name = "local"\n')
            (target / ".agents/skills/local/SKILL.md").parent.mkdir(parents=True)
            (target / ".agents/skills/local/SKILL.md").write_text("project skill\n")
            (target / "scripts").mkdir()
            (target / "scripts/project-check.py").write_text("project check\n")
            (target / "docs/exec-plans/active").mkdir(parents=True)
            (target / "docs/agent").mkdir(parents=True)
            existing_readme = target / "docs/agent/README.md"
            existing_readme.write_text("project map\n")

            result = subprocess.run(
                ["bash", str(ROOT / "install.sh"), str(target)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual((target / ".codex/agents/local.toml").read_text(), 'name = "local"\n')
            self.assertEqual((target / ".agents/skills/local/SKILL.md").read_text(), "project skill\n")
            self.assertEqual((target / "scripts/project-check.py").read_text(), "project check\n")
            self.assertEqual(existing_readme.read_text(), "project map\n")
            self.assertTrue((target / ".codex/agents/researcher.toml").is_file())

    @unittest.skipUnless(SOURCE_REPOSITORY, "installer test is only present in the source repository")
    def test_nested_conflict_is_rejected_before_copying(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            conflicting_skill = target / ".agents/skills/review-loop/SKILL.md"
            conflicting_skill.parent.mkdir(parents=True)
            conflicting_skill.write_text("project-owned\n")

            result = subprocess.run(
                ["bash", str(ROOT / "install.sh"), str(target)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(conflicting_skill.read_text(), "project-owned\n")
            self.assertFalse((target / ".codex").exists())

    @unittest.skipUnless(SOURCE_REPOSITORY, "installer test is only present in the source repository")
    def test_installer_rejects_symlinks_and_incomplete_sources(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            symlink_target = root / "symlink-target"
            symlink_target.mkdir()
            symlink_project = root / "symlink-project"
            symlink_project.mkdir()
            (symlink_project / "scripts").symlink_to(symlink_target, target_is_directory=True)

            result = subprocess.run(
                ["bash", str(ROOT / "install.sh"), str(symlink_project)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse((symlink_project / ".codex").exists())

            dangling_project = root / "dangling-project"
            dangling_project.mkdir()
            (dangling_project / "docs/agent").mkdir(parents=True)
            (dangling_project / "docs/agent/README.md").symlink_to(root / "missing-readme")

            result = subprocess.run(
                ["bash", str(ROOT / "install.sh"), str(dangling_project)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse((dangling_project / ".codex").exists())

            source = root / "source"
            shutil.copytree(ROOT, source)
            (source / "scripts/eval_schema.py").unlink()
            incomplete_project = root / "incomplete-project"
            incomplete_project.mkdir()

            result = subprocess.run(
                ["bash", str(source / "install.sh"), str(incomplete_project)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse((incomplete_project / ".codex").exists())

            source = root / "source-with-invalid-entry"
            shutil.copytree(ROOT, source)
            os.mkfifo(source / ".agents/skills/zz-invalid")
            rollback_project = root / "rollback-project"
            rollback_project.mkdir()
            preserved = rollback_project / "project-owned.txt"
            preserved.write_text("keep\n")

            result = subprocess.run(
                ["bash", str(source / "install.sh"), str(rollback_project)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(preserved.read_text(), "keep\n")
            self.assertFalse((rollback_project / ".codex").exists())
            self.assertFalse((rollback_project / ".agents").exists())

    def test_malformed_json_values_fail_cleanly(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            for relative_path in (".codex", ".agents", ".codex-evals"):
                shutil.copytree(ROOT / relative_path, target / relative_path)
            for relative_path in ("AGENTS.md", "scripts/check-harness.py", "scripts/eval_schema.py"):
                destination = target / relative_path
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(ROOT / relative_path, destination)
            (target / ".codex-evals/runs.jsonl").write_text(
                "[]\n"
                "{\"outcome\":[],\"agents\":[\"researcher\"],\"retries\":0}\n"
                "{\"outcome\":\"PASS\",\"agents\":[],\"retries\":0}\n"
                "{\"outcome\":\"PASS\",\"agents\":[\"researcher\"],\"retries\":0,\"checks\":null,\"review_findings\":null,\"notes\":null}\n"
            )

            result = subprocess.run(
                ["python3", str(target / "scripts/check-harness.py")],
                cwd=target,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("row must be a JSON object", result.stdout)
            self.assertIn("invalid outcome", result.stdout)
            self.assertIn("agents must not be empty", result.stdout)
            self.assertIn("checks must be an object", result.stdout)
            self.assertIn("review_findings must be a non-negative integer", result.stdout)
            self.assertIn("notes must be a list of strings", result.stdout)

if __name__ == "__main__":
    unittest.main()
