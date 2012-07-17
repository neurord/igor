# Copyright (C) 2010 W. Trevor King <wking@drexel.edu>
#
# This file is part of Hooke.
#
# Hooke is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Hooke is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General
# Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with Hooke.  If not, see
# <http://www.gnu.org/licenses/>.

"Read IGOR Binary Wave files into Numpy arrays."

# Based on WaveMetric's Technical Note 003, "Igor Binary Format"
#   ftp://ftp.wavemetrics.net/IgorPro/Technical_Notes/TN003.zip
# From ftp://ftp.wavemetrics.net/IgorPro/Technical_Notes/TN000.txt
#   We place no restrictions on copying Technical Notes, with the
#   exception that you cannot resell them. So read, enjoy, and
#   share. We hope IGOR Technical Notes will provide you with lots of
#   valuable information while you are developing IGOR applications.

import array as _array
import sys as _sys
import types as _types

import numpy as _numpy

from .struct import Structure as _Structure
from .struct import Field as _Field
from .util import assert_null as _assert_null
from .util import byte_order as _byte_order
from .util import need_to_reorder_bytes as _need_to_reorder_bytes
from .util import checksum as _checksum


# Numpy doesn't support complex integers by default, see
#   http://mail.python.org/pipermail/python-dev/2002-April/022408.html
#   http://mail.scipy.org/pipermail/numpy-discussion/2007-October/029447.html
# So we roll our own types.  See
#   http://docs.scipy.org/doc/numpy/user/basics.rec.html
#   http://docs.scipy.org/doc/numpy/reference/generated/numpy.dtype.html
complexInt8 = _numpy.dtype([('real', _numpy.int8), ('imag', _numpy.int8)])
complexInt16 = _numpy.dtype([('real', _numpy.int16), ('imag', _numpy.int16)])
complexInt32 = _numpy.dtype([('real', _numpy.int32), ('imag', _numpy.int32)])
complexUInt8 = _numpy.dtype([('real', _numpy.uint8), ('imag', _numpy.uint8)])
complexUInt16 = _numpy.dtype(
    [('real', _numpy.uint16), ('imag', _numpy.uint16)])
complexUInt32 = _numpy.dtype(
    [('real', _numpy.uint32), ('imag', _numpy.uint32)])

# Begin IGOR constants and typedefs from IgorBin.h

# From IgorMath.h
TYPE_TABLE = {        # (key: integer flag, value: numpy dtype)
    0:None,           # Text wave, not handled in ReadWave.c
    1:_numpy.complex, # NT_CMPLX, makes number complex.
    2:_numpy.float32, # NT_FP32, 32 bit fp numbers.
    3:_numpy.complex64,
    4:_numpy.float64, # NT_FP64, 64 bit fp numbers.
    5:_numpy.complex128,
    8:_numpy.int8,    # NT_I8, 8 bit signed integer. Requires Igor Pro
                      # 2.0 or later.
    9:complexInt8,
    0x10:_numpy.int16,# NT_I16, 16 bit integer numbers. Requires Igor
                      # Pro 2.0 or later.
    0x11:complexInt16,
    0x20:_numpy.int32,# NT_I32, 32 bit integer numbers. Requires Igor
                      # Pro 2.0 or later.
    0x21:complexInt32,
#   0x40:None,        # NT_UNSIGNED, Makes above signed integers
#                     # unsigned. Requires Igor Pro 3.0 or later.
    0x48:_numpy.uint8,
    0x49:complexUInt8,
    0x50:_numpy.uint16,
    0x51:complexUInt16,
    0x60:_numpy.uint32,
    0x61:complexUInt32,
}

# From wave.h
MAXDIMS = 4

# From binary.h
BinHeaderCommon = _Structure(  # WTK: this one is mine.
    name='BinHeaderCommon',
    fields=[
        _Field('h', 'version', help='Version number for backwards compatibility.'),
        ])

BinHeader1 = _Structure(
    name='BinHeader1',
    fields=[
        _Field('h', 'version', help='Version number for backwards compatibility.'),
        _Field('l', 'wfmSize', help='The size of the WaveHeader2 data structure plus the wave data plus 16 bytes of padding.'),
        _Field('h', 'checksum', help='Checksum over this header and the wave header.'),
        ])

