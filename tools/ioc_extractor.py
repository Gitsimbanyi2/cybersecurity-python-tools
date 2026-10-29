#!/usr/bin/env python3
"""Extract IPv4, FQDNs, and SHA256 hex from a text blob (lab IOCs)."""
import argparse
import re
from pathlib import Path

IP = re.compile(r"\b(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)\b")
SHA = re.compile(r"\b[a-fA-F0-9]{64}\b")
DOM = re.compile(r"\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b")
SKIP_DOM = {"ssh2", "localhost"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("text_file", type=Path)
    args = parser.parse_args()
    text = args.text_file.read_text(encoding="utf-8", errors="replace")
    ips = sorted(set(IP.findall(text)))
    shas = sorted(set(x.lower() for x in SHA.findall(text)))
    doms = sorted({d.lower() for d in DOM.findall(text) if d.lower() not in SKIP_DOM and " " not in d})
    print("IPv4")
    for item in ips:
        print(" ", item)
    print("Domains")
    for item in doms:
        print(" ", item)
    print("SHA256")
    for item in shas:
        print(" ", item)


if __name__ == "__main__":
    main()
