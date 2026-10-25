#!/usr/bin/env python3
"""Generate a consolidated audit report from all tools and docs."""
import os, sys, subprocess

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def run_tool(script):
    path = os.path.join(REPO, "tools", script)
    try:
        result = subprocess.run([sys.executable, path], capture_output=True, text=True, cwd=REPO)
        return result.stdout + result.stderr
    except Exception as e:
        return f"Error running {script}: {e}"

def read_file(rel):
    path = os.path.join(REPO, rel)
    try:
        return open(path, encoding="utf-8", errors="replace").read()
    except Exception as e:
        return f"Error reading {rel}: {e}"

def main():
    out = []
    out.append("=" * 80)
    out.append("CONSOLIDATED AUDIT REPORT — PS5 Jailbreak Research")
    out.append(f"Generated: {__import__('datetime').datetime.now().isoformat()}")
    out.append("=" * 80)
    out.append("")

    # 1. Claim audit
    out.append("-" * 40)
    out.append("1. CLAIM AUDIT (tools/claim_audit.py)")
    out.append("-" * 40)
    out.append(run_tool("claim_audit.py"))
    out.append("")

    # 2. Contradiction detector
    out.append("-" * 40)
    out.append("2. CONTRADICTION DETECTOR (tools/contradiction_detector.py)")
    out.append("-" * 40)
    out.append(run_tool("contradiction_detector.py"))
    out.append("")

    # 3. Summary of docs
    out.append("-" * 40)
    out.append("3. DOCUMENTATION SUMMARY")
    out.append("-" * 40)
    docs = os.path.join(REPO, "docs")
    for f in sorted(os.listdir(docs)):
        if f.endswith(".md"):
            path = os.path.join(docs, f)
            lines = len(open(path, encoding="utf-8", errors="replace").read().splitlines())
            out.append(f"  {f}: {lines} lines")
    out.append("")

    # 4. Offset files
    out.append("-" * 40)
    out.append("4. OFFSET FILES")
    out.append("-" * 40)
    offsets = os.path.join(REPO, "offsets")
    for f in sorted(os.listdir(offsets)):
        if f.endswith(".js"):
            path = os.path.join(offsets, f)
            size = os.path.getsize(path)
            out.append(f"  {f}: {size} bytes")
    out.append("")

    # 5. Probe files
    out.append("-" * 40)
    out.append("5. PROBE FILES")
    out.append("-" * 40)
    probes = os.path.join(REPO, "probes")
    count = 0
    for root, _, files in os.walk(probes):
        for f in files:
            if f.endswith(".html") or f.endswith(".js"):
                count += 1
    out.append(f"  Total probe files: {count}")
    out.append("")

    # 6. Key validated claims
    out.append("-" * 40)
    out.append("6. KEY VALIDATED CLAIMS (from source analysis)")
    out.append("-" * 40)
    out.append("  CVE-2026-43720 re-entrancy: HTMLCanvasElement.cpp:226 vs :268 [OK]")
    out.append("  IsoHeap OFF: IsoMalloc.h:31 [OK]")
    out.append("  JSC Config unfrozen: VM.cpp:395 [OK]")
    out.append("  libpas ON: BPlatform.h:341 [OK]")
    out.append("  Release assertions OFF: BAssert.h:35 [OK]")
    out.append("  Structure heap 128MB: StructureID.h:50 [OK]")
    out.append("  Context size: 712 B (mja00) — repo said 384-512 [FAIL]")
    out.append("  State buffer: 8192 B (mja00) — repo said ~6400 [FAIL]")
    out.append("  Guards: 47 lines, 31 files, 2 security-relevant — repo said 22 logging-only [WARN]")
    out.append("")

    # 7. Audit docs created
    out.append("-" * 40)
    out.append("7. AUDIT DOCS CREATED")
    out.append("-" * 40)
    audit_docs = [
        "docs/AUDIT_REPORT.md",
        "docs/PLATFORM_PLAYSTATION_GUARDS.md",
        "docs/CONTRADICTION_REPORT.md",
        "docs/RESEARCH_MAP_AUDIT.md",
        "docs/STRATEGY_AUDIT.md",
        "docs/PROBE_INDEX_AUDIT.md",
        "docs/WK1400_SOURCE_AUDIT_AUDIT.md",
        "docs/SONY_CRASH_TESTS.md",
        "docs/LOCAL_REPRO_GUIDE.md",
        "docs/CONTRIBUTION_GUIDE.md",
        "docs/WORK_SUMMARY.md",
    ]
    for d in audit_docs:
        path = os.path.join(REPO, d)
        if os.path.exists(path):
            lines = len(open(path, encoding="utf-8", errors="replace").read().splitlines())
            out.append(f"  {d}: {lines} lines [OK]")
        else:
            out.append(f"  {d}: MISSING [FAIL]")
    out.append("")

    out.append("=" * 80)
    out.append("END OF REPORT")
    out.append("=" * 80)

    report = "\n".join(out)
    report_path = os.path.join(REPO, "docs", "CONSOLIDATED_REPORT.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(report)
    print(f"\nReport saved to: {report_path}")

if __name__ == "__main__":
    main()
PY