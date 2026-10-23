<p align="center">
  <img src="./installer/assets/icon.svg" width="128" />
</p>
<h1 align="center">PS5 WebKit Remote Loader</h1>
<p align="center">JavaScript payload loader for the PS5.<br>Supports firmwares <b>7.00&ndash;13.60</b>.</p>

Inspired by [remote_lua_loader](https://github.com/n0llptr/remote_lua_loader) and [Y2JB](https://github.com/Gezine/Y2JB), the loader runs in WebKit userland and accepts payloads over TCP on port **9027**. Kernel exploits are optional payloads, not a prerequisite for the loader.

## Setup

Run the PC host from a checkout or use the bundled Python script / Windows
executable from a release:

```sh
sudo python3 host.py
```

The default DNS and HTTPS ports are 53 and 443 (elevated privileges may be needed).
Set the PS5's primary DNS to the PC's LAN IP, then open **Settings → User's Guide**.
Restore automatic DNS when finished.

For a homescreen installation, send `webkit-remote-loader-installer_v*.elf` through
an existing ELF loader. It serves an AppCache installer on port 18180 and installs
the homescreen shortcut (`WKRL00001`). See [installer/README.md](installer/README.md).

## Sending payloads

```sh
python3 tools/send.py <PS5_IP> 9027 payloads/hello_world.js
python3 tools/send.py <PS5_IP> 9027 payloads/notify.js --arg "Hello PS5"
python3 tools/send.py <PS5_IP> 9027 --status
```

See [payloads/README.md](payloads/README.md) for bundled payloads and arguments.

## Payload API

Payloads return an async entry function:

```js
return async function (api) {
  const pid = await api.chain.syscall(0x014);
  await api.log(`pid=${pid.low}`);
};
```

For the complete API reference, memory primitives, ROP batching, and execution rules, see [docs/API.md](docs/API.md).

## Single-file builds

Generate self-contained HTML pages bundling the loader, exploits, and payloads:

```sh
python3 tools/build_standalone.py payloads/hello_world.js -o dist/ps5.html --probe
python3 tools/build_standalone.py payloads/relapse.js \
  'payloads/ftp_server.js::port=1337,path=/data' -o dist/ps5.html
sudo python3 tools/host_standalone.py dist/ps5.html
```

* Payloads run sequentially with shared session state. Use `--no-kexp` to omit kernel binaries.
* Call `api.stopQueue(reason)` from any payload to skip the remaining queue cleanly.
* Standalone pages omit the remote connection HUD and run without opening port 9027.

### Embedded assets and PC host

* `--embed URL=FILE`: Embeds arbitrary files accessible via relative `fetch()` offline.
* `--elfldr [URL=]FILE`: Overrides the default bundled ELF loader (optionally at a custom virtual URL).

```sh
python3 tools/build_standalone.py payloads/hello_world.js \
  --embed payload.bin=/path/to/payload.bin --elfldr /path/to/elfldr.elf \
  -o dist/custom.html --probe

# Package into a standalone Python DNS/HTTPS setup host
python3 tools/build_host.py --page dist/custom.html --name "PS5 CUSTOM HOST"
```

The host builder supports multiple pages (`--page index.html=relapse.html --page poops.html=poops.html`). Multi-page hosts automatically route firmwares incompatible with Relapse (9.05, 11.40) or `?exploit=poops` to `poops.html`.

### Custom appearance and startup scripts

* `--css FILE`: Injects custom stylesheets after the default styles.
* `--js FILE`: Injects startup scripts executed (and awaited) before exploit boot.

```sh
python3 tools/build_standalone.py payloads/hello_world.js \
  --css /path/to/theme.css --js /path/to/setup.js -o dist/custom.html --probe
```

## Build and test

Build the bundled host and native installer:

```sh
make host            # Build standalone host script
./build_release.sh   # Build versioned installer ELF and host (Docker required)
```

Run test suites (Node.js and Python 3):

```sh
make test            # Runs selftest, standalone runner, asset & customization tests
make test-native     # Runs shared native installer tests with stubbed PS5 services
```

---

## 14.10 Research

Security research targeting the PS5 WebKit browser on firmware **14.10**. This firmware runs a no-JIT WebKit on FreeBSD 11 (AMD Zen2) with several noteworthy allocator characteristics that differ from upstream WebKit.

### Environment

| Property | Value |
|----------|-------|
| Firmware | 14.10 |
| WebKit JIT | Disabled (interpreter only) |
| Gigacage | **Disabled** — typed array backing stores share the primary FastMalloc heap |
| IsoHeap | **Disabled** — `WTF_MAKE_ISO_ALLOCATED` compiles to standard `FastMalloc` |
| ASLR | Enabled (24-bit user / 16-bit kernel entropy) |
| libpas | Present (`BPLATFORM(PLAYSTATION)` in `BPlatform.h`) — sparse page commit model |
| WebGL | Unavailable |
| OffscreenCanvas | Unavailable |
| Workers | Available |
| ResizableArrayBuffer | Available (WebCore APIs reject resizable views) |

### CVE-2026-43720 — Canvas Context Lifecycle

Analysis of [CVE-2026-43720](https://www.cve.org/CVERecord?id=CVE-2026-43720), a canvas rendering context lifecycle issue in `HTMLCanvasElement::getContext()`. The reentrant path through `bitmaprenderer` → property getter → `2d` creates a window where the inner context reference outlives its expected scope. Research probes confirm:

- The freed 768-byte `CanvasRenderingContext2D` slot can be reclaimed by a same-size `ArrayBuffer` spray
- The aliased context supports bidirectional read/write through standard Canvas2D APIs (`lineWidth`, `miterLimit`, `setLineDash`, `getLineDash`, `globalAlpha`, etc.)
- Full 12-API capability pass confirmed on device (V562)
- `sizeof(State) = 400`, with key fields mapped: `m_stateStack` at +112, `lineWidth` at +48, `miterLimit` at +64, `lineDash` Vector at +168

### Heap Memory Mapping

A binary subdivision scanner (V655) maps the WebContent process address space by probing whether target pages are resident. The algorithm tests the start, end, and midpoint of a range first, then fills in quarter-points, eighth-points, and so on — achieving ~187KB resolution across a 24MB search space in ~129 probes.

Key memory layout findings (informed by VM map data — see acknowledgments):

- **SceLibcHeap** spans at least two VA ranges in the process map
- The heap uses a sparse commit model: large PROT_NONE reservations with individual pages committed via MAP_FIXED on demand
- Freed blocks remain mapped (no `MADV_FREE` / page decommit), and release assertions are disabled
- ArrayBuffer backing stores, JSC objects, and WebCore DOM objects all share the same FastMalloc heap due to Gigacage and IsoHeap being off

### Probe History

Iterative research probes (V569–V655) cover:

- **V569–V573**: Context reclaim methodology — confirming same-type heap reclaim on device
- **V574–V589**: API surface exploration, capability mapping, and JSC feature testing
- **V590–V601**: State struct layout analysis, Vector growth behavior, gradient/pattern operations
- **V610–V643**: Address scanning strategies (linear, stride, targeted)
- **V650–V655**: Crash oracle and binary subdivision scanner for heap topology mapping

### Acknowledgments

VM map data from [ZigZagBoi1's PS5 14.10 research](https://github.com/ZigZagBoi1/PS5-14.10-Research) provided critical memory layout intelligence that guided the heap scanning strategy. Their 317-region process map (obtained via syscall 674) revealed SceLibcHeap boundaries, GPU mapping locations, and the sparse commit structure of the allocator — a small lamp in the darkness of working without direct memory introspection.

---

## Credits and licenses

* **[Y2JB](https://github.com/Gezine/Y2JB)** and **[remote_lua_loader](https://github.com/n0llptr/remote_lua_loader)** — used for reference.
* Relapse is adapted from [ntfargo](https://github.com/ntfargo) and [Sonic_Iso](https://github.com/soniciso1)'s [Relapse-Exploit](https://github.com/ntfargo/Relapse-Exploit).
* Poops is adapted from [Jordy](https://github.com/jordyidk)'s [slopkit](https://github.com/jordyidk/slopkit).
* **[john-tornblom](https://github.com/john-tornblom)** — [ps5-payload-sdk](https://github.com/ps5-payload-dev/sdk/) and [elfldr](https://github.com/ps5-payload-dev/elfldr)
* **[ufm42](https://github.com/ufm42)** — [kexp](https://github.com/ufm42/kexp)
* **[madler](https://github.com/madler)** — [puff](https://github.com/madler/zlib/tree/master/contrib/puff)

The loader, PC host, and client tools are licensed under [MIT](LICENSE).
The installer and its shared native helpers ([installer/common](installer/common/README.md)) are licensed under [GPLv3](installer/LICENSE).

## Disclaimer

This tool is provided as-is for research and development purposes only. Use at your own risk. The developers are not responsible for any damage, data loss, or consequences resulting from the use of this software.

## Donate
- [donate to PLK](DONATE.md)
