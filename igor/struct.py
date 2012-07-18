# Copyright

"""Structure and Field classes for declaring structures

There are a few formats that can be used to represent the same data, a
binary packed format with all the data in a buffer, a linearized
format with each field in a single Python list, and a nested format
with each field in a hierarchy of Python dictionaries.
"""

from __future__ import absolute_import
import struct as _struct

import numpy as _numpy


_buffer = buffer  # save builtin buffer for clobbered situations


class Field (object):
    """Represent a Structure field.

    The format argument can be a format character from the ``struct``
    documentation (e.g., ``c`` for ``char``, ``h`` for ``short``, ...)
    or ``Structure`` instance (for building nested structures).

    Examples
    --------

    >>> from pprint import pprint
    >>> import numpy

    Example of an unsigned short integer field:

    >>> time = Field(
    ...     'I', 'time', default=0, help='POSIX time')
    >>> time.total_count
    1
    >>> list(time.pack_data(1))
    [1]
    >>> list(time.pack_item(2))
    [2]
    >>> time.unpack_data([3])
    3
    >>> time.unpack_item([4])
    4

    Example of a multi-dimensional float field:

    >>> data = Field(
    ...     'f', 'data', help='example data', count=(2,3,4))
    >>> data.total_count
    24
    >>> list(data.indexes())  # doctest: +ELLIPSIS
    [[0, 0, 0], [0, 0, 1], [0, 0, 2], [0, 0, 3], [0, 1, 0], ..., [1, 2, 3]]
    >>> list(data.pack_data(
    ...     [[[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11]],
    ...      [[12, 13, 14, 15], [16, 17, 18, 19], [20, 21, 22, 23]]])
    ...     )  # doctest: +ELLIPSIS
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, ..., 19, 20, 21, 22, 23]
    >>> list(data.pack_item(3))
    [3]
    >>> data.unpack_data(range(data.total_count))
    array([[[ 0,  1,  2,  3],
            [ 4,  5,  6,  7],
            [ 8,  9, 10, 11]],
    <BLANKLINE>
           [[12, 13, 14, 15],
            [16, 17, 18, 19],
            [20, 21, 22, 23]]])
    >>> data.unpack_item([3])
    3

    Example of a nested structure field:

    >>> run = Structure('run', fields=[time, data])
    >>> runs = Field(run, 'runs', help='pair of runs', count=2)
    >>> runs.total_count  # = 2 * (1 + 24)
    50
    >>> data1 = numpy.arange(data.total_count).reshape(data.count)
    >>> data2 = data1 + data.total_count
    >>> list(runs.pack_data(
    ...     [{'time': 100, 'data': data1},
    ...      {'time': 101, 'data': data2}])
    ...     )  # doctest: +ELLIPSIS
    [100, 0, 1, 2, ..., 22, 23, 101, 24, 25, ..., 46, 47]
    >>> list(runs.pack_item({'time': 100, 'data': data1})
    ...     )  # doctest: +ELLIPSIS
    [100, 0, 1, 2, ..., 22, 23]
    >>> pprint(runs.unpack_data(range(runs.total_count)))
    [{'data': array([[[ 1,  2,  3,  4],
            [ 5,  6,  7,  8],
            [ 9, 10, 11, 12]],
    <BLANKLINE>
           [[13, 14, 15, 16],
            [17, 18, 19, 20],
            [21, 22, 23, 24]]]),
      'time': 0},
     {'data': array([[[26, 27, 28, 29],
            [30, 31, 32, 33],
            [34, 35, 36, 37]],
    <BLANKLINE>
           [[38, 39, 40, 41],
            [42, 43, 44, 45],
            [46, 47, 48, 49]]]),
      'time': 25}]
    >>> pprint(runs.unpack_item(range(runs.structure_count)))
    {'data': array([[[ 1,  2,  3,  4],
            [ 5,  6,  7,  8],
            [ 9, 10, 11, 12]],
    <BLANKLINE>
           [[13, 14, 15, 16],
            [17, 18, 19, 20],
            [21, 22, 23, 24]]]),
     'time': 0}

    If you don't give enough values for an array field, the remaining
    values are filled in with their defaults.

    >>> list(data.pack_data(
    ...     [[[0, 1, 2, 3], [4, 5, 6]], [[10]]]))  # doctest: +ELLIPSIS
    Traceback (most recent call last):
      ...
    ValueError: no default for <Field data ...>
    >>> data.default = 0
    >>> list(data.pack_data(
    ...     [[[0, 1, 2, 3], [4, 5, 6]], [[10]]]))
    [0, 1, 2, 3, 4, 5, 6, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    See Also
    --------
    Structure
    """
    def __init__(self, format, name, default=None, help=None, count=1):
        self.format = format
        self.name = name
        self.default = default
        self.help = help
        self.count = count
        self.item_count = _numpy.prod(count)  # number of item repeats
        if isinstance(self.format, Structure):
            self.structure_count = sum(f.total_count for f in format.fields)
            self.total_count = self.item_count * self.structure_count
        else:
            self.total_count = self.item_count  # struct.Struct format chars

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return '<{} {} {}>'.format(
            self.__class__.__name__, self.name, id(self))

    def indexes(self):
        """Iterate through indexes to a possibly multi-dimensional array"""
        assert self.item_count > 1, self
        try:
            i = [0] * len(self.count)
        except TypeError:  # non-iterable count
            for i in range(self.count):
                yield i
        else:
            for i in range(self.item_count):
                index = []
                for j,c in enumerate(reversed(self.count)):
                    index.insert(0, i % c)
                    i /= c
                yield index

    def pack_data(self, data=None):
        """Linearize a single field's data to a flat list.

        If the field is repeated (count > 1), the incoming data should
        be iterable with each iteration returning a single item.
        """
        if self.item_count > 1:
            if data is None:
                data = []
            if hasattr(data, 'flat'):  # take advantage of numpy's ndarray.flat
                items = 0
                for item in data.flat:
                    items += 1
                    for arg in self.pack_item(item):
                        yield arg
                if items < self.item_count:
                    if f.default is None:
                        raise ValueError(
                            'no default for {}.{}'.format(self, f))
                    for i in range(self.item_count - items):
                        yield f.default
            else:
                for index in self.indexes():
                    try:
                        if isinstance(index, int):
                            item = data[index]
                        else:
                            item = data
                            for i in index:
                                item = item[i]
                    except IndexError:
                        item = None
                    for arg in self.pack_item(item):
                        yield arg
        elif self.item_count:
            for arg in self.pack_item(data):
                yield arg

    def pack_item(self, item=None):
        """Linearize a single count of the field's data to a flat iterable
        """
        if isinstance(self.format, Structure):
            for i in self.format._pack_item(item):
                yield i
        elif item is None:
            if self.default is None:
                raise ValueError('no default for {}'.format(self))
            yield self.default
        else:
            yield item

    def unpack_data(self, data):
        """Inverse of .pack_data"""
        iterator = iter(data)
        try:
            items = [iterator.next() for i in range(self.total_count)]
        except StopIteration:
            raise ValueError('not enough data to unpack {}'.format(self))
        try:
            iterator.next()
        except StopIteration:
            pass
        else:
            raise ValueError('too much data to unpack {}'.format(self))
        if isinstance(self.format, Structure):
            # break into per-structure clumps
            s = self.structure_count
            items = zip(*[items[i::s] for i in range(s)])
        else:
            items = [[i] for i in items]
        unpacked = [self.unpack_item(i) for i in items]
        if self.count == 1:
            return unpacked[0]
        if isinstance(self.format, Structure):
            try:
                len(self.count)
            except TypeError:
                pass
            else:
                raise NotImplementedError('reshape Structure field')
        else:
            unpacked = _numpy.array(unpacked)
            unpacked = unpacked.reshape(self.count)
        return unpacked

    def unpack_item(self, item): 
        """Inverse of .unpack_item"""
        if isinstance(self.format, Structure):
            return self.format._unpack_item(item)
        else:
            assert len(item) == 1, item
            return item[0]


