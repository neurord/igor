# Copyright

"Structure and Field classes for declaring structures "

from __future__ import absolute_import
import struct as _struct

import numpy as _numpy


_buffer = buffer  # save builtin buffer for clobbered situations


class Field (object):
    """Represent a Structure field.

    See Also
    --------
    Structure
    """
    def __init__(self, format, name, default=None, help=None, count=1):
        self.format = format # See the struct documentation
        self.name = name
        self.default = None
        self.help = help
        self.count = count
        self.total_count = _numpy.prod(count)


class Structure (_struct.Struct):
    """Represent a C structure.

    A convenient wrapper around struct.Struct that uses Fields and
    adds dict-handling methods for transparent name assignment.

    See Also
    --------
    Field

    Examples
    --------

    Represent the C structure::

        struct thing {
          short version;
          long size[3];
        }

    As

    >>> import array
    >>> from pprint import pprint
    >>> thing = Structure(name='thing',
    ...     fields=[Field('h', 'version'), Field('l', 'size', count=3)])
    >>> thing.set_byte_order('>')
    >>> b = array.array('b', range(2+4*3))
    >>> d = thing.unpack_dict_from(buffer=b)
    >>> pprint(d)
    {'size': array([ 33752069, 101124105, 168496141]), 'version': 1}
    >>> [hex(x) for x in d['size']]
    ['0x2030405L', '0x6070809L', '0xa0b0c0dL']

    You can even get fancy with multi-dimensional arrays.

    >>> thing = Structure(name='thing',
    ...     fields=[Field('h', 'version'), Field('l', 'size', count=(3,2))])
    >>> thing.set_byte_order('>')
    >>> b = array.array('b', range(2+4*3*2))
    >>> d = thing.unpack_dict_from(buffer=b)
    >>> d['size'].shape
    (3, 2)
    >>> pprint(d)
    {'size': array([[ 33752069, 101124105],
           [168496141, 235868177],
           [303240213, 370612249]]),
     'version': 1}
    """
    def __init__(self, name, fields, byte_order='='):
        # '=' for native byte order, standard size and alignment
        # See http://docs.python.org/library/struct for details
        self.name = name
        self.fields = fields
        self.set_byte_order(byte_order)

    def __str__(self):
        return self.name

    def set_byte_order(self, byte_order):
        """Allow changing the format byte_order on the fly.
        """
        if (hasattr(self, 'format') and self.format != None
            and self.format.startswith(byte_order)):
            return  # no need to change anything
        format = []
        for field in self.fields:
            format.extend([field.format]*field.total_count)
        super(Structure, self).__init__(
            format=byte_order+''.join(format).replace('P', 'L'))

    def _flatten_args(self, args):
        # handle Field.count > 0
        flat_args = []
        for a,f in zip(args, self.fields):
            if f.total_count > 1:
                flat_args.extend(a)
            else:
                flat_args.append(a)
        return flat_args

    def _unflatten_args(self, args):
        # handle Field.count > 0
        unflat_args = []
        i = 0
        for f in self.fields:
            if f.total_count > 1:
                data = _numpy.array(args[i:i+f.total_count])
                data = data.reshape(f.count)
                unflat_args.append(data)
            else:
                unflat_args.append(args[i])
            i += f.total_count
        return unflat_args
        
    def pack(self, *args):
        return super(Structure, self)(*self._flatten_args(args))

    def pack_into(self, buffer, offset, *args):
        return super(Structure, self).pack_into(
            buffer, offset, *self._flatten_args(args))

    def _clean_dict(self, dict):
        for f in self.fields:
            if f.name not in dict:
                if f.default != None:
                    dict[f.name] = f.default
                else:
                    raise ValueError('{} field not set for {}'.format(
                            f.name, self.__class__.__name__))
        return dict

    def pack_dict(self, dict):
        dict = self._clean_dict(dict)
        return self.pack(*[dict[f.name] for f in self.fields])

    def pack_dict_into(self, buffer, offset, dict={}):
        dict = self._clean_dict(dict)
        return self.pack_into(buffer, offset,
                              *[dict[f.name] for f in self.fields])

    def unpack(self, string):
        return self._unflatten_args(
            super(Structure, self).unpack(string))

    def unpack_from(self, buffer, offset=0):
        try:
            args = super(Structure, self).unpack_from(buffer, offset)
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
            unpacked = self._unflatten_args(args)
            data = dict(zip([f.name for f in self.fields],
                            unpacked))
            assert data['npnts'] == 0, data['npnts']
        return self._unflatten_args(args)

    def unpack_dict(self, string):
        return dict(zip([f.name for f in self.fields],
                        self.unpack(string)))

    def unpack_dict_from(self, buffer, offset=0):
        return dict(zip([f.name for f in self.fields],
                        self.unpack_from(buffer, offset)))
