# PS5 14.10 Jailbreak Research

WebKit jailbreak research for PlayStation 5 firmware 14.10. All data comes from probes that ran on the actual console.

> **Disclaimer:** Authorized security research on personally owned hardware. For educational and research purposes only.

## Target

Validated on device (p163).

| Property | Value |
|----------|-------|
| Platform | PlayStation 5 |
| Firmware | 14.10 |
| Browser | Safari 17.0 / AppleWebKit 605.1.15 |
| JIT | Disabled (LLInt only) |
| Cores | 4 |
| Display | 1920x1080 |

**Available:** Workers, WebSocket, fetch, SubtleCrypto, Canvas 2D, ReadableStream, ResizableArrayBuffer, WeakRef, FinalizationRegistry, Proxy, BigInt, structuredClone

**Not available:** WebAssembly, SharedArrayBuffer, WebGL, WebAudio, IndexedDB, ServiceWorker

## Source Reference

The PS5 WebKit binary is not publicly available. We use the open source **WebKit-1200** snapshot (December 2023) as a reference for structure layouts, function internals, and allocator behavior. This is the closest matching version to the Safari 17.0 / AppleWebKit 605.1.15 engine on the console. All assumptions from source are then validated on device with probes.

## The Bug

JavaScriptCore Bug 317632. `UnlinkedMetadataTable::finalize()` uses an `unsigned` accumulator with no overflow check.

```
38,348,816 calls x 112 bytes = 4,295,067,392
uint32 wraps to 100,096 bytes
```

Allocator reserves 100KB. The interpreter writes 4.29GB forward into heap.

## Probes

| Probe | What it does | Result |
|-------|-------------|--------|
| p141 | Overflow test (wrong stride) | SIGSEGV |
| p142 | Correct stride (112) | Overflow triggers |
| p143 | Targets before buffer | No corruption, sweep is forward only |
| p144 | Bait and switch | Forward write confirmed |
| p146 | Worker .length polling | **All 14 strings corrupted, .length = 81400** |
| p147, p148 | Substring and main thread views | StringImpl data intact, JSString.m_fiber corrupted |
| p149g | Read after compile, before call | Overflow is at runtime not compile time |
| p150 | Throwing callback | OOB read crashes before callback |
| p156 | charCodeAt scan | All 0x41, m_data8 points to original buffer |
| p159, p161 | Gradient strings | Crash, rope cells mess up heap |
| p160 | Relapse CVE set | **All patched on 14.10** |
| p162 | Deep scan to 2000 bytes | In progress |
| p163 | Device fingerprint | Complete |

## How to Use

1. Clone the repo
2. Run `python3 tools/host.py`
3. Edit `tools/fa-v62-huff.html` to pick a probe
4. Open the URL on the PS5 browser
5. Watch the beacon log

## Models Used

This research was built with multiple LLMs working together.

| Model | Role |
|-------|------|
| Claude Opus 4.6 | Primary workhorse. Probes, source analysis, struct layouts, heap modeling, coordination |
| GPT-6.1-Sol | Codex dispatches, verification passes, structure recommendations |
| GPT-6.1-Astra | Flagship analysis (sometimes unavailable) |
| DeepSeek v4.1-Flash | Scene sweep, PUP carving, gap analysis, gadget hunting |
| DeepSeek v4-Pro | Deep analysis tasks |
| GLM 5.3 Flash | Router analysis, verification, cross audit |
| Kimi K3 | Escape sequence analysis, exploit page construction |
| Qwen 3.8 | Architecture ladder synthesis, verification |
| Mimo | Analysis support |

## Progress

~30% to kernel. 84 probes built across 9 sessions over 3 days.

| Stage | Status |
|-------|--------|
| Bug identification | Done |
| Trigger on device | Done |
| Heap grooming | Done |
| JSString corruption | Done |
| Data extraction (ASLR leak) | WIP |
| Arbitrary read/write | Not started |
| WebKit code execution | Not started |
| Kernel exploit | Not started |
| Privilege escalation | Not started |

## Contact

X: [@Arn0Stride7](https://x.com/Arn0Stride7)

## License

MIT
