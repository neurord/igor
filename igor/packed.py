# Copyright

"Read IGOR Packed Experiment files files into records."

from .struct import Structure as _Structure
from .struct import Field as _Field
from .util import byte_order as _byte_order
from .util import need_to_reorder_bytes as _need_to_reorder_bytes
from .record import RECORD_TYPE as _RECORD_TYPE
from .record.base import UnknownRecord as _UnknownRecord
from .record.base import UnusedRecord as _UnusedRecord
from .record.folder import FolderStartRecord as _FolderStartRecord
from .record.folder import FolderEndRecord as _FolderEndRecord
from .record.variables import VariablesRecord as _VariablesRecord
from .record.wave import WaveRecord as _WaveRecord


# From PTN003:
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

    # From PTN003:
    """The name must be a valid Igor data folder name. See Object
    Names in the Igor Reference help file for name rules.

    When Igor Pro reads the data folder start record, it creates a new
    data folder with the specified name. Any subsequent variable, wave
    or data folder start records cause Igor to create data objects in
    this new data folder, until Igor Pro reads a corresponding data
    folder end record."""
    # From the Igor Manual, chapter 2, section 8, page II-123
    # http://www.wavemetrics.net/doc/igorman/II-08%20Data%20Folders.pdf
    """Like the Macintosh file system, Igor Pro's data folders use the
    colon character (:) to separate components of a path to an
    object. This is analogous to Unix which uses / and Windows which
    uses \. (Reminder: Igor's data folders exist wholly in memory
    while an experiment is open. It is not a disk file system!)

    A data folder named "root" always exists and contains all other
    data folders.
    """
    # From the Igor Manual, chapter 4, page IV-2
    # http://www.wavemetrics.net/doc/igorman/IV-01%20Commands.pdf
    """For waves and data folders only, you can also use "liberal"
    names. Liberal names can include almost any character, including
    spaces and dots (see Liberal Object Names on page III-415 for
    details).
    """
    # From the Igor Manual, chapter 3, section 16, page III-416
    # http://www.wavemetrics.net/doc/igorman/III-16%20Miscellany.pdf
    """Liberal names have the same rules as standard names except you
    may use any character except control characters and the following:

      " ' : ;
    """
    filesystem = {'root': {}}
    dir_stack = [('root', filesystem['root'])]
    for record in records:
        cwd = dir_stack[-1][-1]
        if isinstance(record, _FolderStartRecord):
            name = record.null_terminated_text
            cwd[name] = {}
            dir_stack.append((name, cwd[name]))
        elif isinstance(record, _FolderEndRecord):
            dir_stack.pop()
        elif isinstance(record, (_VariablesRecord, _WaveRecord)):
            if isinstance(record, _VariablesRecord):
                filename = ':variables'  # start with an invalid character
            else:                        # to avoid collisions with folder
                filename = ':waves'      # names
            if filename in cwd:
                cwd[filename].append(record)
            else:
                cwd[filename] = [record]

    return (records, filesystem)

