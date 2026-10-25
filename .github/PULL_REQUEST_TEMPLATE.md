# Pull Request Template — PS5 Jailbreak Research

## Title format
```
docs: <short description>  OR  probes: <short description>  OR  tools: <short description>
```

## Checklist (must be completed before submitting)

### Evidence
- [ ] All claims of "CONFIRMED on device" have a corresponding beacon log in `results/`
- [ ] V-refs cited in docs have matching log files (run `tools/claim_audit.py` to verify)
- [ ] Probe results are reproducible (include probe filename and device firmware version)
- [ ] No claims of "CONFIRMED" without device evidence (mark as "UNVERIFIED" or "DESIGNED" instead)

### Documentation
- [ ] No internal contradictions (run `tools/contradiction_detector.py`)
- [ ] Heap sizes and offsets match mja00's measurements (context=712B, state buffer=8192B) or are explicitly marked as unmeasured
- [ ] "Freed memory stays mapped" is scoped to large blocks only
- [ ] BYOB is not listed as available (not implemented on 14.10)
- [ ] Guard counts match actual source (47 lines, 31 files, 2 security-relevant)

### Code/Probes
- [ ] Probes are self-contained HTML files
- [ ] Probes report results via console.log or beacon
- [ ] No hardcoded IPs or personal data
- [ ] No exploit payloads or ROP chains

### Offsets
- [ ] New offset files follow the structure of `offsets/13.60.js`
- [ ] Offset values are measured on device (not estimated)
- [ ] Firmware version is specified in the offset file

### Source analysis
- [ ] Claims about source are verifiable against `WebKit_1400.zip`
- [ ] Line numbers are cited for source claims
- [ ] `PLATFORM(PLAYSTATION)` guards are referenced by file and line

---

## Description template

### What does this PR do?
<!-- Brief description -->

### What is the evidence?
<!-- Link to beacon logs, source files, or issue references -->

### What claims are being added/changed?
<!-- List of claims and their evidence status -->

### Checklist
<!-- Copy the checklist above and check all that apply -->

---

## Reviewer notes
- Prefer documentation and tooling PRs.
- Reject PRs that add exploit code, payloads, or ROP chains.
- Verify V-refs against `results/` before merging.
- Run `tools/claim_audit.py` and `tools/contradiction_detector.py` on the PR branch.

---

*Template created as part of the documentation audit effort.*
PY