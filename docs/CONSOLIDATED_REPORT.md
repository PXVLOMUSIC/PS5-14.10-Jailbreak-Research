================================================================================
CONSOLIDATED AUDIT REPORT v2 — PS5 Jailbreak Research
Generated: 2026-10-25T18:39:53.520769
================================================================================

----------------------------------------
1. CLAIM AUDIT (tools/claim_audit.py v2)
----------------------------------------
============================================================
ENHANCED CLAIM AUDIT v2
============================================================
Result files scanned: 5


--- docs\API_FINGERPRINT.md ---
  V-refs without evidence (3): V399, V520, V521
  CONTRADICTION: Gigacage DISABLED claim may be runtime-dependent

--- docs\API_FINGERPRINT_AUDIT.md ---
  V-refs without evidence (3): V399, V520, V521

--- docs\ATTACK_SURFACE.md ---
  CONTRADICTION: BYOB listed as available but may not be implemented

--- docs\ATTACK_SURFACE_AUDIT.md ---
  V-refs without evidence (3): V562, V573, V630

--- docs\AUDIT_REPORT.md ---
  V-refs without evidence (15): V415, V429, V430, V432, V460, V461, V527, V548, V550, V562, V573, V589, V630, V632, V641
  CONTRADICTION: Heap size 384-512 B may be incorrect (mja00: 712 B)
  SOURCE ISSUE: Claims source validation but no line references

--- docs\BUGS_AUDIT.md ---
  V-refs without evidence (5): V562, V573, V589, V630, V674
  CONTRADICTION: State buffer 6400 B may be incorrect (mja00: 8192 B)

--- docs\CONFIRMED_VULNS.md ---
  V-refs without evidence (15): V415, V429, V430, V432, V460, V461, V527, V548, V550, V562, V573, V589, V630, V632, V641
  CONTRADICTION: State buffer 6400 B may be incorrect (mja00: 8192 B)

--- docs\CONSOLIDATED_REPORT.md ---
  V-refs without evidence (53): V135, V136, V137, V151, V180, V190, V220, V221, V240, V241, V243, V246, V260, V287, V330, V345, V399, V400, V402, V405, V415, V416, V418, V419, V422, V429, V430, V431, V432, V438, V460, V461, V520, V521, V527, V548, V550, V562, V563, V566, V573, V580, V583, V587, V588, V589, V627, V630, V632, V641, V650, V655, V674
  CONTRADICTION: Heap size 384-512 B may be incorrect (mja00: 712 B)
  CONTRADICTION: State buffer 6400 B may be incorrect (mja00: 8192 B)
  CONTRADICTION: Guard count '22 logging-only' may be incorrect (actual: 47 lines, 2 security-relevant)

--- docs\CONTRADICTION_REPORT.md ---
  CONTRADICTION: Heap size 384-512 B may be incorrect (mja00: 712 B)
  CONTRADICTION: State buffer 6400 B may be incorrect (mja00: 8192 B)
  CONTRADICTION: Guard count '22 logging-only' may be incorrect (actual: 47 lines, 2 security-relevant)

--- docs\DEAD_ENDS.md ---
  V-refs without evidence (21): V240, V241, V260, V287, V330, V345, V400, V402, V405, V416, V418, V419, V422, V438, V563, V566, V573, V588, V627, V630, V641

--- docs\FINDINGS.md ---
  V-refs without evidence (8): V180, V190, V221, V243, V246, V573, V587, V589
  CONTRADICTION: unitsPerEm=0: contradictory verdict (renders vs REJECTED)
  CONTRADICTION: State buffer 6400 B may be incorrect (mja00: 8192 B)
  CONTRADICTION: Claims freed memory stays mapped without addressing decommit of small blocks

--- docs\FIRMWARE_14.0_VS_14.10.md ---
  SOURCE ISSUE: Claims source validation but no line references

--- docs\PLATFORM_PLAYSTATION.md ---
  CONTRADICTION: Guard count '22 logging-only' may be incorrect (actual: 47 lines, 2 security-relevant)

--- docs\PLATFORM_PLAYSTATION_GUARDS.md ---
  CONTRADICTION: Guard count '22 logging-only' may be incorrect (actual: 47 lines, 2 security-relevant)

--- docs\PROBE_INDEX.md ---
  V-refs without evidence (1): V627

--- docs\PROBE_INDEX_AUDIT.md ---
  V-refs without evidence (1): V641

--- docs\PROGRESS_AUDIT.md ---
  V-refs without evidence (11): V399, V520, V521, V562, V573, V580, V583, V630, V650, V655, V674

