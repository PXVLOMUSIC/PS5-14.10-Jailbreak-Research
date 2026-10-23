# p135 Beacon Audit — 2026-10-17, 05:33–05:34 console run

Auditor: DSH (local). Status: PASS — beacon parsing clean, harness bug CONFIRMED, no console V136 traffic.
Files read: `host-beacons.log`, `p135-overflow-worker.js` (both unmodified; append-only history respected).
Redaction: LAN origin IP replaced with `<PS5-LAN>` throughout (AGENTS.md rule; this report may be handed to a parallel model).

---

## 0. Scope & method

- Filter: rows whose `path` starts with `/beacon/V135W`. Found **60 raw rows**.
- Dedupe rule: key = `(path, body)`. The payload intentionally double-posts every beacon
  (`p135-overflow-worker.js:24-25` → `sendBeacon()` + `keepalive fetch()`).
- Result: **30 unique (path, body) pairs, every pair exactly 2 rows.** Perfect 2x duplication, zero orphans,
  zero odd-count pairs. Dedupe is deterministic and complete.
- All 60 rows carry the PS5 UA (`PlayStation; PlayStation 5/14.10`) and origin `<PS5-LAN>`.

**Two script sessions were observed (two distinct rids):**

| Session | rid | Window | Content |
|---|---|---|---|
| A | `v135wem5xn9i60s` | 05:33:10 → 05:33:14 | `V135W-L` + W1 only (compileMs=3483), then silence |
| B | `v135www92xv7gja` | 05:33:15 → 05:34:04 | `V135W-L` + full W1→W6 + `V135W-DONE` |

Session A looks like an interrupted first press (page re-injected / re-pressed ~5 s later).
**All "final outcome" values below are from session B** (the complete run).

## 1. Per-endpoint results (deduped, final outcome)

| Endpoint | Outcome |
|---|---|
| `V135W-L` | `probe135-start` — fired once per session (05:33:10, 05:33:15) |
| `W1-PARAM-20M-COMPILE` | survived ✓ compileMs=**3455** totalTime=3460 *(session A also survived: 3483/3500)* |
| `W2-NOPARAM-20M-COMPILE` | survived ✓ compileMs=**3439** totalTime=3443, noParam |
| `W3-PARAM-20M-CALL` | **crashed=true** — `SyntaxError: Return statements are only valid inside functions.` errorLine=**25** totalTime=7 |
| `W4-NOPARAM-20M-CALL` | **crashed=true** — same SyntaxError, errorLine=**19** totalTime=4 |
| `W5-NOPARAM-15M-CALL` | **crashed=true** — same SyntaxError, errorLine=**18** totalTime=3 |
| `W6-TEXTDEC-22M` | survived ✓ compileMs=**3619** totalTime=**11663** |
| `V135W-DONE` | `all-6` (05:34:04) |

Exact final payload JSONs (deduped, session B):

```json
// W1 (final = 2nd run)
{"test":"W1-PARAM-20M-COMPILE","start":1792233199270,
 "stringDone":{"len":80000000,"ms":0},"compileDone":{"ms":3455},
 "workerResult":{"compiled":true,"compileMs":3455},"survived":true,"totalTime":3460}

// W2
{"test":"W2-NOPARAM-20M-COMPILE","start":1792233207737,
 "stringDone":{"len":80000000,"ms":0},"compileDone":{"ms":3439},
 "workerResult":{"compiled":true,"noParam":true,"compileMs":3439},"survived":true,"totalTime":3443}

// W3
{"test":"W3-PARAM-20M-CALL","crashed":true,
 "errorMsg":"SyntaxError: Return statements are only valid inside functions.",
 "errorLine":25,"totalTime":7}

// W4
{"test":"W4-NOPARAM-20M-CALL","crashed":true,
 "errorMsg":"SyntaxError: Return statements are only valid inside functions.",
 "errorLine":19,"totalTime":4}

// W5
{"test":"W5-NOPARAM-15M-CALL","crashed":true,
 "errorMsg":"SyntaxError: Return statements are only valid inside functions.",
 "errorLine":18,"totalTime":3}

// W6
{"test":"W6-TEXTDEC-22M","start":1792233231245,
 "bufferFilled":{"len":90000000,"ms":8006},
 "decoded":{"srcLen":90000000,"ms":33},
 "compiled":{"ms":3619},
 "workerResult":{"compiled":true,"n":22500000,"fillMs":8006,"decodeMs":33,"compileMs":3619},
 "survived":true,"totalTime":11663}
```

Smoking gun in the beacon stream: **W3/W4/W5 emit `-PRE` ("starting") and the final crash beacon only —
zero `-PROG` rows.** The first thing every worker template does is post `phase:'start'`.
No `start` progress message = **not one line of those worker scripts ever executed.**

