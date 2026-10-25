# PLATFORM(PLAYSTATION) Guards — Source Analysis (WebKit_1400)

**Source:** Sony WebKit_1400.zip (covers firmware 14.00+)  
**Analysis date:** 2026-10-25  
**Total guards found:** 47 lines across 31 files

---

## Summary

| Category | Count | Security relevance |
|---|---|---|
| Memory allocator / heap | 18 | Medium — affects reclaim behavior |
| JSC engine / VM | 6 | High — JSC Config unfrozen confirmed |
| bmalloc / libpas | 12 | Medium — allocator internals |
| Network / Inspector | 3 | Low |
| Downstream-only APIs | 4 | Low — Sony extensions |
| Build / platform config | 4 | Low |

**Key finding:** The only guard with direct security-exploitation relevance is `VM.cpp:395` (`disableFreezingForTesting()`), which **disables JSC Config freezing** on PS5. This confirms the repo's claim "JSC Config unfrozen".

---

## Guard-by-Guard Analysis

### 1. VM.cpp:395 — JSC Config Freezing Disabled
```cpp
#if PLATFORM(PLAYSTATION)
    // FIXME: <PLAYSTATION> REMOVE disableFreezingForTesting() call after RNPS no longer needs this behavior
    Config::disableFreezingForTesting();
#endif
if (!g_jscConfig.disabledFreezingForTesting)
    Config::permanentlyFreeze();
```
- **Effect:** On PS5, `disabledFreezingForTesting` is true, so `permanentlyFreeze()` is **skipped**.
- **Security impact:** `g_jscConfig` (including `startOfStructureHeap`) remains **writable** at runtime. This enables type confusion with arbitrary write.
- **Claim validation:** ✅ Confirms repo's "JSC Config unfrozen" claim.

