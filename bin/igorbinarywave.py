#!/usr/bin/env python
#
# Copyright

"IBW -> ASCII conversion"

import optparse
import pprint
import sys

import numpy

from igor import __version__
from igor.binarywave import loadibw


p = optparse.OptionParser(version=__version__)

p.add_option('-f', '--infile', dest='infile', metavar='FILE',
             default='-', help='Input IGOR Binary Wave (.ibw) file.')
p.add_option('-o', '--outfile', dest='outfile', metavar='FILE',
             default='-', help='File for ASCII output.')
p.add_option('-v', '--verbose', dest='verbose', default=0,
             action='count', help='Increment verbosity')
p.add_option('-n', '--not-strict', dest='strict', default=True,
             action='store_false', help='Attempt to parse invalid IBW files.')

options,args = p.parse_args()

if len(args) > 0 and options.infile == None:
    options.infile = args[0]
if options.infile == '-':
    options.infile = sys.stdin
if options.outfile == '-':
    options.outfile = sys.stdout

data,bin_info,wave_info = loadibw(options.infile, strict=options.strict)
numpy.savetxt(options.outfile, data, fmt='%g', delimiter='\t')
if options.verbose > 0:
    pprint.pprint(bin_info)
    pprint.pprint(wave_info)
