#!/usr/bin/env python3
"""Enhanced claim audit v2: V-refs + contradictions + source validation."""
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

def check_vrefs(content, all_result_content):
    issues = []
    for m in re.finditer(r"V\d{3,4}", content):
        v = m.group(0)
        if v not in all_result_content:
            issues.append(v)
    return list(set(issues))

def check_contradictions(path, content):
    issues = []
    # unitsPerEm
    if "unitsPerEm=0 loads AND renders" in content and "unitsPerEm=0 | REJECTED" in content:
        issues.append("unitsPerEm=0: contradictory verdict (renders vs REJECTED)")
    # heap sizes
    if "384-512" in content or "384–512" in content:
        issues.append("Heap size 384-512 B may be incorrect (mja00: 712 B)")
    if "6400" in content and ("State" in content or "state" in content):
        issues.append("State buffer 6400 B may be incorrect (mja00: 8192 B)")
    # freed memory
    if "Freed memory is NOT zeroed" in content or "freed memory stays mapped" in content.lower():
        if "decommit" not in content.lower() and "MADV_FREE" not in content:
            issues.append("Claims freed memory stays mapped without addressing decommit of small blocks")
    # BYOB
    if "BYOB readers" in content and "available" in content.lower():
        if "not implemented" not in content.lower():
            issues.append("BYOB listed as available but may not be implemented")
    # Gigacage
    if "Gigacage" in content and "DISABLED" in content:
        if "runtime" not in content.lower():
            issues.append("Gigacage DISABLED claim may be runtime-dependent")
    # IsoHeap
    if "IsoHeap isolation confirmed" in content or "IsoHeap is ON" in content:
        issues.append("IsoHeap claimed ON but is OFF on PS5 (IsoMalloc.h:31)")
    # Guard count
    if "22" in content and "guard" in content.lower() and "logging-only" in content.lower():
        issues.append("Guard count '22 logging-only' may be incorrect (actual: 47 lines, 2 security-relevant)")
    return issues

def check_source_claims(path, content):
    """Check if source-based claims have line references."""
    issues = []
    # Check for claims without source references
    if "source" in content.lower() and "line" not in content.lower() and "src" not in content.lower():
        if "confirmed" in content.lower():
            issues.append("Claims source validation but no line references")
    return issues

def main():
    result_texts = collect_result_text()
    all_result_content = "\n".join(t for _, t in result_texts)

    print("=" * 60)
    print("ENHANCED CLAIM AUDIT v2")
    print("=" * 60)
    print(f"Result files scanned: {len(result_texts)}")
    print()

    total_vrefs = 0
    total_no_ev = 0
    total_contra = 0
    total_source = 0

    for root, _, files in os.walk(DOCS):
        for f in files:
            if not f.endswith(".md"):
                continue
            path = os.path.join(root, f)
            rel = os.path.relpath(path, REPO)
            content = open(path, encoding="utf-8", errors="replace").read()

            vrefs = check_vrefs(content, all_result_content)
            contras = check_contradictions(rel, content)
            source_issues = check_source_claims(rel, content)

            if vrefs or contras or source_issues:
                print(f"\n--- {rel} ---")
                if vrefs:
                    print(f"  V-refs without evidence ({len(vrefs)}): {', '.join(sorted(vrefs))}")
                    total_no_ev += len(vrefs)
                if contras:
                    for c in contras:
                        print(f"  CONTRADICTION: {c}")
                    total_contra += len(contras)
                if source_issues:
                    for s in source_issues:
                        print(f"  SOURCE ISSUE: {s}")
                    total_source += len(source_issues)
            total_vrefs += len(vrefs)

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total V-refs without evidence: {total_no_ev}")
    print(f"Total contradictions detected: {total_contra}")
    print(f"Total source issues detected: {total_source}")
    print(f"Result files: {len(result_texts)}")

if __name__ == "__main__":
    main()
PY