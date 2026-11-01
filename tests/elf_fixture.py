import struct


def elf(exports=(), imports=(), weak=(), wide=True):
    """Build a minimal shared object; wide=False yields a 32-bit (ELF32) file."""
    entry = 24 if wide else 16
    names = bytearray(b'\0')
    symbols = bytearray(entry)
    for values, binding, section in ((exports, 1, 1), (imports, 1, 0), (weak, 2, 0)):
        for name in values:
            info = binding << 4 | 2
            if wide:
                symbols.extend(struct.pack('<IBBHQQ', len(names), info, 0, section, 0, 0))
            else:
                symbols.extend(struct.pack('<IIIBBH', len(names), 0, 0, info, 0, section))
            names.extend(name.encode() + b'\0')
    if wide:
        header = bytearray(64)
        header[:6] = b'\x7fELF\x02\x01'
        struct.pack_into('<Q', header, 40, 64)
        struct.pack_into('<HH', header, 58, 64, 3)
        section_format, section_size = '<IIQQQQIIQQ', 64
    else:
        header = bytearray(52)
        header[:6] = b'\x7fELF\x01\x01'
        struct.pack_into('<I', header, 32, 52)
        struct.pack_into('<HH', header, 46, 40, 3)
        section_format, section_size = '<IIIIIIIIII', 40
    base = len(header) + section_size * 3
    sections = bytes(section_size)
    sections += struct.pack(section_format, 0, 11, 0, 0, base, len(symbols), 2, 0, 4, entry)
    sections += struct.pack(section_format, 0, 3, 0, 0, base + len(symbols), len(names), 0, 0, 1, 0)
    return bytes(header) + sections + bytes(symbols) + bytes(names)
