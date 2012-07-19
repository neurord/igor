# Copyright

"Read IGOR Packed Experiment files files into records."

from .struct import Structure as _Structure
from .struct import Field as _Field
from .util import byte_order as _byte_order
from .util import need_to_reorder_bytes as _need_to_reorder_bytes
from .record import RECORD_TYPE as _RECORD_TYPE
from .record.base import UnknownRecord as _UnknownRecord
from .record.base import UnusedRecord as _UnusedRecord


# Igor writes other kinds of records in a packed experiment file, for
# storing things like pictures, page setup records, and miscellaneous
# settings.  The format for these records is quite complex and is not
# described in PTN003.  If you are writing a program to read packed
# files, you must skip any record with a record type that is not
# listed above.

PackedFileRecordHeader = _Structure(
    name='PackedFileRecordHeader',
    fields=[
        _Field('H', 'recordType', help='Record type plus superceded flag.'),
        _Field('h', 'version', help='Version information depends on the type of record.'),
        _Field('l', 'numDataBytes', help='Number of data bytes in the record following this record header.'),
        ])

#CR_STR = '\x15'  (\r)

PACKEDRECTYPE_MASK = 0x7FFF  # Record type = (recordType & PACKEDREC_TYPE_MASK)
SUPERCEDED_MASK = 0x8000  # Bit is set if the record is superceded by
                          # a later record in the packed file.


def load(filename, strict=True, ignore_unknown=True):
    records = []
    if hasattr(filename, 'read'):
        f = filename  # filename is actually a stream object
    else:
        f = open(filename, 'rb')
    byte_order = None
    initial_byte_order = '='
    try:
        while True:
            b = buffer(f.read(PackedFileRecordHeader.size))
            if not b:
                break
            PackedFileRecordHeader.set_byte_order(initial_byte_order)
            header = PackedFileRecordHeader.unpack_from(b)
            if header['version'] and not byte_order:
                need_to_reorder = _need_to_reorder_bytes(header['version'])
                byte_order = initial_byte_order = _byte_order(need_to_reorder)
                if need_to_reorder:
                    PackedFileRecordHeader.set_byte_order(byte_order)
                    header = PackedFileRecordHeader.unpack_from(b)
            data = buffer(f.read(header['numDataBytes']))
            record_type = _RECORD_TYPE.get(
                header['recordType'] & PACKEDRECTYPE_MASK, _UnknownRecord)
            if record_type in [_UnknownRecord, _UnusedRecord
                               ] and not ignore_unknown:
                raise KeyError('unkown record type {}'.format(
                        header['recordType']))
            records.append(record_type(header, data, byte_order=byte_order))
    finally:
        if not hasattr(filename, 'read'):
            f.close()

    return records

