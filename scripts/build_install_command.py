#!/usr/bin/env python3
"""Build the canonical StellaGate-UI install command."""

from __future__ import annotations

import argparse
import shlex


DEFAULT_INSTALLER = "https://raw.githubusercontent.com/Ralph179/StellaGate-UI/codex/stellagate/install.sh"


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a StellaGate-UI installer command.")
    parser.add_argument("--cloud", default="https://stellagate.simuse.uk", help="Authorization endpoint URL")
    parser.add_argument("--invite", help="Optional invite code for immediate activation")
    parser.add_argument("--installer", default=DEFAULT_INSTALLER, help="Installer URL")
    args = parser.parse_args()

    command = [
        "curl",
        "-fsSL",
        args.installer,
        "|",
        "bash",
        "-s",
        "--",
        "--cloud",
        args.cloud,
    ]
    if args.invite:
        command.extend(["--invite", args.invite])

    rendered = " ".join(part if part == "|" else shlex.quote(part) for part in command)
    print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
