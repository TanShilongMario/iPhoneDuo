# Migration report

- App/revision:
- Xcode/SDK/runtime/build configuration:
- Original minimum OS and compact baseline:
- Root navigation/layout containers:
- State/persistence ownership:
- Official documentation checked on:

## Decisions

| Area | Current risk | Change | Compact/older-OS fallback |
| --- | --- | --- | --- |
| Camera, safe areas and reserved regions | Pending | Pending | Pending |
| Bars and overflow | Pending | Pending | Pending |
| Expanded/partially folded layout | Pending | Pending | Pending |
| Keyboard, focus and draft continuity | Pending | Pending | Pending |
| Presentations and nested gestures | Pending | Pending | Pending |

## Actual results

Copy applicable IDs from the test matrix. Use pass/fail/not applicable with a reason; do not mark a test passed without execution.

| ID | Device/pose/window | Preconditions and action | Result | Build/evidence |
| --- | --- | --- | --- | --- |
| B1 | Ordinary iPhone/original minimum OS | Launch, edit and relaunch | Pending | Pending |
| F1 | Outer display | Exercise camera-adjacent controls | Pending | Pending |
| L1/P1 | Expanded landscape/portrait | Continue the primary workflow | Pending | Pending |
| H1 | Partially folded | Fold/unfold round trip | Pending | Pending |
| K1/K2 | Software keyboard and IME | Resize with uncommitted marked text | Pending | Pending |
| S1 | Empty/existing selection | Transition and remove current object | Pending | Pending |
| M1 | Secondary presentation | Dismiss, tap outside and resize | Pending | Pending |
| W1 | Multitasking on either side | Resize narrow/wide | Pending | Pending |

## Boundaries

- Fixes and retest evidence:
- Remaining observed failures:
- Untested/environment-limited cases:
- Simulator-only results awaiting physical-device acceptance:
- Optional imagery: build, locale, pose, source hash, processing/export/upload state:
