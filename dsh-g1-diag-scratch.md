# DSH-G1-DIAG scratch (leg DSH-G1-DIAG-1, 2026-10-15 14:16→14:4x)

IMMEDIATE-FLUSH. Leg: diagnosis U2 crash-before-beacon (FA-v5 G1 plant) + FA-v6 design.

## Inventory (on disk)
- loader: fake-stream-v5.html (87 L), fake-stream-v6.html (94 L, index dispatch actual), host-beacons.log (181 KB, last 14:16:40), cand-a-tee-livetest.html.
- WK1200 tree: 14.10-bid/wk1200-source/WebKit-1200/Source (verificado). Board: 14.10-bid/SWARM-BOARD.md.
- RIVAL: 14.10-bid/dsh-g1-diag-final.md (97 L, 14:25) ya existe — cross-check hecho, converge + 2 correcciones mías.

## Evidence (log + árbol, coordenadas verificadas)
- LOG run fv5mv9x6t7d-891g: C0A/C0B → 1A/1B BUGLIVE=true → V-U2A 14:16:40 → SILENCIO (no U2B/U2E/P1/G1/U1/Z) = WebProcess murió en U2.
- fake-stream-v5.html:26-36 (v(): B post-work, E solo catch JS), :50 (U2 llamada con 3 args: poisonFn=G1-fn, work=undefined) ⇒ el plant entero corrió DENTRO de v():28 (poison-install) → fase2 rs2.tee() under-yield → SEGV ahí.
- bindings/js/InternalReadableStream.cpp:180-197: convert(:191) → ASSERT(size==2)(:192) → SIN RETURN_IF_EXCEPTION → *results[0]/[1].get()(:195). fromObject(:76)=new InternalReadableStream(globalObject,object) SIN type-check. Contraste TransformStream.cpp:114-117.
- ReadableStreamInternals.js:585-631: builtin retorna [branch1,branch2] (:631) — el array iterado ES del builtin; el poison corre con this=[branch1,branch2].
- JSDOMConvertSequences.h:42-63 + IteratorOperations.h:62-103 (FastArray bypass solo con watchpoint intacto) + JSDOMConvertObject.h:39-49 (isObject guard, throw → sin append).
- WTF Vector.h:1150-1153 expandCapacity = reserveCapacity(max(n,max(16,cap+cap/4+1))) ⇒ vector INNER = 16×8B = 128 B clase-128. Vector.h:1313-1322 reserveInitialCapacity(N) aloca EXACTO N (bypass minCapacity) ⇒ vector OUTER (ReadableStream.cpp:74-87, reserveInitialCapacity(2)) = 16 B clase-16 — AHÍ nace el "16-B" de dshv5 (vector equivocado).
- Vector.h VectorDestructor<true>: corre ~T por elemento en teardown (canMoveWithMemcpy SOLO afecta moves). heap/Strong.h:75-78 ~Strong(){clear();} ⇒ slot[0..size-1] NULLED antes del free ⇒ slot[1] reusado = NULL siempre ⇒ *nullptr. G1/V5 stale-wrap = REFUTADO por árbol.
- bmalloc/Sizes.h:49-57: chunk 1 MB, smallLine 256, smallMax 32 kB ✔ (cita rival OK).
- OptionsPlayStation.cmake:198-207: JIT/DFG/FTL OFF, IsoMalloc OFF (bmalloc default).
- SequenceConverter<IDLObject> = 2 sites ✔; tee callers = 2 (ReadableStream.cpp:76, FetchBody.cpp:317) ✔.
- asObject (JSObject.h:1389-1399): jsCast=static_cast, nunca null (coherente dshpsyv4).

## Verdicts (final)
- ROOT-CAUSE (apilado): (1) SEGV nativo síncrono en :195 (vector size-1; ASSERT-only; sin RETURN_IF_EXCEPTION) — B inalcanzable, try/catch no captura fault; (2) ARIDAD v5:50: poisonFn=G1-fn ejecutó el plant en v():28 (work undefined; U2B imposible aun sin crash); (3) H3=flaw: chosen nunca yielded (poison devuelve this[0],this[1],{}); dtor-nulling hace el stale-wrap irrealizable; el crash observado = null deref (fresh o reuso-nulleado).
- H1✗ (restore JS puro, post-fault) · H2✗ (V-U2A completo+ordenado ⇒ sync XHR OK) · H3✓-corregido (clase-128 inner / clase-16 outer; dtor nulling).
- WRAP-PRIMITIVE correcto = substitución SAME-TEE (over-yield reemplazando yield#2: results[1]=chosen IN-CALL, sin reuse) — S5 del FA-v6. Reuse-path = crash-oracle SOLO.
- FA-v6: rival 10 etapas OK + añadir S5-substitution + heartbeat HB 2s + regla server (HB-gap>4s + L respawn) + 4-args SIEMPRE en v().
- ALERTA: fake-stream-v6.html actual = G5 (string under-yield crash) en posición 5 ⇒ battery-killer; reordenar S0-S9 antes del press.

Products: final rival ya en 14.10-bid/dsh-g1-diag-final.md (converge; le appendée §9 cross-check + correcciones). Board: ACK + enmienda.
