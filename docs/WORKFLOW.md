# Workflow: From Probe to Pull Request

**Purpose:** Document the complete workflow for contributing to the PS5 jailbreak research project.  
**Audience:** New contributors who want to help with measurement, documentation, or tooling.

---

## Overview

```
1. Set up environment (DNS + host.py)
2. Run probes on PS5 14.0/14.10
3. Collect beacon logs
4. Analyze results
5. Update documentation
6. Run audit tools
7. Create PR
```

---

## Step 1: Set up environment

### DNS redirect
- Point a domain (e.g., `ps5test.local`) to your PC's IP.
- On PS5: Settings → Network → Set Up Internet Connection → Custom → DNS → Manual → enter your PC's IP.

### Host server
```bash
cd tools/remote-loader
python3 host.py
```
The server listens on port 80 and serves probe files from `probes/`.

### Verify connectivity
- Open `http://your-domain/` on PS5 browser.
- You should see the probe index page.

---

## Step 2: Run probes on PS5

### Available probes
- `probes/recon/` — API fingerprinting, environment measurement
- `probes/canvas-uaf/` — Canvas UAF trigger and aliasing tests
- `probes/canvas-uaf/VCAN-MEASURE.html` — bmalloc class measurement
- `probes/recon/GIGACAGE-PROBE.html` — Gigacage availability
- `probes/recon/JSCCONFIG-PROBE.html` — JSC Config writability
- `probes/recon/BYOB-PROBE.html` — BYOB availability
- `probes/recon/UMTX-PROBE.html` — UMTX stubbed check
- `probes/misc/APNG-LEAK-PROBE.html` — APNG overread leak

### How to run a probe
1. Navigate to `http://your-domain/probes/recon/GIGACAGE-PROBE.html` on PS5.
2. Wait for results (console.log or on-screen output).
3. Note the results.

### Important rules
- **Never trigger UAF more than once per page load** (double-deref = heap corruption).
- **Full reboot between crash-inducing probes** (some crashes leave the browser in a bad state).
- **Document everything** — even negative results.

---

## Step 3: Collect beacon logs

Probes report back via image beacon requests. The host server logs these.

### Where logs are stored
- `results/beacon-logs/` — raw beacon logs
- Each probe has a unique prefix (e.g., VCAN-, V674-, etc.)

### How to save logs
1. After running a probe, check the host server output.
2. Copy the relevant beacon log to `results/beacon-logs/`.
3. Name it consistently: `<probe-id>-<date>.txt` (e.g., `VCAN-MEASURE-2026-10-25.txt`).

---

## Step 4: Analyze results

### Run audit tools
```bash
python tools/claim_audit.py
python tools/contradiction_detector.py
python tools/consolidated_report.py
```

### What to look for
- Does the probe confirm or refute a claim?
- Are there new contradictions?
- Do the results match the source analysis?

### Document findings
- Update `docs/PROBE_INDEX.md` with the new probe and result.
- Update `docs/CONFIRMED_VULNS.md` if a claim is confirmed.
- Update `docs/DEAD_ENDS.md` if a vector is dead.

---

## Step 5: Update documentation

### Rules for documentation
1. **Every "CONFIRMED" claim must have a log in `results/`**.
2. **Mark unverified claims as "UNVERIFIED"** (not "CONFIRMED").
3. **Scope claims appropriately** (e.g., "freed stays mapped" → "large blocks only").
4. **Cite source line numbers** for source-based claims.
5. **Use mja00's measurements** for heap sizes (712 B context, 8192 B state buffer).

### Run audit before committing
```bash
python tools/claim_audit.py
python tools/contradiction_detector.py
```
Both should show 0 new issues.

---

## Step 6: Create a Pull Request

### Fork the repo
1. Go to https://github.com/pastawithpesto/PS5-14.10-Jailbreak-Research
2. Click "Fork".
3. Clone your fork.

### Make changes
1. Create a new branch: `git checkout -b docs/my-contribution`
2. Add/modify files.
3. Commit: `git commit -m "docs: description of changes"`
4. Push: `git push origin docs/my-contribution`

### Create PR
1. Go to your fork on GitHub.
2. Click "Compare & pull request".
3. Use the PR template (`.github/PULL_REQUEST_TEMPLATE.md`).
4. Fill in the checklist.

### PR guidelines
- **Prefer documentation and tooling PRs.**
- **Avoid exploit code, payloads, or ROP chains.**
- **Include evidence** (beacon logs, source references).
- **Run audit tools** before submitting.

---

## Step 7: After PR is merged

- Your contribution is now part of the upstream repo.
- Other contributors can build on your work.
- Update your fork: `git pull upstream master`.

---

## Quick reference

| Task | Command |
|---|---|
| Run claim audit | `python tools/claim_audit.py` |
| Run contradiction detector | `python tools/contradiction_detector.py` |
| Generate consolidated report | `python tools/consolidated_report.py` |
| Start host server | `python tools/remote-loader/host.py` |
| Clone fork | `git clone https://github.com/YOUR_USER/PS5-14.10-Jailbreak-Research.git` |

---

## Key files for contributors

| File | Purpose |
|---|---|
| `docs/CONFIRMED_VULNS.md` | Confirmed vulnerabilities |
| `docs/DEAD_ENDS.md` | Dead ends (49 documented) |
| `docs/PROBE_INDEX.md` | Probe results index |
| `docs/RESEARCH_MAP.md` | Exploitation chain overview |
| `docs/STRATEGY.md` | Current strategy and phases |
| `docs/EXPLOITATION_ENVIRONMENT.md` | Runtime properties |
| `docs/PLATFORM_PLAYSTATION_GUARDS.md` | Guard analysis |
| `docs/AUDIT_REPORT.md` | Audit of claims vs source |
| `docs/CONTRADICTION_REPORT.md` | Contradictions detected |
| `docs/LOCAL_REPRO_GUIDE.md` | Build and repro guide |
| `docs/WORK_SUMMARY.md` | Summary of contributions |
| `docs/CONTRIBUTION_GUIDE.md` | How to contribute |
| `docs/WORKFLOW.md` | This document |
| `offsets/` | Offset files per firmware |
| `probes/` | HTML/JS probes |
| `tools/` | Analysis tools |

---

*This workflow is for defensive research and documentation improvement only.*
PY