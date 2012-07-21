#!/usr/bin/env python
#
# Copyright (C) 2012 W. Trevor King <wking@tremily.us>
#
# This file is part of igor.
#
# igor is free software: you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# igor is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with igor.  If not, see <http://www.gnu.org/licenses/>.

"PXP -> ASCII conversion"

import pprint

import numpy

from igor.packed import load
from igor.script import Script


def run(args):
    records,filesystem = load(args.infile)
    if hasattr(args.outfile, 'write'):
        f = args.outfile  # filename is actually a stream object
    else:
        f = open(args.outfile, 'w')
    try:
        f.write(pprint.pformat(records))
        f.write('\n')
    finally:
        if f != args.outfile:
            f.close()
    if args.verbose > 0:
        pprint.pprint(filesystem)

s = Script(description=__doc__, filetype='IGOR Packed Experiment (.pxp) file')
s._run = run
s.run()