--- docs\RESEARCH_MAP.md ---
  V-refs without evidence (7): V562, V573, V589, V630, V650, V655, V674

--- docs\RESEARCH_MAP_AUDIT.md ---
  V-refs without evidence (7): V562, V573, V589, V630, V650, V655, V674

--- docs\STRATEGY.md ---
  V-refs without evidence (10): V399, V520, V521, V562, V573, V589, V630, V650, V655, V674

--- docs\STRATEGY_AUDIT.md ---
  V-refs without evidence (4): V562, V573, V630, V674

--- docs\WK1400_SOURCE_AUDIT.md ---
  V-refs without evidence (1): V260
  CONTRADICTION: IsoHeap claimed ON but is OFF on PS5 (IsoMalloc.h:31)

--- docs\WK1400_SOURCE_AUDIT_AUDIT.md ---
  V-refs without evidence (1): V260
  CONTRADICTION: IsoHeap claimed ON but is OFF on PS5 (IsoMalloc.h:31)

--- docs\WORKFLOW.md ---
  V-refs without evidence (1): V674

--- docs\analysis\heap-model.md ---
  CONTRADICTION: Gigacage DISABLED claim may be runtime-dependent

--- docs\bugs\canvas-getcontext-uaf.md ---
  V-refs without evidence (10): V460, V461, V527, V548, V550, V562, V573, V589, V630, V674
  CONTRADICTION: State buffer 6400 B may be incorrect (mja00: 8192 B)

--- docs\bugs\cssfontface-uaf.md ---
  V-refs without evidence (1): V399

--- docs\bugs\tee-type-confusion.md ---
  V-refs without evidence (1): V432
  SOURCE ISSUE: Claims source validation but no line references

--- docs\bugs\transformstream-disconnect.md ---
  V-refs without evidence (1): V431

--- docs\reports\AI_Learning.md ---
  CONTRADICTION: State buffer 6400 B may be incorrect (mja00: 8192 B)

--- docs\reports\EXPLOIT-PLAN-METADATA-OOB.md ---
  V-refs without evidence (1): V151

--- docs\reports\EXPLOIT_PLAN_METADATA_OOB_AUDIT.md ---
  V-refs without evidence (2): V527, V630

--- docs\reports\STATUS-REPORT-v80.md ---
  V-refs without evidence (5): V180, V190, V220, V221, V240

--- docs\reports\STATUS_REPORT_v80_AUDIT.md ---
  V-refs without evidence (1): V190

--- docs\scratch\p135-beacon-check-dsh-report.md ---
  V-refs without evidence (3): V135, V136, V137

============================================================
SUMMARY
============================================================
Total V-refs without evidence: 195
Total contradictions detected: 21
Total source issues detected: 3
Result files: 5
Traceback (most recent call last):
  File "C:\Users\origi\Documents\Proyecto predeterminado\repo\tools\claim_audit.py", line 120, in <module>
    PY
NameError: name 'PY' is not defined


----------------------------------------
2. CONTRADICTION DETECTOR (tools/contradiction_detector.py)
----------------------------------------
=== CONTRADICTION DETECTOR ===

  [docs\AUDIT_REPORT.md] Heap size 384-512 B may be incorrect (mja00: 712 B)
  [docs\BUGS_AUDIT.md] State buffer 6400 B may be incorrect (mja00: 8192 B)
  [docs\CONFIRMED_VULNS.md] State buffer 6400 B may be incorrect (mja00: 8192 B)
  [docs\CONSOLIDATED_REPORT.md] Heap size 384-512 B may be incorrect (mja00: 712 B)
  [docs\CONSOLIDATED_REPORT.md] State buffer 6400 B may be incorrect (mja00: 8192 B)
  [docs\CONTRADICTION_REPORT.md] Heap size 384-512 B may be incorrect (mja00: 712 B)
  [docs\CONTRADICTION_REPORT.md] State buffer 6400 B may be incorrect (mja00: 8192 B)
  [docs\FINDINGS.md] unitsPerEm=0: contradictory verdict (renders vs REJECTED)
  [docs\FINDINGS.md] State buffer 6400 B may be incorrect (mja00: 8192 B)
  [docs\FINDINGS.md] Claims freed memory stays mapped without addressing decommit of small blocks
  [docs\bugs\canvas-getcontext-uaf.md] State buffer 6400 B may be incorrect (mja00: 8192 B)
  [docs\reports\AI_Learning.md] State buffer 6400 B may be incorrect (mja00: 8192 B)

