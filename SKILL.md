---
name: iphone-duo-migration
description: "Migrate and test SwiftUI/UIKit apps for iPhone Duo: camera and fold avoidance, adaptive toolbars, keyboard-safe editing, state continuity, and ordinary iPhone regression. Includes optional guidance for authentic simulator screenshots."
---

# iPhone Duo Migration

Improve an existing app across compact, expanded, partially folded, and multitasking environments without prescribing its information architecture or visual style.

## Read only what the task needs

- Implementation: [migration guide](references/migration.md) and [Apple sources](references/apple-sources.md).
- Verification: [test matrix](references/testing.md); copy the [report template](assets/migration-report.md).
- Marketing or demo captures: [screenshot workflow](references/screenshots.md).

## Workflow

1. Establish an ordinary iPhone baseline. Record the minimum OS, Xcode/SDK, navigation, editing and persistence behavior. Updating the build SDK does not require raising the deployment target. Preserve identifiers and data formats unless the task explicitly changes them.
2. Audit root containers, bars, editors, presentations, gestures and state ownership. Optionally run `python3 <skill>/scripts/audit_layout.py <project>`. Findings are review candidates, not automatic failures.
3. Prefer standard navigation and adaptive layout containers. Gate new APIs by availability and keep existing compact/older-OS paths. Consult current public SDK declarations before using a new symbol.
4. Preserve the user's context while the available space changes: selected item, navigation, draft, focus, marked text and scroll position. Add contextual information when space permits; do not merely stretch every component.
5. Exercise real folding, rotation, keyboard and presentation transitions. Include an ordinary iPhone regression. Screenshots prove a visual state, not interaction correctness.
6. Report changes, tests actually performed, evidence and untested limitations separately. A successful build, simulator run, device installation and physical-device acceptance are different results.

## Essential decisions

- Keep foreground controls and their hit regions clear of cameras, system UI and active fold regions. Distinguish safe-area insets from reserved regions.
- Prefer system-managed vertical bars where available. Follow `toolbarVerticalEdge`, not a hard-coded right edge. The value expresses a preferred context, not proof that a bar is visible.
- Keep related content and actions recognizable across poses. The skill does not mandate a left/right pane order, equal pane widths, a particular selection policy or a custom sheet direction.
- Keep active input and the insertion point visible with the software keyboard. An upper-region editor can help in some vertically folded workflows; evaluate the app's task instead of banning lower-region interaction.
- Do not interpret keyboard-reduced height as a device rotation. Use size classes, container geometry and active regions; still respond to genuine window resizing.
- Share business state and commands across layouts. Avoid orientation-dependent identities that recreate editors or independent snapshots that overwrite one another.

## Resources

- [AdaptiveActions.swift](assets/AdaptiveActions.swift): a small availability-gated system-toolbar example, not a replacement navigation architecture.
- `scripts/audit_layout.py`: read-only Swift/Objective-C heuristic scan; standard-library Python only.
- `scripts/compose_capture.py`: optional Pillow helper that composes an original opaque window crop on a sampled matching background, without an alpha mask or UI regeneration.

This skill does not itself authorize publishing assets, changing account settings, or submitting an app for review.
