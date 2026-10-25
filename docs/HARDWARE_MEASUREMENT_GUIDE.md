# Hardware Measurement Guide — PS5 14.0

**Purpose:** Step-by-step guide for measuring your PS5 14.0 environment (offsets, bmalloc classes, API availability).  
**Hardware:** PS5 Fat, firmware 14.0  
**Prerequisites:** PC on same network, Python 3, Git.

---

## Phase 1: Environment Setup

### 1.1 Configure DNS
1. On PS5: Settings → Network → Set Up Internet Connection → Custom.
2. DNS: Manual → Primary DNS = your PC's IP.
3. Test: Open `http://your-pc-ip/` on PS5 browser. Should show a page.

### 1.2 Start host server
```bash
cd tools/remote-loader
python3 host.py
```
Server listens on port 80. Serves files from `probes/`.

### 1.3 Verify connectivity
- Open `http://your-pc-ip/probes/recon/GIGACAGE-PROBE.html` on PS5.
- Results should appear on screen and in console.

---

## Phase 2: API Fingerprinting

### 2.1 Run API fingerprint probe
- Open `http://your-pc-ip/docs/API_FINGERPRINT.md` (reference) or run `probes/recon/` probes.
- Record which APIs are available.

### 2.2 Run specific probes
| Probe | URL | What it measures |
|---|---|---|
| GIGACAGE-PROBE | `/probes/recon/GIGACAGE-PROBE.html` | Gigacage availability |
| BYOB-PROBE | `/probes/recon/BYOB-PROBE.html` | BYOB availability |
| UMTX-PROBE | `/probes/recon/UMTX-PROBE.html` | UMTX stubbed check |
| JSCCONFIG-PROBE | `/probes/recon/JSCCONFIG-PROBE.html` | JSC Config writability |
| VCAN-MEASURE | `/probes/canvas-uaf/VCAN-MEASURE.html` | bmalloc class measurement |
| APNG-LEAK-PROBE | `/probes/misc/APNG-LEAK-PROBE.html` | APNG overread leak |

### 2.3 Record results
For each probe, note:
- Console output (copy from browser dev tools or on-screen log).
- Crash/no crash.
- Any beacons received by host server.

---

## Phase 3: bmalloc Class Measurement

### 3.1 Run VCAN-MEASURE.html
1. Open the probe on PS5.
2. Observe which spray counts cause aliasing (lineWidth readback).
3. Record the results.

### 3.2 Interpret results
- If spray=500 causes aliasing → context class is reclaimable with 500 contexts.
- If spray=500 crashes → context class may be different on 14.0.
- If no aliasing → trigger may not work on 14.0.

### 3.3 Populate offsets/14.00.js
Use the template in `offsets/14.00.js` and fill in measured values.

---

## Phase 4: Offset Measurement

### 4.1 WebKit offsets
These require binary analysis (Ghidra/IDA) of the WebProcess ELF. Without a decrypted firmware dump, you can only measure:
- Host constructor candidates (via crash oracle).
- memset import (via known patterns).

### 4.2 Kernel offsets
These require a decrypted firmware dump or a jailbroken 14.0 console. Without these, leave as 0 in `offsets/14.00.js`.

### 4.3 What to measure on device
- bmalloc class sizes (via VCAN-MEASURE).
- API availability (via recon probes).
- Crash behavior (via canvas UAF trigger).
- Leak behavior (via APNG probe).

---

## Phase 5: Document and Contribute

### 5.1 Save beacon logs
Copy host server output to `results/beacon-logs/` with consistent naming.

### 5.2 Update documentation
- Add results to `docs/PROBE_INDEX.md`.
- Update `offsets/14.00.js` with measured values.
- Mark claims as "CONFIRMED" or "UNVERIFIED" in docs.

### 5.3 Run audit tools
```bash
python tools/claim_audit.py
python tools/contradiction_detector.py
python tools/consolidated_report.py
```

### 5.4 Create PR
Follow `docs/WORKFLOW.md` for PR creation.

---

## Quick reference

| Task | Command/URL |
|---|---|
| Start host | `python3 tools/remote-loader/host.py` |
| Run probe | `http://your-pc-ip/probes/recon/GIGACAGE-PROBE.html` |
| Claim audit | `python tools/claim_audit.py` |
| Contradiction check | `python tools/contradiction_detector.py` |
| Consolidated report | `python tools/consolidated_report.py` |

---

## Safety notes

- **Full reboot between crash-inducing probes.**
- **Never trigger UAF more than once per page load.**
- **Document everything, including negative results.**
- **Do not connect to PSN** with a modified console.

---

*This guide is for defensive research on personally owned hardware.*
PY