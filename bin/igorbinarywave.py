#!/usr/bin/env python
#
# Copyright

"IBW -> ASCII conversion"

import pprint

import numpy

from igor.binarywave import load
from igor.script import Script


def run(args):
    wave = load(args.infile)
    numpy.savetxt(args.outfile, wave['wave']['wData'], fmt='%g', delimiter='\t')
    if args.verbose > 0:
        wave['wave'].pop('wData')
        pprint.pprint(wave)

s = Script(description=__doc__)
s._run = run
s.run()
