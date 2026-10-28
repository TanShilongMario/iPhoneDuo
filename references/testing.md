# Test matrix

Record the code revision, build configuration, minimum OS, Xcode/SDK and simulator runtime. Use synthetic data or a separate test container. Replace each pending result with pass, fail or not applicable with a reason, and attach evidence.

| ID | Configuration and action | Observable acceptance criterion |
| --- | --- | --- |
| B1 | Ordinary iPhone on original minimum OS; launch, edit and relaunch | Existing navigation and persistence work; no unavailable API is reached |
| B2 | Current ordinary iPhone; supported orientations and long content | No clipping, lost actions, keyboard obstruction or stale empty regions |
| F1 | Duo outer display, portrait | Camera/status regions do not obstruct controls or their hit regions |
| F2 | Outer display, both landscape directions | All actions remain reachable, including overflow; no fixed-edge assumptions |
| L1 | Expanded landscape | Context remains recognizable; panes and content do not distort after transition |
| P1 | Expanded portrait | Information hierarchy is intentional and the primary workflow remains usable |
| H1 | Partial folding in supported orientations, then unfold | Essential controls avoid active fold regions; no duplicate action or state reset |
| K1 | Portrait/partial fold; focus an edge or final field; show software keyboard | Field and insertion point remain visible; keyboard does not trigger a false rotation |
| K2 | Fold/unfold with uncommitted IME marked text | Draft, selection, focus and composition are preserved or gracefully restored |
| K3 | Insert/remove editable content and dismiss keyboard | New content can receive focus; removed content cannot retain stale focus |
| S1 | Empty/existing selection; transition and remove current object | Product selection policy persists; no invalid or stale detail state |
| M1 | Secondary sheet/popover/settings; close, tap outside and rotate | Bounds, dimming, hit testing and dismissal agree with the intended modality |
| T1 | Nested control, surrounding row, scroll and swipe | Intended actions do not steal one another's gestures or execute twice |
| W1 | Inner-display multitasking on either side; resize narrow/wide | Layout follows its actual container and asymmetric bar/safe-area placement |
| C1 | Camera-using app: activate/deactivate inner camera | Foreground adapts to active camera regions; mark not applicable where appropriate |
| A1 | Large text, VoiceOver, reduced motion/transparency | Essential content and actions remain readable, reachable and focusable |
| D1 | Edit, quit, relaunch; concurrent edits if multi-scene is supported | No lost input, stale overwrite, duplicate save or data-format regression |

Prioritize B1, F1, L1, P1, H1, K1, K2, S1 and M1 for an initial pass; this subset is not full platform acceptance.

## Collect evidence

- In the appropriate Xcode environment, use Device Hub's actual open, close, partial-fold and rotate controls. Menu labels and available poses can change across versions.
- If the software keyboard is absent, inspect hardware-keyboard simulation and software-keyboard controls. Computer keyboard input is not a substitute for touch-keyboard testing.
- Use screenshots for settled layout, recordings for transitions/gestures and data assertions for state/persistence. None proves the others.
- Exercise the same object through a round trip. Compare identity, draft text, marked text, selection, focus, insertion point and scroll context before and after.
- Report simulator evidence separately from physical-device acceptance. Installation alone is not acceptance.
- Record failures as precondition → action → actual → expected → build → evidence. Re-run affected cases plus compact baseline after a fix; expand testing when changes justify it.

Copy [the report template](../assets/migration-report.md) for your project. `scripts/audit_layout.py` is a heuristic aid, not a test runner or conformance certificate.