BinHeader2 = _Structure(
    name='BinHeader2',
    fields=[
        _Field('h', 'version', help='Version number for backwards compatibility.'),
        _Field('l', 'wfmSize', help='The size of the WaveHeader2 data structure plus the wave data plus 16 bytes of padding.'),
        _Field('l', 'noteSize', help='The size of the note text.'),
        _Field('l', 'pictSize', default=0, help='Reserved. Write zero. Ignore on read.'),
        _Field('h', 'checksum', help='Checksum over this header and the wave header.'),
        ])

BinHeader3 = _Structure(
    name='BinHeader3',
    fields=[
        _Field('h', 'version', help='Version number for backwards compatibility.'),
        _Field('h', 'wfmSize', help='The size of the WaveHeader2 data structure plus the wave data plus 16 bytes of padding.'),
        _Field('l', 'noteSize', help='The size of the note text.'),
        _Field('l', 'formulaSize', help='The size of the dependency formula, if any.'),
        _Field('l', 'pictSize', default=0, help='Reserved. Write zero. Ignore on read.'),
        _Field('h', 'checksum', help='Checksum over this header and the wave header.'),
        ])

BinHeader5 = _Structure(
    name='BinHeader5',
    fields=[
        _Field('h', 'version', help='Version number for backwards compatibility.'),
        _Field('h', 'checksum', help='Checksum over this header and the wave header.'),
        _Field('l', 'wfmSize', help='The size of the WaveHeader5 data structure plus the wave data.'),
        _Field('l', 'formulaSize', help='The size of the dependency formula, if any.'),
        _Field('l', 'noteSize', help='The size of the note text.'),
        _Field('l', 'dataEUnitsSize', help='The size of optional extended data units.'),
        _Field('l', 'dimEUnitsSize', help='The size of optional extended dimension units.', count=MAXDIMS),
        _Field('l', 'dimLabelsSize', help='The size of optional dimension labels.', count=MAXDIMS),
        _Field('l', 'sIndicesSize', help='The size of string indicies if this is a text wave.'),
        _Field('l', 'optionsSize1', default=0, help='Reserved. Write zero. Ignore on read.'),
        _Field('l', 'optionsSize2', default=0, help='Reserved. Write zero. Ignore on read.'),
        ])


# From wave.h
MAX_WAVE_NAME2 = 18 # Maximum length of wave name in version 1 and 2
                    # files. Does not include the trailing null.
MAX_WAVE_NAME5 = 31 # Maximum length of wave name in version 5
                    # files. Does not include the trailing null.
MAX_UNIT_CHARS = 3

# Header to an array of waveform data.

WaveHeader2 = _Structure(
    name='WaveHeader2',
    fields=[
        _Field('h', 'type', help='See types (e.g. NT_FP64) above. Zero for text waves.'),
        _Field('P', 'next', default=0, help='Used in memory only. Write zero. Ignore on read.'),
        _Field('c', 'bname', help='Name of wave plus trailing null.', count=MAX_WAVE_NAME2+2),
        _Field('h', 'whVersion', default=0, help='Write 0. Ignore on read.'),
        _Field('h', 'srcFldr', default=0, help='Used in memory only. Write zero. Ignore on read.'),
        _Field('P', 'fileName', default=0, help='Used in memory only. Write zero. Ignore on read.'),
        _Field('c', 'dataUnits', default=0, help='Natural data units go here - null if none.', count=MAX_UNIT_CHARS+1),
        _Field('c', 'xUnits', default=0, help='Natural x-axis units go here - null if none.', count=MAX_UNIT_CHARS+1),
        _Field('l', 'npnts', help='Number of data points in wave.'),
        _Field('h', 'aModified', default=0, help='Used in memory only. Write zero. Ignore on read.'),
        _Field('d', 'hsA', help='X value for point p = hsA*p + hsB'),
        _Field('d', 'hsB', help='X value for point p = hsA*p + hsB'),
        _Field('h', 'wModified', default=0, help='Used in memory only. Write zero. Ignore on read.'),
        _Field('h', 'swModified', default=0, help='Used in memory only. Write zero. Ignore on read.'),
        _Field('h', 'fsValid', help='True if full scale values have meaning.'),
        _Field('d', 'topFullScale', help='The min full scale value for wave.'), # sic, 'min' should probably be 'max'
        _Field('d', 'botFullScale', help='The min full scale value for wave.'),
        _Field('c', 'useBits', default=0, help='Used in memory only. Write zero. Ignore on read.'),
        _Field('c', 'kindBits', default=0, help='Reserved. Write zero. Ignore on read.'),
        _Field('P', 'formula', default=0, help='Used in memory only. Write zero. Ignore on read.'),
        _Field('l', 'depID', default=0, help='Used in memory only. Write zero. Ignore on read.'),
        _Field('L', 'creationDate', help='DateTime of creation.  Not used in version 1 files.'),
        _Field('c', 'wUnused', default=0, help='Reserved. Write zero. Ignore on read.', count=2),
        _Field('L', 'modDate', help='DateTime of last modification.'),
        _Field('P', 'waveNoteH', help='Used in memory only. Write zero. Ignore on read.'),
        _Field('f', 'wData', help='The start of the array of waveform data.', count=4),
        ])

