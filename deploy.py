"""Simple local deployment for the Lab 10 app.

Copies the application into a timestamped release folder, refreshes a
"current" folder that always holds the latest release, and smoke-tests
the deployed copy by importing it and calling greet().
"""
import argparse
import importlib.util
import os
import shutil
from datetime import datetime
from pathlib import Path

APP_FILES = ["app.py", "requirements.txt"]
EXPECTED = "Hello, World from Nadim Matta!"


def deploy(source_dir, target_dir, build_id="local"):
    """Copy the app into target_dir/releases/<stamp> and target_dir/current."""
    source_dir = Path(source_dir)
    target_dir = Path(target_dir)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    release = target_dir / "releases" / f"{stamp}-build{build_id}"
    release.mkdir(parents=True, exist_ok=False)
    for name in APP_FILES:
        shutil.copy2(source_dir / name, release / name)

    current = target_dir / "current"
    if current.exists():
        shutil.rmtree(current)
    shutil.copytree(release, current)
    (current / "VERSION").write_text(f"build {build_id} deployed {stamp}\n")
    return current


def smoke_test(deployed_dir):
    """Load the deployed app.py and check that greet() still works."""
    app_path = Path(deployed_dir) / "app.py"
    spec = importlib.util.spec_from_file_location("deployed_app", app_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    result = module.greet("World")
    if result != EXPECTED:
        raise RuntimeError(f"Smoke test failed: got {result!r}")
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description="Deploy the Lab 10 app")
    parser.add_argument("--target",
                        default=os.environ.get("DEPLOY_DIR", "deploy"),
                        help="deployment folder (default: $DEPLOY_DIR)")
    parser.add_argument("--build",
                        default=os.environ.get("BUILD_NUMBER", "local"),
                        help="build id (default: $BUILD_NUMBER)")
    args = parser.parse_args(argv)

    source = Path(__file__).resolve().parent
    current = deploy(source, args.target, args.build)
    output = smoke_test(current)
    print(f"Deployed build {args.build} to {current.resolve()}")
    print(f"Smoke test passed: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
