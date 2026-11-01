#!/usr/bin/env python3
"""Fix NRI's ambiguous Scratch<T> subscripts on 32-bit hosts.

NRI (pinned by the engine) calls `&buffers[0]` and `&textures[0]` on a
Scratch<T>, which has both `operator T*()` and `operator[](size_t)`. With a
plain `int` literal, 32-bit clang finds the member and the built-in
`operator[](T*, int)` equally good and rejects the call. A `size_t` index
selects the member unambiguously and keeps the behavior identical.

Run it after CMake has fetched NRI (build/<dir>/_deps/nri-src) and before the
build. It is idempotent and refuses to guess if the source changed.
"""
import argparse
from pathlib import Path

HEADER = 'Source/Shared/HelperInterface.hpp'
EDITS = (('&buffers[0]', '&buffers[size_t(0)]'), ('&textures[0]', '&textures[size_t(0)]'))


def apply(nri_source):
    path = Path(nri_source) / HEADER
    text = path.read_text()
    for before, after in EDITS:
        if text.count(after) == 1 and text.count(before) == 0:
            continue
        if text.count(before) != 1:
            raise ValueError('NRI source changed; expected one ' + before + ' in ' + str(path))
        text = text.replace(before, after)
    path.write_text(text)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('nri_source', type=Path)
    apply(parser.parse_args().nri_source)