WaveHeader5 = _Structure(
    name='WaveHeader5',
    fields=[
        _Field('P', 'next', help='link to next wave in linked list.'),
        _Field('L', 'creationDate', help='DateTime of creation.'),
        _Field('L', 'modDate', help='DateTime of last modification.'),
        _Field('l', 'npnts', help='Total number of points (multiply dimensions up to first zero).'),
        _Field('h', 'type', help='See types (e.g. NT_FP64) above. Zero for text waves.'),
        _Field('h', 'dLock', default=0, help='Reserved. Write zero. Ignore on read.'),
        _Field('c', 'whpad1', default=0, help='Reserved. Write zero. Ignore on read.', count=6),
        _Field('h', 'whVersion', default=1, help='Write 1. Ignore on read.'),
        _Field('c', 'bname', help='Name of wave plus trailing null.', count=MAX_WAVE_NAME5+1),
        _Field('l', 'whpad2', default=0, help='Reserved. Write zero. Ignore on read.'),
        _Field('P', 'dFolder', default=0, help='Used in memory only. Write zero. Ignore on read.'),
        # Dimensioning info. [0] == rows, [1] == cols etc
        _Field('l', 'nDim', help='Number of of items in a dimension -- 0 means no data.', count=MAXDIMS),
        _Field('d', 'sfA', help='Index value for element e of dimension d = sfA[d]*e + sfB[d].', count=MAXDIMS),
        _Field('d', 'sfB', help='Index value for element e of dimension d = sfA[d]*e + sfB[d].', count=MAXDIMS),
        # SI units
        _Field('c', 'dataUnits', default=0, help='Natural data units go here - null if none.', count=MAX_UNIT_CHARS+1),
        _Field('c', 'dimUnits', default=0, help='Natural dimension units go here - null if none.', count=(MAXDIMS, MAX_UNIT_CHARS+1)),
        _Field('h', 'fsValid', help='TRUE if full scale values have meaning.'),
        _Field('h', 'whpad3', default=0, help='Reserved. Write zero. Ignore on read.'),
        _Field('d', 'topFullScale', help='The max and max full scale value for wave'), # sic, probably "max and min"
        _Field('d', 'botFullScale', help='The max and max full scale value for wave.'), # sic, probably "max and min"
        _Field('P', 'dataEUnits', default=0, help='Used in memory only. Write zero. Ignore on read.'),
        _Field('P', 'dimEUnits', default=0, help='Used in memory only. Write zero.  Ignore on read.', count=MAXDIMS),
        _Field('P', 'dimLabels', default=0, help='Used in memory only. Write zero.  Ignore on read.', count=MAXDIMS),
        _Field('P', 'waveNoteH', default=0, help='Used in memory only. Write zero. Ignore on read.'),
        _Field('l', 'whUnused', default=0, help='Reserved. Write zero. Ignore on read.', count=16),
        # The following stuff is considered private to Igor.
        _Field('h', 'aModified', default=0, help='Used in memory only. Write zero. Ignore on read.'),
        _Field('h', 'wModified', default=0, help='Used in memory only. Write zero. Ignore on read.'),
        _Field('h', 'swModified', default=0, help='Used in memory only. Write zero. Ignore on read.'),
        _Field('c', 'useBits', default=0, help='Used in memory only. Write zero. Ignore on read.'),
        _Field('c', 'kindBits', default=0, help='Reserved. Write zero. Ignore on read.'),
        _Field('P', 'formula', default=0, help='Used in memory only. Write zero. Ignore on read.'),
        _Field('l', 'depID', default=0, help='Used in memory only. Write zero. Ignore on read.'),
        _Field('h', 'whpad4', default=0, help='Reserved. Write zero. Ignore on read.'),
        _Field('h', 'srcFldr', default=0, help='Used in memory only. Write zero. Ignore on read.'),
        _Field('P', 'fileName', default=0, help='Used in memory only. Write zero. Ignore on read.'),
        _Field('P', 'sIndices', default=0, help='Used in memory only. Write zero. Ignore on read.'),
        _Field('f', 'wData', help='The start of the array of data.  Must be 64 bit aligned.', count=1),
        ])