class Structure (_struct.Struct):
    r"""Represent a C structure.

    A convenient wrapper around struct.Struct that uses Fields and
    adds dict-handling methods for transparent name assignment.

    See Also
    --------
    Field

    Examples
    --------

    >>> import array
    >>> from pprint import pprint

    Represent the C structures::

        struct run {
          unsigned int time;
          short data[2][3];
        }

        struct experiment {
          unsigned short version;
          struct run runs[2];
        }

    As

    >>> time = Field('I', 'time', default=0, help='POSIX time')
    >>> data = Field(
    ...     'h', 'data', default=0, help='example data', count=(2,3))
    >>> run = Structure('run', fields=[time, data])
    >>> version = Field(
    ...     'H', 'version', default=1, help='example version')
    >>> runs = Field(run, 'runs', help='pair of runs', count=2)
    >>> experiment = Structure('experiment', fields=[version, runs])

    The structures automatically calculate the flattened data format:

    >>> run.format
    '=Ihhhhhh'
    >>> run.size  # 4 + 2*3*2
    16
    >>> experiment.format
    '=HIhhhhhhIhhhhhh'
    >>> experiment.size  # 2 + 2*(4 + 2*3*2)
    34

    You can read data out of any object supporting the buffer
    interface:

    >>> b = array.array('B', range(experiment.size))
    >>> experiment.set_byte_order('>')
    >>> d = experiment.unpack_from(buffer=b)
    >>> pprint(d)
    {'runs': [{'data': array([[1543, 2057, 2571],
           [3085, 3599, 4113]]),
               'time': 33752069},
              {'data': array([[5655, 6169, 6683],
           [7197, 7711, 8225]]),
               'time': 303240213}],
     'version': 1}
    >>> [hex(x) for x in d['runs'][0]['data'].flat]
    ['0x607L', '0x809L', '0xa0bL', '0xc0dL', '0xe0fL', '0x1011L']

    You can also read out from strings:

    >>> d = experiment.unpack(b.tostring())
    >>> pprint(d)
    {'runs': [{'data': array([[1543, 2057, 2571],
           [3085, 3599, 4113]]),
               'time': 33752069},
              {'data': array([[5655, 6169, 6683],
           [7197, 7711, 8225]]),
               'time': 303240213}],
     'version': 1}

    If you don't give enough values for an array field, the remaining
    values are filled in with their defaults.

    >>> experiment.pack_into(buffer=b, data=d)
    >>> b.tostring()[:17]
    '\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10'
    >>> b.tostring()[17:]
    '\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !'
    >>> run0 = d['runs'].pop(0)
    >>> b = experiment.pack(data=d)
    >>> b[:17]
    '\x00\x01\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f '
    >>> b[17:]
    '!\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

    If you set ``count=0``, the field is ignored.

    >>> experiment2 = Structure('experiment', fields=[
    ...     version, Field('f', 'ignored', count=0), runs], byte_order='>')
    >>> experiment2.format
    '>HIhhhhhhIhhhhhh'
    >>> d = experiment2.unpack(b)
    >>> pprint(d)
    {'ignored': array([], dtype=float64),
     'runs': [{'data': array([[5655, 6169, 6683],
           [7197, 7711, 8225]]),
               'time': 303240213},
              {'data': array([[0, 0, 0],
           [0, 0, 0]]), 'time': 0}],
     'version': 1}
    >>> del d['ignored']
    >>> b2 = experiment2.pack(d)
    >>> b2 == b
    True
    """
    def __init__(self, name, fields, byte_order='='):
        # '=' for native byte order, standard size and alignment
        # See http://docs.python.org/library/struct for details
        self.name = name
        self.fields = fields
        self.set_byte_order(byte_order)

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<{} {} {}>'.format(
            self.__class__.__name__, self.name, id(self))

    def set_byte_order(self, byte_order):
        """Allow changing the format byte_order on the fly.
        """
        if (hasattr(self, 'format') and self.format != None
            and self.format.startswith(byte_order)):
            return  # no need to change anything
        format = []
        for field in self.fields:
            if isinstance(field.format, Structure):
                field_format = field.format.sub_format(
                    ) * field.item_count
            else:
                field_format = [field.format]*field.item_count
            format.extend(field_format)
        super(Structure, self).__init__(
            format=byte_order+''.join(format).replace('P', 'L'))

    def sub_format(self):
        return self.format.lstrip('=<>')  # byte order handled by parent

    def _pack_item(self, item=None):
        """Linearize a single count of the structure's data to a flat iterable
        """
        if item is None:
            item = {}
        for f in self.fields:
            try:
                data = item[f.name]
            except TypeError:
                raise ValueError((f.name, item))
            except KeyError:
                data = None
            for arg in f.pack_data(data):
                yield arg

    def _unpack_item(self, args):
        """Inverse of ._unpack_item"""
        data = {}
        iterator = iter(args)
        for f in self.fields:
            try:
                items = [iterator.next() for i in range(f.total_count)]
            except StopIteration:
                raise ValueError('not enough data to unpack {}.{}'.format(
                        self, f))
            data[f.name] = f.unpack_data(items)
        try:
            iterator.next()
        except StopIteration:
            pass
        else:
            raise ValueError('too much data to unpack {}'.format(self))
        return data

    def pack(self, data):
        args = list(self._pack_item(data))
        return super(Structure, self).pack(*args)

    def pack_into(self, buffer, offset=0, data={}):
        args = list(self._pack_item(data))
        return super(Structure, self).pack_into(
            buffer, offset, *args)

    def unpack(self, *args, **kwargs):
        args = super(Structure, self).unpack(*args, **kwargs)
        return self._unpack_item(args)

    def unpack_from(self, buffer, offset=0, *args, **kwargs):
        try:
            args = super(Structure, self).unpack_from(
                buffer, offset, *args, **kwargs)
        except _struct.error as e:
            if not self.name in ('WaveHeader2', 'WaveHeader5'):
                raise
            # HACK!  For WaveHeader5, when npnts is 0, wData is
            # optional.  If we couldn't unpack the structure, fill in
            # wData with zeros and try again, asserting that npnts is
            # zero.
            if len(buffer) - offset < self.size:
                # missing wData?  Pad with zeros
                buffer += _buffer('\x00'*(self.size + offset - len(buffer)))
            args = super(Structure, self).unpack_from(buffer, offset)
            data = self._unpack_item(args)
            assert data['npnts'] == 0, data['npnts']
        return self._unpack_item(args)
