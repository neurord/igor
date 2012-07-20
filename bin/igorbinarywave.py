#!/usr/bin/env python
#
# Copyright

"IBW -> ASCII conversion"

import logging
import optparse
import pprint
import sys

import numpy

from igor import __version__, LOG
from igor.binarywave import load


p = optparse.OptionParser(version=__version__)

p.add_option('-f', '--infile', dest='infile', metavar='FILE',
             default='-', help='Input IGOR Binary Wave (.ibw) file.')
p.add_option('-o', '--outfile', dest='outfile', metavar='FILE',
             default='-', help='File for ASCII output.')
p.add_option('-v', '--verbose', dest='verbose', default=0,
             action='count', help='Increment verbosity')

options,args = p.parse_args()

if len(args) > 0 and options.infile == None:
    options.infile = args[0]
if options.infile == '-':
    options.infile = sys.stdin
if options.outfile == '-':
    options.outfile = sys.stdout

if options.verbose > 1:
    log_levels = [logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG]
    log_level = log_levels[min(options.verbose-1, len(log_levels)-1)]
    LOG.setLevel(log_level)

wave = load(options.infile)
numpy.savetxt(options.outfile, wave['wave']['wData'], fmt='%g', delimiter='\t')
if options.verbose > 0:
    wave['wave'].pop('wData')
    pprint.pprint(wave)