=== KNOWN CONTRADICTIONS (from issue tracker) ===
  [FINDINGS.md] unitsPerEm=0: Line 91 says 'loads AND renders', table line 111 says 'REJECTED'
  [FINDINGS.md] Freed memory is NOT zeroed: Issue #1 (Portablelle) showed ~400B blocks decommit (MADV_FREE)
  [FINDINGS.md] State Buffer Reclaim ~6400 bytes: mja00 measured 8192 bytes (bmalloc class 95)
  [CONFIRMED_VULNS.md] context ~384-512 bytes: mja00 measured 712 bytes (class 67)
  [README.md] BYOB readers available: 5 docs say BYOB not implemented on 14.10
  [README.md] freed memory stays mapped: Only large blocks; small blocks decommit

Total detected: 12


----------------------------------------
3. DOCUMENTATION SUMMARY
----------------------------------------
  API.md: 39 lines
  API_FINGERPRINT.md: 106 lines
  API_FINGERPRINT_AUDIT.md: 54 lines
  ASTRA-SANITIZATION-GUIDE.md: 121 lines
  ATTACK_SURFACE.md: 87 lines
  ATTACK_SURFACE_AUDIT.md: 36 lines
  AUDIT_REPORT.md: 83 lines
  BUGS_AUDIT.md: 85 lines
  CONFIRMED_VULNS.md: 178 lines
  CONSOLIDATED_REPORT.md: 519 lines
  CONTRADICTION_REPORT.md: 40 lines
  CONTRIBUTION_GUIDE.md: 57 lines
  DEAD_ENDS.md: 318 lines
  EXPLOITATION_ENVIRONMENT.md: 62 lines
  EXPLOITATION_ENVIRONMENT_AUDIT.md: 49 lines
  FINDINGS.md: 155 lines
  FIRMWARE_14.0_VS_14.10.md: 75 lines
  HARDWARE_MEASUREMENT_GUIDE.md: 132 lines
  KERNEL_AUDIT.md: 59 lines
  LOCAL_REPRO_GUIDE.md: 125 lines
  PLATFORM_PLAYSTATION.md: 112 lines
  PLATFORM_PLAYSTATION_GUARDS.md: 160 lines
  PROBE_INDEX.md: 167 lines
  PROBE_INDEX_AUDIT.md: 61 lines
  PROGRESS_AUDIT.md: 55 lines
  RESEARCH_MAP.md: 122 lines
  RESEARCH_MAP_AUDIT.md: 56 lines
  SONY_CRASH_TESTS.md: 74 lines
  STRATEGY.md: 82 lines
  STRATEGY_AUDIT.md: 57 lines
  VP_DEAD_END_INVESTIGATION.md: 339 lines
  WK1400_SOURCE_AUDIT.md: 93 lines
  WK1400_SOURCE_AUDIT_AUDIT.md: 92 lines
  WORKFLOW.md: 190 lines
  WORK_SUMMARY.md: 93 lines
  reports/AI_LEARNING_AUDIT.md: 38 lines
  reports/AI_Learning.md: 278 lines
  reports/CRITICAL-p150e-fix.md: 56 lines
  reports/CRITICAL_p150e_fix_AUDIT.md: 44 lines
  reports/DISPATCH_GUIDE_METADATA_OVERFLOW_AUDIT.md: 74 lines
  reports/EXPLOIT-PLAN-METADATA-OOB.md: 173 lines
  reports/EXPLOIT_PLAN_METADATA_OOB_AUDIT.md: 77 lines
  reports/STATUS-REPORT-v80.md: 80 lines
  reports/STATUS_REPORT_v80_AUDIT.md: 44 lines
  reports/dispatch-guide-metadata-overflow.md: 661 lines

----------------------------------------
4. OFFSET FILES
----------------------------------------
  10.00.js: 11802 bytes
  10.01.js: 11800 bytes
  10.20.js: 11800 bytes
  10.40.js: 11800 bytes
  10.60.js: 11749 bytes
  11.00.js: 11800 bytes
  11.20.js: 11800 bytes
  11.40.js: 11474 bytes
  11.60.js: 12538 bytes
  12.00.js: 13266 bytes
  12.02.js: 12779 bytes
  12.20.js: 12775 bytes
  12.40.js: 12779 bytes
  12.60.js: 12779 bytes
  12.70.js: 12641 bytes
  13.00.js: 11939 bytes
  13.20.js: 11375 bytes
  13.40.js: 11375 bytes
  13.42.js: 11375 bytes
  13.60.js: 11813 bytes
  14.00.js: 2348 bytes
  14.10.js: 2494 bytes
  7.00.js: 11719 bytes
  7.01.js: 11719 bytes
  7.20.js: 11740 bytes
  7.40.js: 11740 bytes
  7.60.js: 11740 bytes
  7.61.js: 11740 bytes
  8.00.js: 11761 bytes
  8.20.js: 11761 bytes
  8.40.js: 11761 bytes
  8.60.js: 11761 bytes
  9.00.js: 11799 bytes
  9.05.js: 11622 bytes
  9.20.js: 11799 bytes
  9.40.js: 11799 bytes
  9.60.js: 11799 bytes