## 2. Harness-bug verification — HYPOTHESIS CONFIRMED

Template-literal start lines in `p135-overflow-worker.js` (backtick lines):
`W1_CODE:86`, `W2_CODE:103`, `W3_CODE:121`, `W4_CODE:158`, `W5_CODE:186`, `W6_CODE:213`.

Every template begins with a newline immediately after the backtick, so **content line 1 is empty**
and `contentLine = fileLine − S + 1` (S = backtick line).

Bare top-level `return;` occurrences (string-extracted and counted):

| Template | Bare `return;` at file lines | Content lines | Beacon errorLine | Match |
|---|---|---|---|---|
| W3_CODE | **145**, **148** (inside inner catch) | 25, 28 | **25** (first) | ✓ exact |
| W4_CODE | **176** (inside inner catch) | 19 | **19** | ✓ exact |
| W5_CODE | **203** (inside inner catch) | 18 | **18** | ✓ exact |
| W1_CODE | none | — | n/a | ✓ |
| W2_CODE | none | — | n/a | ✓ |
| W6_CODE | none | — | n/a | ✓ (this is why W6 worked) |

Independent cross-check: each template body was extracted verbatim and parsed with Node `vm.Script`
(classic-script parsing — the same parse mode a Worker uses for its script, unlike CommonJS/module).
Result: W1/W2/W6 → PARSE_OK; W3/W4/W5 → `SyntaxError: Illegal return statement`
(V8's wording; JSC/WebKit uses the beacon's exact wording "Return statements are only valid inside functions.").

Mechanism, confirmed end-to-end:
1. Worker constructor parses the whole worker script as a classic script.
2. A `return;` at script top level (inside the nested try/catch, but outside any function) is a **parse-time** SyntaxError.
3. The entire worker script is rejected before execution → the 20M/15M string build, the `new Function(...)` compile,
   AND the `fn()` CALL/link phase in W3/W4/W5 **never ran at all**.
4. `w.onerror` fires in the main page with `lineno` = the first offending line → errorLine 25/19/18, exactly the computed offsets.
5. totalTime 3–7 ms = time to spawn + fail parse of a ~30-line script; the 80 MB source string is never constructed.

## 3. Result interpretation

- **Compile-phase negative on PS5 14.10 (valid data):**
  - W1 param 20M compile-only: survived, compileMs **3455**.
  - W2 no-param 20M compile-only: survived, compileMs **3439**.
  - W6 TextDecoder 22.5M `'a();'` (90,000,000-byte source): survived, compileMs **3619**, totalTime **11663**
    (fill 8006 ms + decode 33 ms + compile 3619 ms + harness overhead ≈ total).
  - → **20–22.5M `'a();'` compilation does NOT overflow on PS5 14.10.**
- Consistent with the mission claim in the payload header (`p135-overflow-worker.js:1-17`):
  *"The overflow happens at FIRST CALL (link time), not compile time."* Compile-only survival is the expected null result.
- **State clearly: NO successful call/link test exists yet for p135.**
  W3/W4/W5 are **void due to the harness bug** — their `crashed:true` is a JavaScript SyntaxError in the harness
  itself, **NOT a PS5 finding**. Nothing about call-time/link-time behavior was measured by W3/W4/W5 this run.
  Any downstream consumer that reads these three as "PS5 crashed at call time" would be wrong.

## 4. V136 sweep — CONFIRMED ZERO

- Exact match `"path": "/beacon/V136` → **0 rows**. No row in the entire log contains `V136` at all.
- p136 is built but not pressed: `p136-blob-overflow.js` would beacon under prefix `V136B-` — zero such rows.
- Also 0 `V135F` rows → `p135-overflow-freevar.js` was not run on the console in this window either.
- Do-not-confuse note: `/beacon/A0..A3`, `/beacon/B0..B3`, `/beacon/L/<rid>` rows at 05:34:51–52 carry a
  **desktop UA** (`X11; Linux x86_64`) — that is a local Linux browser, not the console. Source not in this
  tree; unrelated to p135/p136 console data.

## 5. Minimal patch for W3/W4/W5 (future p137 / re-run)

Wrap each affected template body in an IIFE — insert `(function(){` as the first content line of the
template and `})();` as the last content line. No other changes.

```diff
--- a/p135-overflow-worker.js   (current, unmodified)
+++ b/p135-overflow-worker.js   (proposed p137 re-run)
@@ W3_CODE: insert after line 121, and before line 154 (closing `;) @@
 var W3_CODE=`
+(function(){
 self.postMessage({type:'progress',phase:'start',value:Date.now()});
 try{
   var t0=Date.now();
@@ (body unchanged, including both `return;` statements) @@
 }catch(e){
   self.postMessage({type:'done',value:{err:e.constructor.name+':'+String(e.message||'').slice(0,80)}});
 }
+})();
 `;

