#!/usr/bin/env python3
"""Audit claims in docs against evidence in results/."""
import os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(REPO, "docs")
RESULTS = os.path.join(REPO, "results")

def collect_result_text():
    texts = []
    for root, _, files in os.walk(RESULTS):
        for f in files:
            path = os.path.join(root, f)
            try:
                with open(path, "r", encoding="utf-8", errors="replace") as fh:
                    texts.append((path, fh.read()))
            except Exception:
                pass
    return texts

def main():
    result_texts = collect_result_text()
    all_result_content = "\n".join(t for _, t in result_texts)

    claims = []
    for root, _, files in os.walk(DOCS):
        for f in files:
            if not f.endswith(".md"):
                continue
            path = os.path.join(root, f)
            with open(path, "r", encoding="utf-8", errors="replace") as fh:
                content = fh.read()
            # Find V-refs
            for m in re.finditer(r"V\d{3,4}", content):
                v = m.group(0)
                has_evidence = v in all_result_content
                claims.append((os.path.relpath(path, REPO), v, has_evidence))
            # Find CONFIRMED lines
            for i, line in enumerate(content.splitlines(), 1):
                if "CONFIRMED" in line and ("device" in line.lower() or "on device" in line.lower()):
                    claims.append((os.path.relpath(path, REPO), f"CONFIRMED@{i}", None))

    # Report
    print("=== CLAIM AUDIT ===")
    print(f"Result files scanned: {len(result_texts)}")
    vrefs = [c for c in claims if c[1].startswith("V")]
    print(f"V-refs found in docs: {len(vrefs)}")
    no_ev = [c for c in vrefs if not c[2]]
    print(f"V-refs WITHOUT evidence in results/: {len(no_ev)}")
    for doc, v, _ in no_ev:
        print(f"  - {doc}: {v}")
    print()
    conf = [c for c in claims if c[1].startswith("CONFIRMED")]
    print(f"CONFIRMED lines found: {len(conf)}")
    for doc, v, _ in conf:
        print(f"  - {doc}: {v}")

if __name__ == "__main__":
    main()