### 2. BPlatform.h:341 — libpas enabled on PS5
```cpp
#if BCPU(ADDRESS64) && (BOS(DARWIN) || (BOS(LINUX) && ...) || BPLATFORM(PLAYSTATION))
#define BENABLE_LIBPAS 1
```
- **Effect:** libpas (bmalloc's allocator) is used on PS5.
- **Security impact:** libpas uses out-of-band bitmap tracking; freed blocks may retain data (relevant for info leak). But small blocks (~400 B) are decommitted (MADV_FREE).
- **Claim validation:** ✅ Confirms "libpas on PS5" claim.

### 3. BPlatform.h:360 — Pthread mutex + release large free disabled
```cpp
#if BPLATFORM(PLAYSTATION)
#define BUSE_PTHREAD_MUTEX 1
#define BUSE_RELEASE_LARGE_FREE 0
#endif
```
- **Effect:** `releaseLargeFree` is disabled on PS5 (large free blocks are not released to OS).
- **Security impact:** Large freed blocks stay mapped → info leak candidate for large allocations. Small blocks still decommit.
- **Claim validation:** ✅ Partially confirms "freed stays mapped" (only for large blocks).

### 4. StructureID.h:50 — Structure heap size 128 MB
```cpp
#elif PLATFORM(PLAYSTATION)
constexpr uintptr_t structureHeapAddressSize = 128 * MB;
```
- **Effect:** Structure heap is 128 MB on PS5 (vs 4 GB default).
- **Security impact:** Smaller structure heap → easier to predict / spray. Relevant for type confusion.

### 5. Heap.h:91 / bmalloc.cpp:151 — releaseLargeFree disabled
```cpp
#if BPLATFORM(PLAYSTATION)
void releaseLargeFree(const LockHolder&);
#endif
// in bmalloc.cpp:
#if BPLATFORM(PLAYSTATION) && BUSE(RELEASE_LARGE_FREE)
    // release large free blocks
#endif
```
- **Effect:** Combined with BUSE_RELEASE_LARGE_FREE=0, large free blocks are NOT released.
- **Security impact:** Confirms large-block info leak potential.

### 6. VMAllocate.h — MAT (Memory Allocation Tracking) logging
```cpp
#if BPLATFORM(PLAYSTATION) && BENABLE(MAT)
    // MatReserveVirtualRange, MatMemoryPoolCommit, MatMemoryPoolDecommit, MatUnmapMemory
#endif
```
- **Effect:** Sony's MAT system tracks virtual memory allocations/deallocations.
- **Security impact:** MAT is for debugging/diagnostics; not a security boundary. But decommit paths (MADV_FREE) are logged.

### 7. IsoMalloc.h:31 — IsoHeap OFF
```cpp
#if USE(SYSTEM_MALLOC) || !USE(ISO_MALLOC)
#define WTF_MAKE_ISO_ALLOCATED(name) WTF_MAKE_FAST_ALLOCATED
#endif
```
- **Effect:** `WTF_MAKE_ISO_ALLOCATED` degrades to FastMalloc on PS5.
- **Security impact:** Enables same-type reclaim (core of CVE-2026-43720).
- **Claim validation:** ✅ Confirms repo's "IsoHeap OFF" claim.

### 8. JSBase.cpp:144,152 — Downstream-only APIs
```cpp
#if PLATFORM(PLAYSTATION) // for downstream-only
    WTF::initializeMainThread();
    RunLoop::run();
#endif
```
- **Effect:** Sony-specific JS API extensions.
- **Security impact:** Low — not relevant to exploitation.

### 9. BAssert.h:35 — NDEBUG assertions on PS5
```cpp
#if defined(NDEBUG) && (BOS(DARWIN) || BPLATFORM(PLAYSTATION))
    // assertions disabled in release
```
- **Effect:** Assertions are compiled out in release builds on PS5.
- **Security impact:** Enables OOB reads/writes that would trap in debug builds (e.g., tee() OOB).

### 10. Other guards (low security relevance)
- `BlockDirectory.cpp:63`: `!PLATFORM(PLAYSTATION)` — skips some block directory logic.
- `RemoteInspectorSocket.cpp:41,262`: Sony-specific inspector socket.
- `LLIntPCRanges.h:46`: LLInt PC ranges for PS5.
- `JSDateMath.cpp:147,501`: Date math fixes.
- `JSLock.cpp:160`: Lock behavior.
- `Options.cpp:452`: Option handling.
- `HTMLSelectElement.cpp:1325`: Select element fix.
- `Environment.cpp:130`: Debug heap disabled.
- `Scavenger.cpp:43,386`: Scavenger behavior.
- `Mutex.h:36,101`: Mutex implementation.
- `LargeMap.cpp/h:91/49`: Large map handling.
- `libpas pas_config.h pas_internal_config.h pas_lock.h pas_utils.h`: allocator internals.
- `testmem/testmem.cpp`: test memory.
- `FunctionOverridesTest.cpp`, `TypedArrayCTest.cpp`: test files.

---

## Security-Relevant Conclusions

1. **JSC Config is unfrozen** (VM.cpp) → type confusion with arb write is viable.
2. **IsoHeap is OFF** (IsoMalloc.h) → same-type reclaim works.
3. **libpas is ON** with out-of-band bitmap tracking → large freed blocks retain data.
4. **Release assertions are OFF** (BAssert.h) → OOB reads that trap in debug builds succeed.
5. **Structure heap is 128 MB** (smaller than default 4 GB) → may aid spraying.
6. **releaseLargeFree is OFF** (BPlatform.h) → large blocks stay mapped.
7. **No guard weakens security checks** beyond the above (all others are logging/platform adaptations).

---

## Claims validated by this analysis

| Repo claim | Guard evidence | Verdict |
|---|---|---|
| "JSC Config unfrozen" | VM.cpp:395 disableFreezingForTesting() | ✅ Confirmed |
| "IsoHeap OFF" | IsoMalloc.h:31 | ✅ Confirmed |
| "libpas on PS5" | BPlatform.h:341 BENABLE_LIBPAS | ✅ Confirmed |
| "PLATFORM(PLAYSTATION) guards are logging-only" | Mixed: most are logging/platform, but VM.cpp:395 and BAssert.h:35 have security relevance | ⚠️ Partially — 2 guards have security impact |
| "22 guards analyzed, all logging-only" | 47 guard lines found, 2 with security relevance | ⚠️ Count and characterization need correction |

---

*Generated by static analysis of Sony's WebKit_1400 source drop.*
PY