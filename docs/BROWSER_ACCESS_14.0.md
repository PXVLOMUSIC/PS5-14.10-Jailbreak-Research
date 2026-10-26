# Browser Accessibility on PS5 Firmware 14.0

**Date:** 2026-10-26  
**Hardware:** PS5 Fat, firmware 14.0  
**Reporter:** PXVLOMUSIC (via PR #46)

---

## Summary

On PS5 firmware 14.0, the built-in WebKit browser appears to be **inaccessible** through normal means. The browser cannot be opened via the standard Media menu, Settings, or any known workaround. DNS spoofing (`manuals.playstation.net` → PC IP) works at the DNS level (queries are received and answered), but the PS5 never attempts to load a web page — it only makes telemetry/API calls.

## Symptoms

1. **DNS queries are received** by the spoofing server (confirmed: `manuals.playstation.net -> 192.168.1.135`).
2. **The PS5 does NOT load any web page** — no HTTP/HTTPS requests are received by the host server.
3. **The browser cannot be opened** via:
   - Media menu (not visible)
   - Settings → Support → User's Guide (does not redirect to browser)
   - Settings → Network → Test Internet Connection (no "Open Browser" option)
   - Notifications with web links
   - Game/app links (no games can be launched — PSN verification blocked by DNS spoofing)
   - Privacy settings (requires PSN login, which requires firmware update to 14.20)
4. **PSN is blocked** by DNS spoofing (all `*.playstation.com` → NXDOMAIN), preventing game launches and PSN login.

## DNS query log (sample)

```
[DNS] manuals.playstation.net -> 192.168.1.135
[DNS] ecode.np.cs.playstation.net -> 192.168.1.135
[DNS] telemetry-console.api.playstation.com -> BLOCKED (NXDOMAIN)
[DNS] smetrics.aem.playstation.com -> BLOCKED (NXDOMAIN)
[DNS] ps5cel.np.dl.playstation.net -> BLOCKED (NXDOMAIN)
```

The PS5 makes DNS queries but **never follows up with HTTP/HTTPS requests**. This suggests the browser is either:
- Disabled in firmware 14.0
- Blocked by a system-level check (possibly tied to PSN verification)
- Requires a firmware update to be accessible

## Impact on research

- **Cannot execute HTML/JS probes** on PS5 14.0.
- **Cannot measure bmalloc classes** (VCAN-MEASURE).
- **Cannot verify API availability** (GIGACAGE-PROBE, BYOB-PROBE, etc.).
- **Cannot verify Gigacage, JSC Config, UMTX** status on 14.0.
- **Cannot populate offsets/14.00.js** with device measurements.
- **Cannot contribute beacon logs** to the repo.

## Comparison with 14.10

The repo's documentation states that the browser is available on 14.10 and all probes were run on 14.10. However, on 14.0, the browser appears to be inaccessible through the same methods (DNS spoofing + User's Guide).

This raises the question: **was the browser accessible on 14.0, or did Sony block it between 14.0 and 14.10?**

## Workarounds attempted (all failed)

1. DNS spoofing (`manuals.playstation.net` → PC IP) — DNS works, but PS5 doesn't load the page.
2. Settings → Support → User's Guide — redirects to `ecode.np.cs.playstation.net`, not to browser.
3. Settings → Network → Test Internet Connection — no "Open Browser" option.
4. Notifications with web links — no web links available.
5. Game/app links — cannot launch games (PSN blocked by DNS spoofing).
6. Privacy settings — requires PSN login (requires firmware update to 14.20).
7. Truco de notificación de actualización — no web link available.
8. Desconectar de internet y reiniciar — browser still not accessible.

## Recommendation for the repo

1. **Document that browser access on 14.0 may be restricted** — add a note to `FIRMWARE_14.0_VS_14.10.md`.
2. **Provide an alternative method** for users who cannot access the browser (e.g., using a different firmware version or a devkit).
3. **Mark 14.0-specific claims as "UNVERIFIED"** until browser access is confirmed.
4. **Consider that 14.0 and 14.10 may have different browser accessibility** — the repo targets 14.10, but 14.0 users cannot contribute measurements.

---

*Reported by PXVLOMUSIC via PR #46. Hardware: PS5 Fat, firmware 14.0.*
PY