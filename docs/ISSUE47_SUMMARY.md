# Issue #47 Summary — 14.10 WebKit Bootstrap: APNG Base Leak + Live Vtable Offset

**Issue:** https://github.com/pastawithpesto/PS5-14.10-Jailbreak-Research/issues/47  
**Author:** Portablelle  
**Date:** Oct 25, 2026  
**Audit date:** 2026-10-26

---

## Summary

Portablelle has documented the **current state of the 14.10 WebKit bootstrap** chain based on CVE-2026-43720. The UAF and AB(720) reclaim are confirmed on device, and the module base is obtainable via APNG hidden-frame leak (probabilistic). However, the **live vtable offset is still open** — the 13.00 live read vtable (`base+0x31868c0`) has been ruled out on 14.10.

## Proven on 13.00 (testbed)

| Item | Value |
|---|---|
| WebProcess pid | 130 |
| Module base | `0x8034c8000` |
| sizeof(CanvasRenderingContext2D) | 712 (bmalloc 768) |
| sizeof(State) | 448 |
| Live read vtable | `0x31868c0` (different from primary vtable `0x31935c0`) |
| 8-byte read proven | Yes (with live vptr) |
| vptr=0 | Crashes (vptr required for dispatch) |

## Proven on 14.10 (retail, guide browser)

| Item | Status |
|---|---|
| UAF trigger (CVE-2026-43720) | ✅ Confirmed |
| AB(720) reclaim | ✅ Confirmed |
| APNG hidden-frame leak → module base | ✅ Confirmed (probabilistic) |
| Same-page leak + UAF | ✅ Works |
| Live vtable offset | ❌ 0x31868c0 ruled out; others untested |
| 8-byte read | ❌ Not yet (needs valid vptr) |
| Arbitrary R/W | ❌ Not yet |
| Code execution | ❌ Not yet |

## 14.10 Module bases observed

| Run | Base | DF | DW | Leak offset |
|---|---|---|---|---|
| 17/18 | `0x814a05000` | `0x815a70aa0` | `0x815a71540` | 4888/4896 |
| 23/25 | `0x819711000` | `0x81a77caa0` | `0x81a77d540` | 10072/10080 |
| 32 | `0x81a5b5000` | `0x81b620aa0` | `0x81b621540` | 4344/4352 |

**Base changes per WebProcess/session.** Stale base invalidates every vptr/CAND.

## 14.10 vptr candidates (untested on clean base)

| Candidate | Status | Notes |
|---|---|---|
| `base+0x31868c0` | ❌ Ruled out | 13.00 live vtable, not 14.10 |
| `base+0x31867d0` | ⏳ Untested | Same -0xF0 shift as PNG code |
| `base+0x31935c0` | ⏳ Untested | Primary vtable (13.00) |
| `base+0x3193660` | ⏳ Untested | Secondary vtable (13.00) |
| `base+0x3193760` | ⏳ Untested | Not previously tested |
| `base+0x7850` | ⏳ Untested | APNG fingerprint vtable (devonmvfisher, different vtable) |

## Heap layout study (13.00, ps5debug)

- `row_buf` (green frame row) at `0x8801e656c`
- `png_struct` copies at `0x8801ab470`, `0x8801ab8d0`, `0x8801ac6d0`, `0x8801ace70`
- Distance: ~242 KiB. Leak window: 24 KiB. png_struct always outside window.
- Simple decode pressure (sequential/concurrent) does not create high-address png_struct.
- **Leak is probabilistic** — requires fresh heap state or aggressive allocator manipulation.

## Negative results

- Unique tEXt nonce → heap changes → miss.
- sameLen → hit once, then empty.
- Blob URLs → still often empty.
- autoRetry 8/8 empty.
- keepVptr → AB zeroed, vptr lost.
- vptr=0 → crash.
- `base+0x3377370` → in rw segment, not data.rel.ro (not a canvas vtable).

## What is still open

1. **Deterministic 14.10 base leak** — Need png_struct after row_buf within 24 KiB.
2. **14.10 live vtable offset** — Test `base+0x31867d0`, `base+0x31935c0`, `base+0x3193660`, `base+0x3193760`.
3. **14.10 State/rodata offsets** — `base+0x2ee91e8` (13.00 rodata oracle) not verified on 14.10.
4. **14.10 binary** — A `libSceNKWebKit` 14.10 module would give vtable and data.rel.ro layout directly.

## Collaborator findings (devonmvfisher)

- APNG vtable fingerprint: module base + 0x7850 (4 measured bases, 12/12 match, 3/3 device runs on 14.10)
- V736: 16/16 Canvas2D fields mapped through same-type alias, bmalloc class 704 on 14.10
- Save counter offset: +0x220 from context base
- Boot determinism: 3/3 cold boots byte-identical VA maps
- Private collab repo: `devonmvfisher/ps5-collab` (pastawithpesto can add Portablelle as collaborator)

## Cross-reference with our audit

| Our claim | Issue #47 finding | Verdict |
|---|---|---|
| "ASLR Defeat: CONFIRMED (V674)" | APNG leak is probabilistic, not deterministic; base changes per session | ⚠️ "ASLR Defeat" is overstated; should be "Probabilistic base leak" |
| "1,651 heap pointers leaked" | PR #44 replaces this with narrower verified result | ⚠️ V674 claim is unsupported; PR #44's result is verified |
| No offsets for 14.10 | Issue #47 documents 14.10 module bases and candidate vtable offsets | ✅ New data available |
| "Gigacage disabled" | Still runtime-dependent; no device verification | ⚠️ Unverified |
| "Context size 712 B" | Issue #47 confirms 712 on 13.00, 704 bmalloc class on 14.10 | ✅ Confirmed (13.00), slightly different on 14.10 |

## Key takeaway

> **The 14.10 WebKit bootstrap is in progress but not complete.** UAF + reclaim are proven, module base leak is probabilistic, live vtable offset is open. No read/write, no code execution, no jailbreak yet. The community is collaborating (Portablelle, devonmvfisher, pastawithpesto, 0xyg3n) via a private repo.

---

*Generated by audit of issue #47 and related PRs against our existing audit findings.*
PY