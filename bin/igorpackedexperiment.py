#!/usr/bin/env python
#
# Copyright

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
