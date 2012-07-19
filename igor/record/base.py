# Copyright


class Record (object):
    def __init__(self, header, data, byte_order=None):
        self.header = header
        self.data = data
        self.byte_order = byte_order

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


# Copyright

from .base import Record


class TextRecord (Record):
    def __init__(self, *args, **kwargs):
        super(TextRecord, self).__init__(*args, **kwargs)
        self.text = str(self.data).replace('\r\n', '\n').replace('\r', '\n')