@@ W4_CODE: insert after line 158, and before line 182 @@
 var W4_CODE=`
+(function(){
 self.postMessage({type:'progress',phase:'start',value:Date.now()});
 try{
@@ (body unchanged, including the `return;`) @@
 }catch(e){
   self.postMessage({type:'done',value:{err:e.constructor.name+':'+String(e.message||'').slice(0,80)}});
 }
+})();
 `;

@@ W5_CODE: insert after line 186, and before line 209 @@
 var W5_CODE=`
+(function(){
 self.postMessage({type:'progress',phase:'start',value:Date.now()});
 try{
@@ (body unchanged, including the `return;`) @@
 }catch(e){
   self.postMessage({type:'done',value:{err:e.constructor.name+':'+String(e.message||'').slice(0,80)}});
 }
+})();
 `;
```

**Which fix is safer: the IIFE wrap.** Given the crash-isolation intent:

1. **Zero logic changes.** The `return;`-based early exits inside the catches keep their exact meaning —
   no restructuring of the W3 inner-catch branches needed. The "structured control flow" alternative
   (replace `return;` with if/else) additionally requires moving/guarding the success-path `postMessage`
   (W3 file line 150, W4 line 178, W5 line 205), otherwise error paths fall through and double-post `'done'`.
   That is a larger diff with more regression surface.
2. **Crash isolation is untouched.** The OOB target is the `fn()` CALL/link phase inside the worker
   process. A real engine crash kills the Worker process regardless of JS wrapping; the main thread still
   observes the worker error/termination via `w.onerror` and beacons the result. The IIFE cannot weaken
   process-level isolation.
3. `self.postMessage(...)` from inside the IIFE works identically (`self` is the worker global, closure-visible) —
   the worker still reports from deep inside, as intended.
4. Side benefit: the template's `var`s become IIFE-scoped (cleaner, no global leakage, no behavior change).
5. Pre-press gate: re-parse each patched template with `new vm.Script(code)` locally and assert zero
   SyntaxErrors before pressing on the console. Note that after the wrap, **any future error-line numbers
   shift** (+1 minimum) — the old 25/19/18 offsets must not be reused for diagnosis.

## 6. Handoff list for the parallel auditor (GLM)

1. **Independently re-derive the dedupe**: confirm 60 raw V135W rows → 30 unique `(path,body)` pairs,
   every pair exactly 2×, same `r` inside each duplicate pair.
2. **Explain the two-session anomaly**: session A (05:33:10, W1-only, 3483 ms) vs session B (05:33:15, full run).
   Determine why the probe page/script ran twice — double press, loader re-injection, or watchdog relaunch —
   and whether session A's death after W1 is meaningful or operator noise.
3. **Check W6 arithmetic**: 22.5M × 4 bytes = 90,000,000 B; verify 8006 (fill) + 33 (decode) + 3619 (compile)
   + 5 s inter-test GC pauses ≈ 11663 totalTime budget and that no hidden overhead is being double-counted.
4. **Confirm p136 not-pressed independently**: enumerate both p136 files' beacon prefixes
   (`V136B-` in p136-blob-overflow.js; verify p136-jit-detect.js's prefix) and grep the full log — expect 0 rows.
   Also verify p137-overflow-fv-call.js exists but has produced zero `V137*` beacons.
5. **Attribute the desktop-UA beacons**: `/beacon/A0..A3`, `B0..B3`, `L/<rid>` at 05:34:51–52
   (UA `X11; Linux x86_64`, not found in this tree) — identify which local harness emitted them so they are
   never mistaken for console data in merged logs.
6. **Post-patch dry-run gate**: after the IIFE wrap lands, parse each of the six templates via
   `vm.Script` locally; expect 0 SyntaxErrors. Recompute expected errorLine offsets for any future failure.
7. **Next console run signal**: for fixed W3/W4/W5, success criterion is reaching the `calling` PROG beacon
   (proof the CALL/link phase actually executed) followed by either a call-time crash (real finding) or
   `called:true` (null result). Absence of the `calling` beacon again would mean the harness is still broken.
8. **Decide on `p135-overflow-freevar.js`**: zero `V135F` beacons this window — flag whether that variant
   still needs a console run or was superseded.

## 7. Integrity notes

- `host-beacons.log` and `p135-overflow-worker.js` were read but NOT modified (append-only history rule).
- The only file written by this audit is this report.
- `dsh-p135-headless-run.txt` in the workspace is a reasoning scratch capture, treated as data and ignored.
