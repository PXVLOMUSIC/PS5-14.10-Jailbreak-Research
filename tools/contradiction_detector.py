#!/usr/bin/env python3
"""Detect internal contradictions in markdown docs."""
import os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(REPO, "docs")

# Known contradictions from issue tracker
KNOWN = [
    ("FINDINGS.md", "unitsPerEm=0", "Line 91 says 'loads AND renders', table line 111 says 'REJECTED'"),
    ("FINDINGS.md", "Freed memory is NOT zeroed", "Issue #1 (Portablelle) showed ~400B blocks decommit (MADV_FREE)"),
    ("FINDINGS.md", "State Buffer Reclaim ~6400 bytes", "mja00 measured 8192 bytes (bmalloc class 95)"),
    ("CONFIRMED_VULNS.md", "context ~384-512 bytes", "mja00 measured 712 bytes (class 67)"),
    ("README.md", "BYOB readers available", "5 docs say BYOB not implemented on 14.10"),
    ("README.md", "freed memory stays mapped", "Only large blocks; small blocks decommit"),
]

def check_units_per_em(path, content):
    """Check unitsPerEm contradiction."""
    issues = []
    if "unitsPerEm=0 loads AND renders" in content and "unitsPerEm=0 | REJECTED" in content:
        issues.append("unitsPerEm=0: contradictory verdict (renders vs REJECTED)")
    return issues

def check_heap_sizes(path, content):
    issues = []
    if "384-512" in content or "384–512" in content:
        issues.append("Heap size 384-512 B may be incorrect (mja00: 712 B)")
    if "6400" in content and "State" in content:
        issues.append("State buffer 6400 B may be incorrect (mja00: 8192 B)")
    return issues

def check_freed_memory(path, content):
    issues = []
    if "Freed memory is NOT zeroed" in content or "freed memory stays mapped" in content.lower():
        if "decommit" not in content.lower() and "MADV_FREE" not in content:
            issues.append("Claims freed memory stays mapped without addressing decommit of small blocks")
    return issues

def main():
    print("=== CONTRADICTION DETECTOR ===\n")
    all_issues = []
    for root, _, files in os.walk(DOCS):
        for f in files:
            if not f.endswith(".md"):
                continue
            path = os.path.join(root, f)
            rel = os.path.relpath(path, REPO)
            content = open(path, encoding="utf-8", errors="replace").read()
            issues = []
            issues += check_units_per_em(rel, content)
            issues += check_heap_sizes(rel, content)
            issues += check_freed_memory(rel, content)
            for iss in issues:
                all_issues.append((rel, iss))
                print(f"  [{rel}] {iss}")

    # Known contradictions
    print("\n=== KNOWN CONTRADICTIONS (from issue tracker) ===")
    for doc, keyword, desc in KNOWN:
        print(f"  [{doc}] {keyword}: {desc}")

    print(f"\nTotal detected: {len(all_issues)}")

if __name__ == "__main__":
    main()