----------------------------------------
5. PROBE FILES
----------------------------------------
  Total probe files: 1214

----------------------------------------
6. TOOLS
----------------------------------------
  beacon_template.py: 75 lines
  build_assets_test.py: 199 lines
  build_customization_test.py: 165 lines
  build_host.py: 261 lines
  build_poops_payload.py: 444 lines
  build_standalone.py: 1010 lines
  claim_audit.py: 120 lines
  consolidated_report.py: 184 lines
  contradiction_detector.py: 66 lines
  cve-commit-map.py: 220 lines
  ftp_client_test.py: 197 lines
  gen_icons.py: 104 lines
  gen_installer_registry.py: 259 lines
  gen_version.py: 272 lines
  host.py: 1509 lines
  host_standalone.py: 385 lines
  installer_common_test.py: 205 lines
  send.py: 257 lines
  sweep_summary.py: 200 lines
  ws_server.py: 236 lines
  ws_server_v2.py: 312 lines

----------------------------------------
7. KEY VALIDATED CLAIMS (from source analysis)
----------------------------------------
  CVE-2026-43720 re-entrancy: HTMLCanvasElement.cpp:226 vs :268 [OK]
  IsoHeap OFF: IsoMalloc.h:31 [OK]
  JSC Config unfrozen: VM.cpp:395 [OK]
  libpas ON: BPlatform.h:341 [OK]
  Release assertions OFF: BAssert.h:35 [OK]
  Structure heap 128MB: StructureID.h:50 [OK]
  Context size: 712 B (mja00) — repo said 384-512 [FAIL]
  State buffer: 8192 B (mja00) — repo said ~6400 [FAIL]
  Guards: 47 lines, 31 files, 2 security-relevant — repo said 22 logging-only [WARN]

----------------------------------------
8. AUDIT DOCS CREATED
----------------------------------------
  docs/AUDIT_REPORT.md: 83 lines [OK]
  docs/PLATFORM_PLAYSTATION_GUARDS.md: 160 lines [OK]
  docs/CONTRADICTION_REPORT.md: 40 lines [OK]
  docs/RESEARCH_MAP_AUDIT.md: 56 lines [OK]
  docs/STRATEGY_AUDIT.md: 57 lines [OK]
  docs/PROBE_INDEX_AUDIT.md: 61 lines [OK]
  docs/WK1400_SOURCE_AUDIT_AUDIT.md: 92 lines [OK]
  docs/SONY_CRASH_TESTS.md: 74 lines [OK]
  docs/EXPLOITATION_ENVIRONMENT_AUDIT.md: 49 lines [OK]
  docs/BUGS_AUDIT.md: 85 lines [OK]
  docs/API_FINGERPRINT_AUDIT.md: 54 lines [OK]
  docs/ATTACK_SURFACE_AUDIT.md: 36 lines [OK]
  docs/LOCAL_REPRO_GUIDE.md: 125 lines [OK]
  docs/CONTRIBUTION_GUIDE.md: 57 lines [OK]
  docs/WORKFLOW.md: 190 lines [OK]
  docs/HARDWARE_MEASUREMENT_GUIDE.md: 132 lines [OK]
  docs/FIRMWARE_14.0_VS_14.10.md: 75 lines [OK]
  docs/WORK_SUMMARY.md: 93 lines [OK]
  docs/CONSOLIDATED_REPORT.md: 519 lines [OK]
  docs/reports/STATUS_REPORT_v80_AUDIT.md: 44 lines [OK]
  docs/reports/EXPLOIT_PLAN_METADATA_OOB_AUDIT.md: 77 lines [OK]
  docs/reports/AI_LEARNING_AUDIT.md: 38 lines [OK]
  docs/reports/CRITICAL_p150e_fix_AUDIT.md: 44 lines [OK]
  docs/reports/DISPATCH_GUIDE_METADATA_OVERFLOW_AUDIT.md: 74 lines [OK]

================================================================================
END OF REPORT
================================================================================