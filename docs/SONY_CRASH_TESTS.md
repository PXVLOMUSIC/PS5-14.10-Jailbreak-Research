# Sony PS5 Crash Tests — Analysis

**Source:** `LayoutTests/platform/playstation-ps5/TestExpectations` (from WebKit_1400.zip)  
**Total `[ Crash ]` entries:** 54  
**Analysis date:** 2026-10-25

---

## Summary

| Category | Count | Harness-dependent? | Triggerable from browser? |
|---|---|---|---|
| fast/ (forms, dom, events, etc.) | 45 | Mostly yes | ❌ No (requires testRunner) |
| editing/ (secure-input, selection, etc.) | 6 | Yes | ❌ No |
| compositing/ (backing, iframes, tiling) | 3 | Yes | ❌ No |

**Verdict (mja00, issue #11):** All 54 are harness-only. None are triggerable from the browser. They are platform-layer crashes (validation bubbles, visual viewport, datalist/date pickers, secure input), not WebProcess memory bugs.

---

## Full list of crash tests

### compositing/ (3)
- `compositing/backing/backing-store-attachment-scroll.html`
- `compositing/iframes/remove-reinsert-webview-with-iframe.html`
- `compositing/tiling/tile-coverage-on-scroll.html`

### editing/ (6)
- `editing/execCommand/typing-should-not-trigger-scrolling-when-selection-is-visible.html`
- `editing/input/delete-text-in-composition.html`
- `editing/secure-input/password-input-changed-type.html`
- `editing/secure-input/password-input-focusing.html`
- `editing/secure-input/removed-password-input.html`
- `editing/secure-input/reset-state-on-navigation.html`

### fast/ (45)
- `fast/dom/Window/post-message-large-array-buffer-should-not-crash.html`
- `fast/events/autoscroll-when-input-is-offscreen.html`
- `fast/events/autoscroll-with-software-keyboard.html`
- `fast/events/before-input-prevent-insert-replacement.html`
- `fast/events/input-event-insert-replacement.html`
- `fast/forms/datalist/datalist-option-labels.html`
- `fast/forms/scroll-into-view-and-show-validation-message.html`
- `fast/forms/validation-bubble-disappears-when-input-detached.html`
- `fast/forms/validation-bubble-disappears-when-input-moved.html`
- `fast/forms/validation-bubble-disappears-when-input-no-longer-visible.html`
- `fast/forms/validation-bubble-escape-key-dismiss.html`
- `fast/forms/validation-custom-message.html`
- `fast/forms/validation-message-detached-iframe.html`
- `fast/forms/validation-message-detached-iframe2.html`
- `fast/forms/validation-messages.html`
- `fast/visual-viewport/` (15 tests — visual viewport crashes)

*(Full list: extract from TestExpectations file)*

---

## Why they're not exploitable

1. **Harness dependency:** All require `testRunner` or `UIHelper` APIs not available in the browser.
2. **Platform-layer, not WebProcess:** Crashes are in Sony's WTR/UI-process port (validation bubbles, visual viewport, datalist/date pickers), not in WebCore memory.
3. **0/54 overlap with corpus:** None appear in the 644-case corpus or in Sony's change list as picked fixes.
4. **ASan verification:** mja00 ran 11 plain-JS tests under ASan — all clean, no memory corruption.

---

## Recommendation

**Do not invest time in these crash tests.** They are not exploitable from the browser. Focus on CVE-2026-43720 and the info leak problem.

---

*Analysis based on mja00's findings (issue #11) and source inspection of WebKit_1400.zip.*
PY