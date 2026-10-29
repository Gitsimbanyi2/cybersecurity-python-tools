#!/usr/bin/env python3
"""Build a short markdown security report from a synthetic auth log."""
import argparse
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
import re

FAIL = re.compile(
    r"Failed password for (?:invalid user )?(?P<user>\S+) from (?P<ip>\d{1,3}(?:\.\d{1,3}){3})"
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("log_file", type=Path)
    parser.add_argument("--out", type=Path, default=Path("lab-security-report.md"))
    args = parser.parse_args()
    counts = Counter()
    for line in args.log_file.read_text(encoding="utf-8", errors="replace").splitlines():
        match = FAIL.search(line)
        if match:
            counts[match.group("ip")] += 1
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# Lab security report",
        "",
        f"Generated: {generated}",
        f"Source: `{args.log_file.name}` (synthetic)",
        "",
        "| Source IP | Failed passwords |",
        "|-----------|------------------|",
    ]
    for ip, n in counts.most_common():
        lines.append(f"| {ip} | {n} |")
    if not counts:
        lines.append("| (none) | 0 |")
    lines.append("")
    lines.append("This report is for lab training. It is not a production SOC deliverable.")
    args.out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
