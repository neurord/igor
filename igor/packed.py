# Copyright

from io import BytesIO as _BytesIO

from .binarywave import load as _loadibw
from .struct import Structure as _Structure
from .struct import Field as _Field

"Read IGOR Packed Experiment files files into records."


class Record (object):
    def __init__(self, header, data):
        self.header = header
        self.data = data

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, id(self))


class UnknownRecord (Record):
    def __repr__(self):
        return '<{}-{} {}>'.format(
            self.__class__.__name__, self.header['recordType'], id(self))


class UnusedRecord (Record):
    pass


class VariablesRecord (Record):
    pass


class HistoryRecord (Record):
    pass


class WaveRecord (Record):
    def __init__(self, *args, **kwargs):
        super(WaveRecord, self).__init__(*args, **kwargs)
        self.wave = _loadibw(_BytesIO(bytes(self.data)), strict=False)

    def __str__(self):
        return str(self.wave)

    def __repr__(self):
        return str(self.wave)


class RecreationRecord (Record):
    pass


class ProcedureRecord (Record):
    pass


class GetHistoryRecord (Record):
    pass


class PackedFileRecord (Record):
    pass


class FolderStartRecord (Record):
    pass


class FolderEndRecord (Record):
    pass


# From PackedFile.h
RECORD_TYPE = {
    0: UnusedRecord,
    1: VariablesRecord,
    2: HistoryRecord,
    3: WaveRecord,
    4: RecreationRecord,
    5: ProcedureRecord,
    6: UnusedRecord,
    7: GetHistoryRecord,
    8: PackedFileRecord,
    9: FolderStartRecord,
    10: FolderEndRecord,
    }

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
    try:
        while True:
            PackedFileRecordHeader.set_byte_order('=')
            b = buffer(f.read(PackedFileRecordHeader.size))
            if not b:
                break
            header = PackedFileRecordHeader.unpack_from(b)
            data = buffer(f.read(header['numDataBytes']))
            record_type = RECORD_TYPE.get(
                header['recordType'] & PACKEDRECTYPE_MASK, UnknownRecord)
            if record_type in [UnknownRecord, UnusedRecord
                               ] and not ignore_unknown:
                raise KeyError('unkown record type {}'.format(
                        header['recordType']))
            records.append(record_type(header, data))
    finally:
        if not hasattr(filename, 'read'):
            f.close()

    return records

