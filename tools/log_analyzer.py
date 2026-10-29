#!/usr/bin/env python3
"""Count failed SSH authentications in a syslog-style file."""
import argparse
import re
from collections import Counter
from pathlib import Path

FAIL = re.compile(
    r"Failed password for (?:invalid user )?(?P<user>\S+) from (?P<ip>\d{1,3}(?:\.\d{1,3}){3})"
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("log_file", type=Path)
    args = parser.parse_args()
    counts = Counter()
    users = Counter()
    for line in args.log_file.read_text(encoding="utf-8", errors="replace").splitlines():
        match = FAIL.search(line)
        if not match:
            continue
        counts[match.group("ip")] += 1
        users[match.group("user")] += 1
    print("Failed password by source IP")
    for ip, n in counts.most_common():
        print(f"  {ip:16} {n}")
    print("Users targeted")
    for user, n in users.most_common():
        print(f"  {user:16} {n}")


if __name__ == "__main__":
    main()
