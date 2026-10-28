#!/usr/bin/env python3
"""Read-only migration candidates, not a Swift parser or conformance checker."""
import argparse
import json
import os
from pathlib import Path
import re

RULES = [
    ('global-screen', r'UIScreen\s*\.\s*main|UIScreen\s+mainScreen|\[UIScreen\s+mainScreen\]', 'Use container/scene geometry; a two-display device has no unambiguous main screen.'),
    ('orientation', r'UIDevice\s*\.\s*current\s*\.\s*orientation|interfaceOrientation|isLandscape|isPortrait', 'Check whether hardware orientation is being mistaken for available layout space.'),
    ('idiom', r'userInterfaceIdiom|UIDevice\s*\.\s*current\s*\.\s*model', 'Review device-type gating; wide layouts may run on iPhone and compact ones on iPad.'),
    ('safe-area', r'ignoresSafeArea\s*\(|edgesIgnoringSafeArea\s*\(', 'Background escapes can be valid; review interactive foreground and keyboard handling.'),
    ('fixed-frame', r'\.frame\s*\([^\n]*(?:width|height)\s*:\s*\d', 'Review fixed content/pane sizes; icon sizes and minimum touch targets may be intentional.'),
    ('dynamic-identity', r'\.id\s*\([^\n]*(?:UUID\(|orientation|sizeClass|geometry|\.size)', 'Review whether resizing recreates the editor or resets focus/state.'),
    ('gesture-scope', r'\.onTapGesture|\.highPriorityGesture|\.simultaneousGesture|\.contentShape', 'Review nested controls, their containing item, and competing swipe/scroll gestures.'),
]
SKIP = {'.git', '.build', 'build', 'DerivedData', 'Pods', 'Carthage', 'node_modules', '.swiftpm', 'vendor'}

def audit(root):
    findings, scanned, unreadable = [], 0, []
    paths = []
    for directory, folders, files in os.walk(root, followlinks=False):
        folders[:] = sorted(name for name in folders if name not in SKIP and not (Path(directory)/name).is_symlink())
        paths.extend(Path(directory)/name for name in sorted(files))
    for path in paths:
        relative = path.relative_to(root)
        if any(part in SKIP for part in relative.parts) or path.is_symlink():
            continue
        if not path.is_file() or path.suffix not in {'.swift', '.m', '.mm', '.h'}:
            continue
        try:
            lines = path.read_text(encoding='utf-8').splitlines()
        except (OSError, UnicodeError):
            unreadable.append(relative.as_posix())
            continue
        scanned += 1
        for line_number, line in enumerate(lines, 1):
            if line.lstrip().startswith('//'):
                continue
            for name, pattern, reason in RULES:
                if re.search(pattern, line):
                    findings.append(dict(rule=name, file=relative.as_posix(), line=line_number, reason=reason))
    return dict(scannedFiles=scanned, findings=findings, unreadableFiles=unreadable,
                limitation='Heuristic candidates only. Comments, wrappers and multiline code may cause false positives or omissions; no matches does not mean migration passed.')

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project', type=Path)
    parser.add_argument('--format', choices=['markdown', 'json'], default='markdown')
    parser.add_argument('--max-findings', type=int, default=100)
    args = parser.parse_args()
    if not args.project.is_dir() or args.max_findings < 1:
        parser.error('project must be a directory; max-findings must be positive')
    report = audit(args.project.resolve())
    count = len(report['findings'])
    report['totalCandidates'] = count
    report['findings'] = report['findings'][:args.max_findings]
    if args.format == 'json':
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"Scanned {report['scannedFiles']} source files; {count} candidates; showing {len(report['findings'])}.")
        print('\nThese are review candidates, not failures or compliance certification.\n')
        for entry in report['findings']:
            print(f"- `{entry['file']}:{entry['line']}` [{entry['rule']}]: {entry['reason']}")
        if report['unreadableFiles']:
            print('\nUnreadable files: '+', '.join(report['unreadableFiles']))

if __name__ == '__main__':
    main()
