# Copyright

"Interface for reading binary IGOR files."

__version__ = '0.2'


import logging as _logging


LOG = _logging.getLogger('igor')
LOG.setLevel(_logging.ERROR)
LOG.addHandler(_logging.StreamHandler())
LOG.handlers[-1].setFormatter(
    _logging.Formatter('%(name)s - %(levelname)s - %(message)s'))
