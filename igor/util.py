# Copyright

"Utility functions for handling buffers"

import sys as _sys

import numpy as _numpy


def hex_bytes(buffer, spaces=None):
    r"""Pretty-printing for binary buffers.

    >>> hex_bytes(buffer('\x00\x01\x02\x03\x04'))
    '0001020304'
    >>> hex_bytes(buffer('\x00\x01\x02\x03\x04'), spaces=1)
    '00 01 02 03 04'
    >>> hex_bytes(buffer('\x00\x01\x02\x03\x04'), spaces=2)
    '0001 0203 04'
    >>> hex_bytes(buffer('\x00\x01\x02\x03\x04\x05\x06'), spaces=2)
    '0001 0203 0405 06'
    >>> hex_bytes(buffer('\x00\x01\x02\x03\x04\x05\x06'), spaces=3)
    '000102 030405 06'
    """
    hex_bytes = ['{:02x}'.format(ord(x)) for x in buffer]
    if spaces is None:
        return ''.join(hex_bytes)
    elif spaces is 1:
        return ' '.join(hex_bytes)
    for i in range(len(hex_bytes)//spaces):
        hex_bytes.insert((spaces+1)*(i+1)-1, ' ')
    return ''.join(hex_bytes)

def assert_null(buffer, strict=True):
    r"""Ensure an input buffer is entirely zero.

    >>> import sys
    >>> assert_null(buffer(''))
    >>> assert_null(buffer('\x00\x00'))
    >>> assert_null(buffer('\x00\x01\x02\x03'))
    Traceback (most recent call last):
      ...
    ValueError: 00 01 02 03
    >>> stderr = sys.stderr
    >>> sys.stderr = sys.stdout
    >>> assert_null(buffer('\x00\x01\x02\x03'), strict=False)
    warning: post-data padding not zero: 00 01 02 03
    >>> sys.stderr = stderr
    """
    if buffer and ord(max(buffer)) != 0:
        hex_string = hex_bytes(buffer, spaces=1)
        if strict:
            raise ValueError(hex_string)
        else:
            _sys.stderr.write(
                'warning: post-data padding not zero: {}\n'.format(hex_string))

# From ReadWave.c
def byte_order(needToReorderBytes):
    little_endian = _sys.byteorder == 'little'
    if needToReorderBytes:
        little_endian = not little_endian
    if little_endian:
        return '<'  # little-endian
    return '>'  # big-endian    

# From ReadWave.c
def need_to_reorder_bytes(version):
    # If the low order byte of the version field of the BinHeader
    # structure is zero then the file is from a platform that uses
    # different byte-ordering and therefore all data will need to be
    # reordered.
    return version & 0xFF == 0

# From ReadWave.c
def checksum(buffer, byte_order, oldcksum, numbytes):
    x = _numpy.ndarray(
        (numbytes/2,), # 2 bytes to a short -- ignore trailing odd byte
        dtype=_numpy.dtype(byte_order+'h'),
        buffer=buffer)
    oldcksum += x.sum()
    if oldcksum > 2**31:  # fake the C implementation's int rollover
        oldcksum %= 2**32
        if oldcksum > 2**31:
            oldcksum -= 2**31
    return oldcksum & 0xffff
