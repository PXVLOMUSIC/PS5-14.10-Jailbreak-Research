# Auditoría de Claims vs Source — PS5 Jailbreak Research

**Fecha:** 2026-10-25  
**Fuente:** `WebKit_1400.zip` (Sony, cubre 14.00+)  
**Repo auditado:** `pastawithpesto/PS5-14.10-Jailbreak-Research` (commit 92780e1)

---

## 1. Validaciones confirmadas contra el source

| Claim del repo | Evidencia en source | Veredicto |
|---|---|---|
| CVE-2026-43720: `getContext()` checkea `m_context` antes de `convert<IDLDictionary>` sin re-check | `HTMLCanvasElement.cpp:226` (check) vs `:268` (convert) | ✅ Confirmado |
| IsoHeap OFF en PS5 | `IsoMalloc.h:31-36`: `WTF_MAKE_ISO_ALLOCATED` → `WTF_MAKE_FAST_ALLOCATED` cuando `!USE(ISO_MALLOC)` | ✅ Confirmado |
| `m_canvas` en `CanvasRenderingContext` | `CanvasRenderingContext.h:123`: `CanvasBase& m_canvas` | ✅ Confirmado |
| `ref()`/`deref()` virtuales en `CanvasBase` (slots 4/5) | `CanvasBase.h:68-69` | ✅ Confirmado |
| Fix del CVE ausente en WK-1400 | `WebKit-1400-changes.txt`: no hay modificación en `html/canvas/HTMLCanvasElement.cpp` para re-check post-conversión | ✅ Confirmado (bug vivo) |
| Sony modificó `HTMLCanvasElement.cpp` y `CanvasRenderingContext2DBase.cpp` | changes.txt lista M en ambos | ✅ Confirmado (pero no el fix del CVE) |

---

## 2. Inconsistencias documentales detectadas

### 2.1 Evidencia de sondas no verificable
- `docs/CONFIRMED_VULNS.md` cita **15 sondas** (V415, V429, V430, V432, V460, V461, V527, V548, V550, V562, V573, V589, V630, V632, V641).
- `results/` contiene **solo 5 archivos** y **ninguno** menciona ninguna de esas sondas.
- **Impacto:** Claims de "CONFIRMED on device" no son reproducibles ni auditables desde el repo.
- **Recomendación:** Adjuntar logs de beacon o marcar como "UNVERIFIED".

### 2.2 Gap de offsets para firmware 14.x
- `offsets/` tiene archivos hasta `13.60.js`.
- **No existe** `14.00.js` ni `14.10.js`.
- **Impacto:** Los offsets de kernel/libc/WebKit para 14.0/14.10 no están documentados en el repo.
- **Recomendación:** Crear plantillas y poblarlas con mediciones de hardware.

### 2.3 Claims de tamaño de heap inflados (según issue #21/#27)
- README/CONFIRMED_VULNS afirman context ~384-512 bytes; mja00 midió **712 bytes** (clase bmalloc 768).
- State buffer: repo dice ~3.4 KB con 8 saves; cálculo correcto da **8192 bytes** (clase 95).
- **Impacto:** Los probes de reclaim usan rangos de spray incorrectos.
- **Recomendación:** Corregir números con las mediciones de mja00.

### 2.4 "Freed memory stays mapped" no aplica a todos los tamaños
- Issue #1 (Portablelle) demostró que bloques de ~400 bytes (context class) **se decommiten** (MADV_FREE) o dañan el freelist.
- El claim genérico en README debe re-scoparse a bloques grandes.

### 2.5 BYOB readers
- `ATTACK_SURFACE` los lista como disponibles; 5 docs dicen que BYOB **no está implementado** en 14.10.
- **Recomendación:** Eliminar de la lista de disponibles.

---

## 3. Lo que el source NO puede resolver (requiere hardware/binario)

| Pregunta | Por qué no se puede resolver estáticamente |
|---|---|
| Offsets de kernel (allproc, rootvnode, etc.) | Son del binario del sistema, no del source. |
| Gadgets ROP | Requieren binario desensamblado. |
| Tamaños reales de bmalloc classes en 14.0 | Dependen del allocator compilado; el source da struct sizes pero no class boundaries. |
| Comportamiento de MADV_FREE en runtime | Es comportamiento del kernel, no del source. |
| Leaks reales de punteros heap | Requieren ejecución en consola. |

---

## 4. Recomendaciones para contribuciones

1. **Adjuntar logs**: cada claim "CONFIRMED" debe tener un archivo en `results/` con el beacon log.
2. **Corregir números**: actualizar tamaños de heap con las mediciones de mja00 (712 B context, 8192 B state buffer).
3. **Crear offsets para 14.0/14.10**: plantilla + mediciones.
4. **Re-scopar claims de memoria liberada**: distinguir bloques grandes vs pequeños.
5. **Unificar documentación**: resolver contradicciones (BYOB, heap sizes, etc.).

---

## 5. Aporte propuesto (PR)

- Corregir `docs/CONFIRMED_VULNS.md`: marcar V-refs sin log como "UNVERIFIED".
- Añadir `offsets/14.00.js` y `offsets/14.10.js` (plantillas vacías con estructura).
- Actualizar README con tamaños correctos de heap.
- Añadir sección "Evidence" a cada vuln confirmada.

---
*Generado por análisis estático del source oficial de Sony (WebKit_1400.zip).*
PY