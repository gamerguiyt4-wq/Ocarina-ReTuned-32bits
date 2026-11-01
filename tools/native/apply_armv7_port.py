#!/usr/bin/env python3
"""Let the pinned engine's Android build accept armeabi-v7a (experimental).

Only the ABI gates are relaxed. This does not make the engine correct on 32-bit
hosts: compile and run it to find out. Source changes that a real 32-bit build
needs belong in their own focused patches, not here.
"""
import argparse
from pathlib import Path
import subprocess

REVISION = '17218b0cfdb944645bb5cde5249f313dca7e53ce'
GATE = 'NOT CMAKE_ANDROID_ARCH_ABI STREQUAL "arm64-v8a"'
RELAXED = 'NOT CMAKE_ANDROID_ARCH_ABI MATCHES "^(arm64-v8a|armeabi-v7a)$"'
CMAKE_FILES = ('runtime', 'renderer', 'native')


def apply(engine):
    root = Path(engine)
    head = subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD'], text=True).strip()
    if head != REVISION:
        raise ValueError('Unexpected native runtime revision.')
    for name in CMAKE_FILES:
        path = root / 'ports/android' / name / 'CMakeLists.txt'
        text = path.read_text()
        if RELAXED in text:
            continue
        if text.count(GATE) != 1:
            raise ValueError('Android ABI gate changed: ' + str(path))
        path.write_text(text.replace(GATE, RELAXED))
    # The app is packaged for one ABI at a time, so the filter and the staged
    # library directory both follow it.
    gradle = root / 'ports/android/app/build.gradle.kts'
    text = gradle.read_text()
    if 'abiFilters += "arm64-v8a"' not in text and 'abiFilters += "armeabi-v7a"' not in text:
        raise ValueError('Android ABI filter changed: ' + str(gradle))
    gradle.write_text(text.replace('arm64-v8a', 'armeabi-v7a'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('engine', type=Path)
    apply(parser.parse_args().engine)
