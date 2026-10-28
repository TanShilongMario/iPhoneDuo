# Apple sources and boundaries

Last checked: **2026-10-28**. Recheck availability and API signatures against the toolchain you actually use. These are brief pointers, not copies of Apple's documentation.

| Official resource | Use |
| --- | --- |
| [Designing for iPhone Duo](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo) | Hardware regions, adaptable content and continuity across displays |
| [Prepare your app for iPhone Duo](https://developer.apple.com/videos/play/tech-talks/111461/) | SDK, Device Hub, size classes, screen assumptions and asymmetric safe areas |
| [Raise the bar with iPhone Duo](https://developer.apple.com/videos/play/tech-talks/111462/) | System-managed vertical bars, item ordering, axis behavior and overflow |
| [Strike a pose with adaptive layouts on iPhone Duo](https://developer.apple.com/videos/play/tech-talks/111463/) | Reserved-region queries, division/occlusion and arrangement containers |
| [Leverage multiple displays and scenes on iPhone Duo](https://developer.apple.com/videos/play/tech-talks/111464/) | Hinge interaction versus layout, multitasking and scene availability |
| [Layout](https://developer.apple.com/design/human-interface-guidelines/layout) | Safe areas, margins and platform-specific layout guidance |
| [toolbarVerticalEdge](https://developer.apple.com/documentation/swiftui/environmentvalues/toolbarverticaledge) | Preferred context/edge; a non-nil value is not evidence of actual visibility |
| [SwiftUI updates](https://developer.apple.com/documentation/Updates/SwiftUI) | Current bar, arrangement and reserved-region API references |
| [UIView.ReservedRegion](https://developer.apple.com/documentation/uikit/uiview/reservedregion) | UIKit division and occlusion regions |
| [UIKeyboardLayoutGuide](https://developer.apple.com/documentation/uikit/uikeyboardlayoutguide) | Keyboard-occupied layout space and undocked keyboard behavior |
| [Screenshot specifications](https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications/) | Current accepted sizes and no-alpha requirements |
| [Upload previews and screenshots](https://developer.apple.com/help/app-store-connect/manage-app-information/upload-app-previews-and-screenshots/) | Asset workflow, version states and localization/device-size handling |

## Implementation choices are not platform mandates

Pane ordering, equal-width splits, editor location, selection policy, presentation direction and visual styling belong to the app's product design. Examples and diagrams in this repository do not prescribe them.

A side bar is often useful for preserving vertical space; its actual placement follows the system and window context. Keeping an active editor above a keyboard is a visibility requirement, not a universal rule that all input must occupy the upper display region. Matching a capture's backdrop is an optional image-production technique, not a guarantee of store approval.

The included SwiftUI toolbar example was type-checked with the iPhoneSimulator 27.1 SDK and a lower deployment target. This does not establish runtime acceptance for another app or SDK.
