#!/usr/bin/env python3
"""
Market Insights - Automate Chris Vermeulen YouTube analysis

This script checks for new Chris Vermeulen videos, fetches transcripts,
and cross-references recommendations with current portfolio.
"""

import argparse
import subprocess
import sys
from pathlib import Path

# JARVIS paths
SKILLS_DIR = Path(__file__).parent
CHECK_VIDEOS_SCRIPT = SKILLS_DIR / "check_new_videos.py"
VENV_PYTHON = SKILLS_DIR / ".venv/bin/python3"


def main():
    parser = argparse.ArgumentParser(
        description="JARVIS Market Insights - Chris Vermeulen YouTube automation"
    )
    parser.add_argument(
        "--check-new-videos",
        action="store_true",
        help="Check for new Chris Vermeulen videos"
    )

    args = parser.parse_args()

    if args.check_new_videos:
        # Call the existing check_new_videos.py script
        print("🎥 Checking for new Chris Vermeulen videos...\n")

        try:
            # Use venv python if available, otherwise fall back to system python3
            python_cmd = str(VENV_PYTHON) if VENV_PYTHON.exists() else "python3"

            result = subprocess.run(
                [python_cmd, str(CHECK_VIDEOS_SCRIPT)],
                cwd=SKILLS_DIR,
                timeout=60
            )
            return result.returncode

        except subprocess.TimeoutExpired:
            print("❌ Video check timed out after 60 seconds")
            return 1
        except Exception as e:
            print(f"❌ Error running video check: {e}")
            return 1
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