# End IGOR constants and typedefs from IgorBin.h

def _version_structs(version, byte_order):
    if version == 1:
        bin = BinHeader1
        wave = WaveHeader2
    elif version == 2:
        bin = BinHeader2
        wave = WaveHeader2
    elif version == 3:
        bin = BinHeader3
        wave = WaveHeader2
    elif version == 5:
        bin = BinHeader5
        wave = WaveHeader5
    else:
        raise ValueError(
            ('This does not appear to be a valid Igor binary wave file. '
             'The version field = {}.\n').format(version))
    checkSumSize = bin.size + wave.size
    if version == 5:
        checkSumSize -= 4  # Version 5 checksum does not include the wData field.
    bin.set_byte_order(byte_order)
    wave.set_byte_order(byte_order)
    return (bin, wave, checkSumSize)

# Translated from ReadWave()
def load(filename, strict=True):
    if hasattr(filename, 'read'):
        f = filename  # filename is actually a stream object
    else:
        f = open(filename, 'rb')
    try:
        BinHeaderCommon.set_byte_order('=')
        b = buffer(f.read(BinHeaderCommon.size))
        version = BinHeaderCommon.unpack_dict_from(b)['version']
        needToReorderBytes = _need_to_reorder_bytes(version)
        byteOrder = _byte_order(needToReorderBytes)

        if needToReorderBytes:
            BinHeaderCommon.set_byte_order(byteOrder)
            version = BinHeaderCommon.unpack_dict_from(b)['version']
        bin_struct,wave_struct,checkSumSize = _version_structs(
            version, byteOrder)

        b = buffer(b + f.read(bin_struct.size + wave_struct.size - BinHeaderCommon.size))
        c = _checksum(b, byteOrder, 0, checkSumSize)
        if c != 0:
            raise ValueError(
                ('This does not appear to be a valid Igor binary wave file.  '
                 'Error in checksum: should be 0, is {}.').format(c))
        bin_info = bin_struct.unpack_dict_from(b)
        wave_info = wave_struct.unpack_dict_from(b, offset=bin_struct.size)
        if version in [1,2,3]:
            tail = 16  # 16 = size of wData field in WaveHeader2 structure
            waveDataSize = bin_info['wfmSize'] - wave_struct.size
            # =  bin_info['wfmSize']-16 - (wave_struct.size - tail)
        else:
            assert version == 5, version
            tail = 4  # 4 = size of wData field in WaveHeader5 structure
            waveDataSize = bin_info['wfmSize'] - (wave_struct.size - tail)
        # dtype() wrapping to avoid numpy.generic and
        # getset_descriptor issues with the builtin numpy types
        # (e.g. int32).  It has no effect on our local complex
        # integers.
        if version == 5:
            shape = [n for n in wave_info['nDim'] if n > 0] or (0,)
        else:
            shape = (wave_info['npnts'],)
        t = _numpy.dtype(_numpy.int8)  # setup a safe default
        if wave_info['type'] == 0:  # text wave
            shape = (waveDataSize,)
        elif wave_info['type'] in TYPE_TABLE or wave_info['npnts']:
            t = _numpy.dtype(TYPE_TABLE[wave_info['type']])
            assert waveDataSize == wave_info['npnts'] * t.itemsize, (
                '{}, {}, {}, {}'.format(
                    waveDataSize, wave_info['npnts'], t.itemsize, t))
        else:
            pass  # formula waves
        if wave_info['npnts'] == 0:
            data_b = buffer('')
        else:
            tail_data = _array.array('f', b[-tail:])
            data_b = buffer(buffer(tail_data) + f.read(waveDataSize-tail))
        data = _numpy.ndarray(
            shape=shape,
            dtype=t.newbyteorder(byteOrder),
            buffer=data_b,
            order='F',
            )

        if version == 1:
            pass  # No post-data information
        elif version == 2:
            # Post-data info:
            #   * 16 bytes of padding
            #   * Optional wave note data
            pad_b = buffer(f.read(16))  # skip the padding
            _assert_null(pad_b, strict=strict)
            bin_info['note'] = str(f.read(bin_info['noteSize'])).strip()
        elif version == 3:
            # Post-data info:
            #   * 16 bytes of padding
            #   * Optional wave note data
            #   * Optional wave dependency formula
            """Excerpted from TN003:

            A wave has a dependency formula if it has been bound by a
            statement such as "wave0 := sin(x)". In this example, the
            dependency formula is "sin(x)". The formula is stored with
            no trailing null byte.
            """
            pad_b = buffer(f.read(16))  # skip the padding
            _assert_null(pad_b, strict=strict)
            bin_info['note'] = str(f.read(bin_info['noteSize'])).strip()
            bin_info['formula'] = str(f.read(bin_info['formulaSize'])).strip()
        elif version == 5:
            # Post-data info:
            #   * Optional wave dependency formula
            #   * Optional wave note data
            #   * Optional extended data units data
            #   * Optional extended dimension units data
            #   * Optional dimension label data
            #   * String indices used for text waves only
            """Excerpted from TN003:

            dataUnits - Present in versions 1, 2, 3, 5. The dataUnits
              field stores the units for the data represented by the
              wave. It is a C string terminated with a null
              character. This field supports units of 0 to 3 bytes. In
              version 1, 2 and 3 files, longer units can not be
              represented. In version 5 files, longer units can be
              stored using the optional extended data units section of
              the file.

            xUnits - Present in versions 1, 2, 3. The xUnits field
              stores the X units for a wave. It is a C string
              terminated with a null character.  This field supports
              units of 0 to 3 bytes. In version 1, 2 and 3 files,
              longer units can not be represented.

            dimUnits - Present in version 5 only. This field is an
              array of 4 strings, one for each possible wave
              dimension. Each string supports units of 0 to 3
              bytes. Longer units can be stored using the optional
              extended dimension units section of the file.
            """
            bin_info['formula'] = str(f.read(bin_info['formulaSize'])).strip()
            bin_info['note'] = str(f.read(bin_info['noteSize'])).strip()
            bin_info['dataEUnits'] = str(f.read(bin_info['dataEUnitsSize'])).strip()
            bin_info['dimEUnits'] = [
                str(f.read(size)).strip() for size in bin_info['dimEUnitsSize']]
            bin_info['dimLabels'] = []
            for size in bin_info['dimLabelsSize']:
                labels = str(f.read(size)).split(chr(0)) # split null-delimited strings
                bin_info['dimLabels'].append([L for L in labels if len(L) > 0])
            if wave_info['type'] == 0:  # text wave
                bin_info['sIndices'] = f.read(bin_info['sIndicesSize'])

        if wave_info['type'] == 0:  # text wave
            # use sIndices to split data into strings
            strings = []
            start = 0
            for i,string_index in enumerate(bin_info['sIndices']):
                offset = ord(string_index)
                if offset > start:
                    string = data[start:offset]
                    strings.append(''.join(chr(x) for x in string))
                    start = offset
                else:
                    assert offset == 0, offset
            data = _numpy.array(strings)
            shape = [n for n in wave_info['nDim'] if n > 0] or (0,)
            data.reshape(shape)
    finally:
        if not hasattr(filename, 'read'):
            f.close()

    return data, bin_info, wave_info


def save(filename):
    raise NotImplementedError
