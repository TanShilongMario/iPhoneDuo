# iPhone Duo Migration Skill

**English** · [简体中文](README.zh-CN.md)

An agent skill and practical toolkit for migrating SwiftUI and UIKit apps to iPhone Duo while preserving the ordinary iPhone experience.

![Adaptive layout principles across compact, expanded and keyboard-present contexts](docs/images/adaptive-layouts.svg)

*Conceptual diagrams, not device specifications or screenshots of an app. Pane arrangement is illustrative; choose it for your product.*

## What it covers

- Camera, safe-area and fold-region avoidance, including actual button hit areas.
- System-managed side toolbars, overflow and asymmetric insets.
- Continuity of navigation, selection, drafts, focus and marked text across poses.
- Editing with the software keyboard, partial folding and multitasking.
- Regression testing on ordinary iPhones and the original minimum OS.
- Optional authentic simulator captures with reproducible, opaque-background composition.

The guidance is product-independent. It does not require a card interface, a fixed pane order, equal-width columns, a particular color palette or an upper-screen-only editor. Public Apple behavior is distinguished from implementation choices.

## Quick start

### Use it with an agent

The repository root is a complete skill directory. For Codex, clone it into your skills directory:

```sh
git clone https://github.com/TanShilongMario/iPhoneDuo.git \
  "${CODEX_HOME:-$HOME/.codex}/skills/iphone-duo-migration"
```

Then invoke:

```text
Use $iphone-duo-migration to audit this iOS app, migrate its adaptive layout,
and test Duo poses plus ordinary iPhone behavior. Preserve the deployment
target and data model unless a change is necessary and explained.
```

For other agents, provide [SKILL.md](SKILL.md) as the entrypoint. The guides and tools are also usable without an agent.

### Run the read-only audit

```sh
python3 scripts/audit_layout.py /path/to/your/app --format markdown
```

The audit flags candidates such as global-screen assumptions, orientation-driven layout, device-type gating, fixed content frames and editor identity changes. It neither edits code nor certifies compatibility. False positives and omissions are possible.

### Test and record evidence

Follow the [migration guide](references/migration.md), execute the [test matrix](references/testing.md), and copy the [report template](assets/migration-report.md). Run the app with an actual software keyboard, not only a hardware keyboard or Preview.

![Keep the active editor visible while preserving focus and input across a size change](docs/images/keyboard-continuity.svg)

*The invariant is visible input and preserved state. The diagram is one possible arrangement, not a required layout.*

## Included files

| Resource | Purpose |
| --- | --- |
| [SKILL.md](SKILL.md) | Agent entrypoint and workflow |
| [Migration guide](references/migration.md) | Containers, reserved regions, bars, input and state |
| [Test matrix](references/testing.md) | Observable acceptance criteria, including compact regression |
| [Apple sources](references/apple-sources.md) | Official documentation and Tech Talks |
| [Screenshot workflow](references/screenshots.md) | Authentic captures and matching-background composition |
| [SwiftUI example](assets/AdaptiveActions.swift) | Standard adaptive actions and overflow |
| [Report template](assets/migration-report.md) | Results, evidence and remaining limitations |

## Requirements and checks

The documentation supports both SwiftUI and UIKit. The SwiftUI example uses iOS 27.1 APIs behind availability gating; check your installed SDK and preserve the app's own minimum OS. Official links were last checked on **2026-10-28** and should be rechecked for your toolchain.

Python 3.9+ runs the audit. Only screenshot composition and its tests need Pillow:

```sh
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements-dev.txt
python3 -m unittest discover -s tests -v
```

The screenshot helper creates opaque RGB PNGs and JSON provenance. It does not capture a screen, synthesize UI, or guarantee App Store acceptance. See [its workflow and parameters](references/screenshots.md).

## Contributing

Useful contributions include reproducible layout failures, SDK/API corrections, tests and translations. Include the Xcode/SDK/runtime, the smallest reproducer, expected behavior and actual behavior. Use synthetic data and remove app identifiers, credentials and private content from reports. Product-specific designs should remain examples, not become universal rules.

## License

[MIT](LICENSE). Community-maintained; not affiliated with or endorsed by Apple. Linked Apple materials remain subject to their original terms.
