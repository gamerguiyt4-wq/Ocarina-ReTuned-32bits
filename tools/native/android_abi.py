"""Android ABIs the native host can be packaged for.

arm64-v8a is the supported release ABI. armeabi-v7a is an experimental 32-bit
port; nothing here claims it boots or performs acceptably.
"""

DEFAULT_ABI = 'arm64-v8a'
API_LEVEL = 29

ABIS = {
    'arm64-v8a': {
        'module_target': 'aarch64-linux-android',
        'clang_target': 'aarch64-linux-android29',
        'sysroot_library_directory': 'aarch64-linux-android',
        'readelf_machine': 'AArch64',
        'elf_class': 64,
    },
    'armeabi-v7a': {
        'module_target': 'armv7a-linux-androideabi',
        'clang_target': 'armv7a-linux-androideabi29',
        'sysroot_library_directory': 'arm-linux-androideabi',
        'readelf_machine': 'ARM',
        'elf_class': 32,
    },
}


def abi_settings(abi):
    try:
        return ABIS[abi]
    except KeyError:
        raise ValueError('Unsupported Android ABI: ' + str(abi)) from None
