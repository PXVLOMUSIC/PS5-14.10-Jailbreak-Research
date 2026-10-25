#!/usr/bin/env python3
"""Generate beacon log templates for probes that lack evidence.

This tool does NOT fabricate data. It creates empty templates with the expected
fields so contributors can fill them with real device data.
"""
import os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = os.path.join(REPO, "results", "beacon-logs")

# Known probe prefixes and their expected fields (from PROBE_INDEX.md)
PROBE_TEMPLATES = {
    "VCAN-MEASURE": ["spray_count", "lineWidth_readback", "alias_idx", "crash"],
    "GIGACAGE-PROBE": ["sharedarraybuffer", "atomics_wait", "webassembly", "status"],
    "BYOB-PROBE": ["byob_reader", "byte_stream", "transformstream", "status"],
    "UMTX-PROBE": ["sharedarraybuffer", "atomics_wait", "webassembly", "status"],
    "JSCCONFIG-PROBE": ["uaf_trigger", "stale_read", "stale_write", "status"],
    "APNG-LEAK-PROBE": ["pixel_data", "leak_count", "non_zero_gb", "status"],
    "OFFSCREENCANVAS-PROBE": ["offscreen_canvas", "context_2d", "status"],
    "WEBGL-PROBE": ["webgl_context", "webgl2_context", "status"],
    "V527": ["lineWidth", "reclaim", "status"],
    "V573": ["alias", "idx", "bidirectional", "rw"],
    "V630": ["api", "result", "status"],
    "V674": ["ptr_count", "heap_ptrs", "aslr"],
    "V589": ["trigger", "status", "crash"],
    "V627": ["phase", "status", "crash"],
    "p161a": ["fontface", "numglyphs", "unitsperem", "canvas_pixels"],
    "p161b": ["formats", "truncated_png", "createimagebitmap", "status"],
    "p180a": ["variants", "loca_oob", "dir_past_eof", "status"],
    "p221": ["proxy_trap", "butterfly_freed", "status"],
    "p243": ["holes", "spray_reclaim", "status"],
    "p246": ["jsarray_spray", "reclaim", "status"],
    "p170": ["woff2_rejected", "cssfontface_uaf", "status"],
    "p175": ["ttf_load", "uaf_trigger", "status"],
}

def generate_template(probe_id, fields):
    lines = []
    lines.append(f"# Beacon log template for {probe_id}")
    lines.append(f"# Fill in real device data. Do NOT fabricate.")
    lines.append(f"# Firmware: 14.10 (or your version)")
    lines.append(f"# Date: YYYY-MM-DD")
    lines.append(f"# Probe: {probe_id}")
    lines.append("")
    for field in fields:
        lines.append(f"{probe_id}-{field.upper()}: <value>")
    lines.append("")
    lines.append(f"# Notes: <any additional observations>")
    lines.append(f"# Console output: <paste relevant console.log>")
    return "\n".join(lines)

def main():
    os.makedirs(RESULTS, exist_ok=True)
    generated = 0
    skipped = 0
    for probe_id, fields in PROBE_TEMPLATES.items():
        filename = f"{probe_id}-TEMPLATE.txt"
        path = os.path.join(RESULTS, filename)
        if os.path.exists(path):
            skipped += 1
            continue
        content = generate_template(probe_id, fields)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        generated += 1
        print(f"  CREATED: {filename}")

    print(f"\nGenerated {generated} template files ({skipped} skipped).")
    print(f"Location: {RESULTS}")
    print("Fill in real device data before committing.")

if __name__ == "__main__":
    main()
PY