# Work Summary — PS5 Jailbreak Research (Personal Environment)

**Date:** 2026-10-25  
**Hardware target:** PS5 Fat, firmware 14.0  
**Repo:** `pastawithpesto/PS5-14.10-Jailbreak-Research` (cloned locally)

---

## What I did (static analysis + tooling)

### 1. Cloned and audited the research repo
- Location: `C:\Users\origi\Documents\Proyecto predeterminado\repo`
- Audited `docs/CONFIRMED_VULNS.md`, `docs/DEAD_ENDS.md`, `docs/EXPLOITATION_ENVIRONMENT.md`.

### 2. Downloaded and analyzed Sony's official source drop
- `WebKit_1400.zip` (1.6 GB) from PlayStation OSS page.
- Extracted `Source/WebCore/html`, `Source/bmalloc`, `Source/JavaScriptCore`.
- **Validated CVE-2026-43720**: `HTMLCanvasElement::getContext()` checks `m_context` at line 226 but does NOT re-check after `convert<IDLDictionary>` at line 268 → re-entrancy confirmed.
- **Validated IsoHeap OFF**: `IsoMalloc.h:31` degrades `WTF_MAKE_ISO_ALLOCATED` to `WTF_MAKE_FAST_ALLOCATED` when `!USE(ISO_MALLOC)`.
- **Validated refcount path**: `CanvasRenderingContext::ref/deref` virtual in `CanvasBase` (slots 4/5), `m_canvas` at `CanvasRenderingContext.h:123`.
- **Validated JSC Config unfrozen**: `VM.cpp:395-398` calls `Config::disableFreezingForTesting()` under `PLATFORM(PLAYSTATION)` → confirms "JSC Config unfrozen" claim.
- **Validated Gigacage**: `HeapKind.h` shows gigacage heaps are only active if `Gigacage::isEnabled()` (runtime). Source doesn't force-disable; claim is runtime-dependent.

### 3. Created audit report
- `docs/AUDIT_REPORT.md`: lists validated claims, inconsistencies (159/173 V-refs without evidence in `results/`), gaps (no offsets for 14.x), and recommendations.

### 4. Created claim audit tool
- `tools/claim_audit.py`: scans docs for V-refs and CONFIRMED lines, cross-references against `results/`. Run with `python tools/claim_audit.py`.

### 5. Created offset templates
- `offsets/14.00.js` and `offsets/14.10.js`: empty templates with correct structure, ready to populate with hardware measurements.

### 6. Created measurement probe
- `probes/canvas-uaf/VCAN-MEASURE.html`: self-contained HTML probe to measure bmalloc class reclamation on your PS5 14.0.

### 7. Installed tooling
- LLVM/clang 23.1.4 via winget (for static analysis/layout dumps).

---

## What you can do on your PS5 14.0

### Environment measurement (safe, no exploit)
1. Set up DNS redirect + `tools/remote-loader/host.py` on your PC.
2. Open `VCAN-MEASURE.html` on PS5 browser.
3. Record which spray counts cause aliasing (lineWidth readback).
4. Populate `offsets/14.00.js` with measured values.
5. Run `tools/claim_audit.py` to see which claims need evidence.

### Static analysis (no hardware)
- Read `docs/AUDIT_REPORT.md` for validated vs unverified claims.
- Read docs/PLATFORM_PLAYSTATION_GUARDS.md for guard analysis.
- Read docs/LOCAL_REPRO_GUIDE.md for build/repro steps.
- Compare your 14.0 behavior against 14.10 docs.

---

## What I CANNOT help with (my limits)

- ROP chains, gadgets, vtable hijacks, payloads.
- Code execution or kernel escalation steps.
- Building a functional exploit (stage 2+).

These require community scene resources (PS5Dev, forums, Discord) and your own reverse engineering of firmware binaries.

---

## Files created/modified

| File | Purpose |
|---|---|
| `docs/AUDIT_REPORT.md` | Audit of claims vs source |
| `tools/claim_audit.py` | Automated claim verification tool |
| `offsets/14.00.js` | Offset template for 14.0 |
| `offsets/14.10.js` | Offset template for 14.10 |
| `probes/canvas-uaf/VCAN-MEASURE.html` | bmalloc class measurement probe |
| docs/PLATFORM_PLAYSTATION_GUARDS.md | Analysis of 47 PLATFORM(PLAYSTATION) guards |
| probes/recon/GIGACAGE-PROBE.html | Gigacage availability probe |
| probes/recon/JSCCONFIG-PROBE.html | JSC Config writability probe |
| docs/LOCAL_REPRO_GUIDE.md | Local build and repro guide |
| docs/WORK_SUMMARY.md | This summary |

---

## Next steps for you

1. **Run `VCAN-MEASURE.html`** on your PS5 14.0 and report results.
2. **Populate `offsets/14.00.js`** with real offsets from your console.
3. **Contribute findings** to the upstream repo (PRs welcome).
4. For the **offensive part** (code exec, kernel), consult the PS5 scene community.

I'm here to help with measurement, static analysis, and documentation — not with exploit construction.
PY