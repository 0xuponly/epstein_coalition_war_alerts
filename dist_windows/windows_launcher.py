#!/usr/bin/env python3
"""
Windows-compatible launcher for the Telegram channel forwarder + optional UI.
Creates venv, installs requirements, then offers a menu (same pattern as tg_mantracker dist_windows).
"""

import os
import shutil
import subprocess
import sys
import venv
from pathlib import Path


class CoalitionForwarderLauncher:
    def __init__(self):
        self.app_dir = Path(__file__).resolve().parent
        self.venv_dir = self.app_dir / "venv"
        self.logs_dir = self.app_dir / "logs"

    def _python_pip(self):
        if sys.platform == "win32":
            return (
                self.venv_dir / "Scripts" / "python.exe",
                self.venv_dir / "Scripts" / "pip.exe",
            )
        return self.venv_dir / "bin" / "python", self.venv_dir / "bin" / "pip"

    def setup_environment(self):
        print("Telegram channel forwarder - Windows setup")
        print("=" * 50)

        self.logs_dir.mkdir(parents=True, exist_ok=True)

        if not self.venv_dir.exists():
            print("Creating virtual environment...")
            venv.create(self.venv_dir, with_pip=True)
            print("  OK: venv created at", self.venv_dir)

        python_path, pip_path = self._python_pip()
        req = self.app_dir / "requirements.txt"
        if not req.exists():
            print("ERROR: requirements.txt not found in", self.app_dir)
            return None

        print("Installing / updating dependencies...")
        try:
            subprocess.run(
                [str(pip_path), "install", "-q", "-r", str(req)],
                check=True,
            )
            print("  OK: requirements installed")
        except subprocess.CalledProcessError as e:
            print("ERROR: pip install failed:", e)
            return None

        return str(python_path)

    def ensure_env_file(self):
        env_path = self.app_dir / ".env"
        example = self.app_dir / "env.example"
        if not env_path.exists():
            if example.exists():
                shutil.copy(example, env_path)
                print("\nCreated .env from env.example - please edit it with your API credentials.")
            else:
                print("\nERROR: No .env and no env.example - add .env manually.")
                return False
        return True

    def check_configuration(self):
        env_path = self.app_dir / ".env"
        if not env_path.exists():
            return False

        try:
            from dotenv import load_dotenv

            load_dotenv(env_path)
        except ImportError:
            print("ERROR: python-dotenv missing - run setup again.")
            return False

        api_id = os.environ.get("TELEGRAM_API_ID", "").strip()
        api_hash = os.environ.get("TELEGRAM_API_HASH", "").strip()
        dest = os.environ.get("TELEGRAM_FORWARD_TO_1", "").strip()
        kw = os.environ.get("TELEGRAM_KEYWORDS_1", "").strip()

        missing = []
        if not api_id or api_id == "12345678":
            missing.append("TELEGRAM_API_ID (real value from my.telegram.org)")
        if not api_hash or "your_api" in api_hash.lower():
            missing.append("TELEGRAM_API_HASH")
        if not dest:
            missing.append("TELEGRAM_FORWARD_TO_1")
        if not kw:
            missing.append("TELEGRAM_KEYWORDS_1")

        if missing:
            print("\nConfiguration incomplete. Fix .env:")
            for m in missing:
                print("  -", m)
            print("\nFile:", env_path)
            return False

        print("Configuration looks OK (API + channel 1).")
        return True

    def run_forwarder(self, python_path):
        script = self.app_dir / "forward_channel_messages.py"
        if not script.exists():
            print("ERROR: forward_channel_messages.py not found")
            return
        print("\nStarting forwarder (Ctrl+C to stop)...\n")
        try:
            subprocess.run([python_path, str(script)], cwd=str(self.app_dir), check=False)
        except KeyboardInterrupt:
            print("\nStopped.")

    def run_ui(self, python_path):
        script = self.app_dir / "ui_app.py"
        if not script.exists():
            print("ERROR: ui_app.py not found")
            return
        os.environ.setdefault("TELEGRAM_UI_QUIET", "1")
        print("\nStarting web UI. Open http://127.0.0.1:8765 (Ctrl+C to stop)...\n")
        try:
            subprocess.run([python_path, str(script)], cwd=str(self.app_dir), check=False)
        except KeyboardInterrupt:
            print("\nStopped.")

    def tail_log(self):
        logf = self.logs_dir / "forwarder.log"
        if not logf.exists():
            print("No logs/forwarder.log yet.")
            return
        print(f"\nLast 25 lines of {logf}:\n")
        try:
            lines = logf.read_text(encoding="utf-8", errors="replace").splitlines()
            for line in lines[-25:]:
                print(" ", line)
        except OSError as e:
            print("Read error:", e)

    def main(self):
        print("Telegram coalition channel forwarder (Windows package)")
        print("=" * 50)

        py = self.setup_environment()
        if not py:
            return 1

        self.ensure_env_file()

        while True:
            print("\nWhat would you like to do?")
            print("  1 - Run forwarder (monitor channels / forward messages)")
            print("  2 - Run local web UI (view forwards, sound mute)")
            print("  3 - Configuration help (.env path)")
            print("  4 - Tail forwarder log")
            print("  5 - Exit")

            choice = input("\nEnter choice (1-5): ").strip()

            if choice == "1":
                if not self.check_configuration():
                    continue
                self.run_forwarder(py)
            elif choice == "2":
                if not self.check_configuration():
                    continue
                self.run_ui(py)
            elif choice == "3":
                print("\nEdit this file in Notepad or your editor:")
                print(" ", self.app_dir / ".env")
                print("\nCopy from env.example if needed:")
                print(" ", self.app_dir / "env.example")
                print("\nRequired: TELEGRAM_API_ID, TELEGRAM_API_HASH,")
                print("  TELEGRAM_FORWARD_TO_1, TELEGRAM_KEYWORDS_1 (and optional _2 / _3).")
            elif choice == "4":
                self.tail_log()
            elif choice == "5":
                print("Goodbye.")
                break
            else:
                print("Invalid choice.")

        return 0


if __name__ == "__main__":
    sys.exit(CoalitionForwarderLauncher().main())
