# Migration guide

## Establish a baseline

Identify the root navigation/container, editors, presentation entrypoints and state owners. Record the current compact experience and original deployment target. Separate platform availability from layout capability: a useful wide layout must not be restricted to iPad merely because of its device idiom, and ordinary iPad behavior must not depend on a Duo-only API.

Use local view or scene geometry rather than an assumed main screen. Consult size classes, available bounds and active reserved regions together. Device orientation alone does not describe a multitasking window. Keep older-OS fallbacks and type-check new APIs against the installed SDK.

## Cameras, folds and bars

Prefer standard navigation containers and their managed bars. Putting a standalone custom bar near a camera does not grant it the adaptation behavior of a navigation container.

- Keep interactive foreground and its full hit area clear of system UI. A button can look visible while part of its touch region is obstructed.
- Handle safe-area edges independently; opposite insets need not be equal. Only backgrounds should extend freely behind hardware/system regions by default.
- Where vertical bars are appropriate, let the system choose their edge. `toolbarVerticalEdge` reports a preferred context, not actual visibility. Avoid accidentally hiding the only available action entrypoint.
- Provide localized titles and accessibility names even when icons are the visible representation. Prioritize frequent actions and use system overflow when space is constrained.
- For custom layouts, distinguish occlusion regions from division regions and compare their frames in a consistent coordinate space.

See [Raise the bar](https://developer.apple.com/videos/play/tech-talks/111462/) and [toolbarVerticalEdge](https://developer.apple.com/documentation/swiftui/environmentvalues/toolbarverticaledge).

## Choose containers before pose-specific branches

Use `NavigationSplitView` / `UISplitViewController` for navigation hierarchy. Evaluate `ArrangementView` / `UIArrangementViewController` for two related regions without imposing an unrelated navigation model. Use reserved-region queries when a custom container genuinely needs them.

Keep familiar content and actions recognizable as space changes. Additional space can expose context without requiring a wholesale redesign. There is no universal rule for which pane belongs on the left, whether columns are equal, or where all controls must move.

When partially folded, keep essential controls within usable regions. Continuous scrolling content may remain continuous; do not reposition every list merely because a fold exists. Prefer minimal displacement of related content. Hinge-angle data is useful for special interactions; arrangement and region APIs are usually a better basis for ordinary layout.

Check both transition frames and the settled state. Common failures include oversized content after the final frame, duplicated insets, stale spacer reservations and layouts constrained to full-display bounds instead of their pane. For a deliberately equal split, calculate in one workspace coordinate system, then inset each pane; active fold regions take precedence over a purely geometric midpoint.

See [adaptive layouts](https://developer.apple.com/videos/play/tech-talks/111463/) and [hinge versus layout APIs](https://developer.apple.com/videos/play/tech-talks/111464/).

## Keyboard and state continuity

Keep the active field, insertion point and necessary context visible with the software keyboard. Depending on the workflow, an editor in an upper region and secondary controls elsewhere may help. That is a design option, not a ban on lower-region input.

- Do not switch layout modes solely because the keyboard reduced the reported height. Distinguish keyboard-driven viewport changes from genuine scene/window resizing; do not permanently cache the first orientation either.
- Keep model, selection, draft and commands under stable ownership. A layout branch may change presentation without creating independent edit snapshots.
- Avoid changing an editor's identity with orientation, transient geometry or a fresh UUID. Check focus, marked text and scroll position through transitions.
- For newly inserted editable rows, create a stable identity, then focus and reveal the inserted field after layout. Validate removal of the active field too.
- Respect the product's existing selection policy. If nothing is selected, show an intentional state rather than silently opening an arbitrary object; clear or update invalid selections after removal.
- Do not enable multiple scenes just to create multiple panes. Existing multi-scene apps need coordinated persistence and dynamic scene-availability handling.

UIKit can track keyboard space with [UIKeyboardLayoutGuide](https://developer.apple.com/documentation/uikit/uikeyboardlayoutguide). In SwiftUI, scope keyboard-safe-area overrides narrowly and verify actual visibility. A blanket `.ignoresSafeArea(.keyboard)` is not a general repair.

## Presentations and nested gestures

Start with system sheet/popover behavior. Custom local presentations must keep visual bounds, dismissal behavior, dimming and hit testing consistent with their modality. Do not imply that a whole window is disabled while only intercepting one pane, or block an unrelated pane without a reason.

Distinguish selecting an object from opening its secondary settings. With nested controls, verify their intended hit regions independently of the containing row, scrolling and swipe actions. Do not fix a missing transparency requirement by changing the entire color palette.

Preview is a diagnostic aid. Reproduce issues in the actual simulator with the same build and compare container, navigation and safe-area environments before changing production layout. Report rendering/caching limitations separately from runtime bugs.
