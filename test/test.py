r"""Test the igor module by loading sample files.

>>> dumpibw('mac-double.ibw', strict=False)  # doctest: +REPORT_UDIFF
array([ 5.,  4.,  3.,  2.,  1.])
{'checksum': 25137,
 'note': '',
 'noteSize': 0,
 'pictSize': 0,
 'version': 2,
 'wfmSize': 166}
{'aModified': 0,
 'bname': array(['d', 'o', 'u', 'b', 'l', 'e', '', '', '', '', '', '', '', '', '',
       '', '', '', '', ''],
      dtype='|S1'),
 'botFullScale': 0.0,
 'creationDate': 3001587842,
 'dataUnits': array(['', '', '', ''],
      dtype='|S1'),
 'depID': 0,
 'fileName': 0,
 'formula': 0,
 'fsValid': 0,
 'hsA': 1.0,
 'hsB': 0.0,
 'kindBits': '\x00',
 'modDate': 3001587842,
 'next': 0,
 'npnts': 5,
 'srcFldr': 0,
 'swModified': 0,
 'topFullScale': 0.0,
 'type': 4,
 'useBits': '\x00',
 'wData': array([ 2.3125,  0.    ,  2.25  ,  0.    ]),
 'wModified': 0,
 'wUnused': array(['', ''],
      dtype='|S1'),
 'waveNoteH': 0,
 'whVersion': 0,
 'xUnits': array(['', '', '', ''],
      dtype='|S1')}

>>> dumpibw('mac-textWave.ibw')  # doctest: +REPORT_UDIFF
array(['Mary', 'had', 'a', 'little', 'lamb'],
      dtype='|S6')
{'checksum': 5554,
 'dataEUnits': '',
 'dataEUnitsSize': 0,
 'dimEUnits': ['', '', '', ''],
 'dimEUnitsSize': array([0, 0, 0, 0]),
 'dimLabels': [[], [], [], []],
 'dimLabelsSize': array([0, 0, 0, 0]),
 'formula': '',
 'formulaSize': 0,
 'note': '',
 'noteSize': 0,
 'optionsSize1': 0,
 'optionsSize2': 0,
 'sIndices': '\x00\x00\x00\x04\x00\x00\x00\x07\x00\x00\x00\x08\x00\x00\x00\x0e\x00\x00\x00\x12',
 'sIndicesSize': 20,
 'version': 5,
 'wfmSize': 338}
{'aModified': 0,
 'bname': array(['t', 'e', 'x', 't', '0', '', '', '', '', '', '', '', '', '', '', '',
       '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
      dtype='|S1'),
 'botFullScale': 0.0,
 'creationDate': 3001571199,
 'dFolder': 69554896,
 'dLock': 0,
 'dataEUnits': 0,
 'dataUnits': array(['', '', '', ''],
      dtype='|S1'),
 'depID': 22,
 'dimEUnits': array([0, 0, 0, 0]),
 'dimLabels': array([0, 0, 0, 0]),
 'dimUnits': array([['', '', '', ''],
       ['', '', '', ''],
       ['', '', '', ''],
       ['', '', '', '']],
      dtype='|S1'),
 'fileName': 0,
 'formula': 0,
 'fsValid': 0,
 'kindBits': '\x00',
 'modDate': 3001571215,
 'nDim': array([5, 0, 0, 0]),
 'next': 0,
 'npnts': 5,
 'sIndices': 69557296,
 'sfA': array([ 1.,  1.,  1.,  1.]),
 'sfB': array([ 0.,  0.,  0.,  0.]),
 'srcFldr': 0,
 'swModified': 1,
 'topFullScale': 0.0,
 'type': 0,
 'useBits': '\x00',
 'wData': 236398480.0,
 'wModified': 0,
 'waveNoteH': 0,
 'whUnused': array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
 'whVersion': 1,
 'whpad1': array(['', '', '', '', '', ''],
      dtype='|S1'),
 'whpad2': 0,
 'whpad3': 0,
 'whpad4': 0}

>>> dumpibw('mac-version2.ibw', strict=False)  # doctest: +REPORT_UDIFF
array([ 5.,  4.,  3.,  2.,  1.], dtype=float32)
{'checksum': -16803,
 'note': 'This is a test.',
 'noteSize': 15,
 'pictSize': 0,
 'version': 2,
 'wfmSize': 146}
{'aModified': 0,
 'bname': array(['v', 'e', 'r', 's', 'i', 'o', 'n', '2', '', '', '', '', '', '', '',
       '', '', '', '', ''],
      dtype='|S1'),
 'botFullScale': 0.0,
 'creationDate': 3001251979,
 'dataUnits': array(['', '', '', ''],
      dtype='|S1'),
 'depID': 0,
 'fileName': 0,
 'formula': 0,
 'fsValid': 0,
 'hsA': 1.0,
 'hsB': 0.0,
 'kindBits': '\x00',
 'modDate': 3001573594,
 'next': 0,
 'npnts': 5,
 'srcFldr': 0,
 'swModified': 0,
 'topFullScale': 0.0,
 'type': 2,
 'useBits': '\x00',
 'wData': array([ 5.,  4.,  3.,  2.]),
 'wModified': 0,
 'wUnused': array(['', ''],
      dtype='|S1'),
 'waveNoteH': 0,
 'whVersion': 0,
 'xUnits': array(['', '', '', ''],
      dtype='|S1')}

>>> dumpibw('mac-version3Dependent.ibw', strict=False)  # doctest: +REPORT_UDIFF
array([], dtype=int8)
{'checksum': 0,
 'formula': '',
 'formulaSize': 0,
 'note': '',
 'noteSize': 8257536,
 'pictSize': 262144,
 'version': 3,
 'wfmSize': 0}
{'aModified': 10,
 'bname': array(['', '', 'v', 'e', 'r', 's', 'i', 'o', 'n', '3', 'D', 'e', 'p', 'e',
       'n', 'd', 'e', 'n', 't', ''],
      dtype='|S1'),
 'botFullScale': 0.0,
 'creationDate': 1507328,
 'dataUnits': array(['', '', '', ''],
      dtype='|S1'),
 'depID': -487849984,
 'fileName': 0,
 'formula': 1577,
 'fsValid': 1,
 'hsA': 4.5193417557662e-309,
 'hsB': 0.0,
 'kindBits': '\x00',
 'modDate': 45801,
 'next': 131072,
 'npnts': 0,
 'srcFldr': 0,
 'swModified': 1,
 'topFullScale': 0.0,
 'type': -32334,
 'useBits': '\x00',
 'wData': array([ 0.,  0.,  0.,  0.]),
 'wModified': 0,
 'wUnused': array(['', ''],
      dtype='|S1'),
 'waveNoteH': 3835494400,
 'whVersion': 0,
 'xUnits': array(['', '', '', ''],
      dtype='|S1')}

>>> dumpibw('mac-version5.ibw')  # doctest: +REPORT_UDIFF
array([ 5.,  4.,  3.,  2.,  1.], dtype=float32)
{'checksum': -12033,
 'dataEUnits': '',
 'dataEUnitsSize': 0,
 'dimEUnits': ['', '', '', ''],
 'dimEUnitsSize': array([0, 0, 0, 0]),
 'dimLabels': [['Column0'], [], [], []],
 'dimLabelsSize': array([64,  0,  0,  0]),
 'formula': '',
 'formulaSize': 0,
 'note': 'This is a test.',
 'noteSize': 15,
 'optionsSize1': 0,
 'optionsSize2': 0,
 'sIndicesSize': 0,
 'version': 5,
 'wfmSize': 340}
{'aModified': 0,
 'bname': array(['v', 'e', 'r', 's', 'i', 'o', 'n', '5', '', '', '', '', '', '', '',
       '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
      dtype='|S1'),
 'botFullScale': 0.0,
 'creationDate': 3001252180,
 'dFolder': 69554896,
 'dLock': 0,
 'dataEUnits': 0,
 'dataUnits': array(['', '', '', ''],
      dtype='|S1'),
 'depID': 27,
 'dimEUnits': array([0, 0, 0, 0]),
 'dimLabels': array([69554136,        0,        0,        0]),
 'dimUnits': array([['', '', '', ''],
       ['', '', '', ''],
       ['', '', '', ''],
       ['', '', '', '']],
      dtype='|S1'),
 'fileName': 69554292,
 'formula': 0,
 'fsValid': 0,
 'kindBits': '\x00',
 'modDate': 3001573601,
 'nDim': array([5, 0, 0, 0]),
 'next': 69555212,
 'npnts': 5,
 'sIndices': 0,
 'sfA': array([ 1.,  1.,  1.,  1.]),
 'sfB': array([ 0.,  0.,  0.,  0.]),
 'srcFldr': -32349,
 'swModified': 1,
 'topFullScale': 0.0,
 'type': 2,
 'useBits': '\x00',
 'wData': 5.0,
 'wModified': 0,
 'waveNoteH': 69554032,
 'whUnused': array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
 'whVersion': 1,
 'whpad1': array(['', '', '', '', '', ''],
      dtype='|S1'),
 'whpad2': 0,
 'whpad3': 0,
 'whpad4': 0}

>>> dumpibw('mac-zeroPointWave.ibw')  # doctest: +REPORT_UDIFF
array([], dtype=float32)
{'checksum': -15649,
 'dataEUnits': '',
 'dataEUnitsSize': 0,
 'dimEUnits': ['', '', '', ''],
 'dimEUnitsSize': array([0, 0, 0, 0]),
 'dimLabels': [[], [], [], []],
 'dimLabelsSize': array([0, 0, 0, 0]),
 'formula': '',
 'formulaSize': 0,
 'note': '',
 'noteSize': 0,
 'optionsSize1': 0,
 'optionsSize2': 0,
 'sIndicesSize': 0,
 'version': 5,
 'wfmSize': 320}
{'aModified': 3,
 'bname': array(['z', 'e', 'r', 'o', 'W', 'a', 'v', 'e', '', '', '', '', '', '', '',
       '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
      dtype='|S1'),
 'botFullScale': 0.0,
 'creationDate': 3001573964,
 'dFolder': 69554896,
 'dLock': 0,
 'dataEUnits': 0,
 'dataUnits': array(['', '', '', ''],
      dtype='|S1'),
 'depID': 29,
 'dimEUnits': array([0, 0, 0, 0]),
 'dimLabels': array([0, 0, 0, 0]),
 'dimUnits': array([['', '', '', ''],
       ['', '', '', ''],
       ['', '', '', ''],
       ['', '', '', '']],
      dtype='|S1'),
 'fileName': 0,
 'formula': 0,
 'fsValid': 0,
 'kindBits': '\x00',
 'modDate': 3001573964,
 'nDim': array([0, 0, 0, 0]),
 'next': 0,
 'npnts': 0,
 'sIndices': 0,
 'sfA': array([ 1.,  1.,  1.,  1.]),
 'sfB': array([ 0.,  0.,  0.,  0.]),
 'srcFldr': 0,
 'swModified': 1,
 'topFullScale': 0.0,
 'type': 2,
 'useBits': '\x00',
 'wData': 0.0,
 'wModified': 1,
 'waveNoteH': 0,
 'whUnused': array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
 'whVersion': 1,
 'whpad1': array(['', '', '', '', '', ''],
      dtype='|S1'),
 'whpad2': 0,
 'whpad3': 0,
 'whpad4': 0}

>>> dumpibw('win-double.ibw')  # doctest: +REPORT_UDIFF
array([ 5.,  4.,  3.,  2.,  1.])
{'checksum': 28962,
 'note': '',
 'noteSize': 0,
 'pictSize': 0,
 'version': 2,
 'wfmSize': 166}
{'aModified': 0,
 'bname': array(['d', 'o', 'u', 'b', 'l', 'e', '', '', '', '', '', '', '', '', '',
       '', '', '', '', ''],
      dtype='|S1'),
 'botFullScale': 0.0,
 'creationDate': 3001587842,
 'dataUnits': array(['', '', '', ''],
      dtype='|S1'),
 'depID': 0,
 'fileName': 0,
 'formula': 0,
 'fsValid': 0,
 'hsA': 1.0,
 'hsB': 0.0,
 'kindBits': '\x00',
 'modDate': 3001587842,
 'next': 0,
 'npnts': 5,
 'srcFldr': 0,
 'swModified': 0,
 'topFullScale': 0.0,
 'type': 4,
 'useBits': '\x00',
 'wData': array([ 0.    ,  2.3125,  0.    ,  2.25  ]),
 'wModified': 0,
 'wUnused': array(['', ''],
      dtype='|S1'),
 'waveNoteH': 0,
 'whVersion': 0,
 'xUnits': array(['', '', '', ''],
      dtype='|S1')}

>>> dumpibw('win-textWave.ibw')  # doctest: +REPORT_UDIFF
array(['Mary', 'had', 'a', 'little', 'lamb'],
      dtype='|S6')
{'checksum': 184,
 'dataEUnits': '',
 'dataEUnitsSize': 0,
 'dimEUnits': ['', '', '', ''],
 'dimEUnitsSize': array([0, 0, 0, 0]),
 'dimLabels': [[], [], [], []],
 'dimLabelsSize': array([0, 0, 0, 0]),
 'formula': '',
 'formulaSize': 0,
 'note': '',
 'noteSize': 0,
 'optionsSize1': 0,
 'optionsSize2': 0,
 'sIndices': '\x04\x00\x00\x00\x07\x00\x00\x00\x08\x00\x00\x00\x0e\x00\x00\x00\x12\x00\x00\x00',
 'sIndicesSize': 20,
 'version': 5,
 'wfmSize': 338}
{'aModified': 0,
 'bname': array(['t', 'e', 'x', 't', '0', '', '', '', '', '', '', '', '', '', '', '',
       '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
      dtype='|S1'),
 'botFullScale': 0.0,
 'creationDate': 3001571199,
 'dFolder': 8108612,
 'dLock': 0,
 'dataEUnits': 0,
 'dataUnits': array(['', '', '', ''],
      dtype='|S1'),
 'depID': 32,
 'dimEUnits': array([0, 0, 0, 0]),
 'dimLabels': array([0, 0, 0, 0]),
 'dimUnits': array([['', '', '', ''],
       ['', '', '', ''],
       ['', '', '', ''],
       ['', '', '', '']],
      dtype='|S1'),
 'fileName': 7814472,
 'formula': 0,
 'fsValid': 0,
 'kindBits': '\x00',
 'modDate': 3001571215,
 'nDim': array([5, 0, 0, 0]),
 'next': 0,
 'npnts': 5,
 'sIndices': 8133100,
 'sfA': array([ 1.,  1.,  1.,  1.]),
 'sfB': array([ 0.,  0.,  0.,  0.]),
 'srcFldr': -1007,
 'swModified': 0,
 'topFullScale': 0.0,
 'type': 0,
 'useBits': '\x00',
 'wData': 7.865683337909351e+34,
 'wModified': 1,
 'waveNoteH': 0,
 'whUnused': array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
 'whVersion': 1,
 'whpad1': array(['', '', '', '', '', ''],
      dtype='|S1'),
 'whpad2': 0,
 'whpad3': 0,
 'whpad4': 0}

>>> dumpibw('win-version2.ibw')  # doctest: +REPORT_UDIFF
array([ 5.,  4.,  3.,  2.,  1.], dtype=float32)
{'checksum': 1047,
 'note': 'This is a test.',
 'noteSize': 15,
 'pictSize': 0,
 'version': 2,
 'wfmSize': 146}
{'aModified': 0,
 'bname': array(['v', 'e', 'r', 's', 'i', 'o', 'n', '2', '', '', '', '', '', '', '',
       '', '', '', '', ''],
      dtype='|S1'),
 'botFullScale': 0.0,
 'creationDate': 3001251979,
 'dataUnits': array(['', '', '', ''],
      dtype='|S1'),
 'depID': 0,
 'fileName': 0,
 'formula': 0,
 'fsValid': 0,
 'hsA': 1.0,
 'hsB': 0.0,
 'kindBits': '\x00',
 'modDate': 3001573594,
 'next': 0,
 'npnts': 5,
 'srcFldr': 0,
 'swModified': 0,
 'topFullScale': 0.0,
 'type': 2,
 'useBits': '\x00',
 'wData': array([ 5.,  4.,  3.,  2.]),
 'wModified': 0,
 'wUnused': array(['', ''],
      dtype='|S1'),
 'waveNoteH': 0,
 'whVersion': 0,
 'xUnits': array(['', '', '', ''],
      dtype='|S1')}

>>> dumpibw('win-version5.ibw')  # doctest: +REPORT_UDIFF
array([ 5.,  4.,  3.,  2.,  1.], dtype=float32)
{'checksum': 13214,
 'dataEUnits': '',
 'dataEUnitsSize': 0,
 'dimEUnits': ['', '', '', ''],
 'dimEUnitsSize': array([0, 0, 0, 0]),
 'dimLabels': [['Column0'], [], [], []],
 'dimLabelsSize': array([64,  0,  0,  0]),
 'formula': '',
 'formulaSize': 0,
 'note': 'This is a test.',
 'noteSize': 15,
 'optionsSize1': 0,
 'optionsSize2': 0,
 'sIndicesSize': 0,
 'version': 5,
 'wfmSize': 340}
{'aModified': 0,
 'bname': array(['v', 'e', 'r', 's', 'i', 'o', 'n', '5', '', '', '', '', '', '', '',
       '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
      dtype='|S1'),
 'botFullScale': 0.0,
 'creationDate': 3001252180,
 'dFolder': 8108612,
 'dLock': 0,
 'dataEUnits': 0,
 'dataUnits': array(['', '', '', ''],
      dtype='|S1'),
 'depID': 30,
 'dimEUnits': array([0, 0, 0, 0]),
 'dimLabels': array([8138784,       0,       0,       0]),
 'dimUnits': array([['', '', '', ''],
       ['', '', '', ''],
       ['', '', '', ''],
       ['', '', '', '']],
      dtype='|S1'),
 'fileName': 8131824,
 'formula': 0,
 'fsValid': 0,
 'kindBits': '\x00',
 'modDate': 3001573601,
 'nDim': array([5, 0, 0, 0]),
 'next': 8125236,
 'npnts': 5,
 'sIndices': 0,
 'sfA': array([ 1.,  1.,  1.,  1.]),
 'sfB': array([ 0.,  0.,  0.,  0.]),
 'srcFldr': -1007,
 'swModified': 0,
 'topFullScale': 0.0,
 'type': 2,
 'useBits': '\x00',
 'wData': 5.0,
 'wModified': 1,
 'waveNoteH': 8131596,
 'whUnused': array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
 'whVersion': 1,
 'whpad1': array(['', '', '', '', '', ''],
      dtype='|S1'),
 'whpad2': 0,
 'whpad3': 0,
 'whpad4': 0}

>>> dumpibw('win-zeroPointWave.ibw')  # doctest: +REPORT_UDIFF
array([], dtype=float32)
{'checksum': 27541,
 'dataEUnits': '',
 'dataEUnitsSize': 0,
 'dimEUnits': ['', '', '', ''],
 'dimEUnitsSize': array([0, 0, 0, 0]),
 'dimLabels': [[], [], [], []],
 'dimLabelsSize': array([0, 0, 0, 0]),
 'formula': '',
 'formulaSize': 0,
 'note': '',
 'noteSize': 0,
 'optionsSize1': 0,
 'optionsSize2': 0,
 'sIndicesSize': 0,
 'version': 5,
 'wfmSize': 320}
{'aModified': 3,
 'bname': array(['z', 'e', 'r', 'o', 'W', 'a', 'v', 'e', '', '', '', '', '', '', '',
       '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
      dtype='|S1'),
 'botFullScale': 0.0,
 'creationDate': 3001573964,
 'dFolder': 8108612,
 'dLock': 0,
 'dataEUnits': 0,
 'dataUnits': array(['', '', '', ''],
      dtype='|S1'),
 'depID': 31,
 'dimEUnits': array([0, 0, 0, 0]),
 'dimLabels': array([0, 0, 0, 0]),
 'dimUnits': array([['', '', '', ''],
       ['', '', '', ''],
       ['', '', '', ''],
       ['', '', '', '']],
      dtype='|S1'),
 'fileName': 8125252,
 'formula': 0,
 'fsValid': 0,
 'kindBits': '\x00',
 'modDate': 3001573964,
 'nDim': array([0, 0, 0, 0]),
 'next': 8133140,
 'npnts': 0,
 'sIndices': 0,
 'sfA': array([ 1.,  1.,  1.,  1.]),
 'sfB': array([ 0.,  0.,  0.,  0.]),
 'srcFldr': -1007,
 'swModified': 0,
 'topFullScale': 0.0,
 'type': 2,
 'useBits': '\x00',
 'wData': 0.0,
 'wModified': 1,
 'waveNoteH': 0,
 'whUnused': array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
 'whVersion': 1,
 'whpad1': array(['', '', '', '', '', ''],
      dtype='|S1'),
 'whpad2': 0,
 'whpad3': 0,
 'whpad4': 0}

>>> dumppxp('polar-graphs-demo.pxp')    # doctest: +REPORT_UDIFF, +ELLIPSIS
record 0:
<UnknownRecord-11 ...>
record 1:
<UnknownRecord-12 ...>
record 2:
<UnknownRecord-13 ...>
record 3:
<UnknownRecord-13 ...>
record 4:
<UnknownRecord-13 ...>
record 5:
<UnknownRecord-13 ...>
record 6:
<UnknownRecord-13 ...>
record 7:
<UnknownRecord-13 ...>
record 8:
<UnknownRecord-13 ...>
record 9:
<UnknownRecord-14 ...>
record 10:
<UnknownRecord-15 ...>
record 11:
<UnknownRecord-16 ...>
record 12:
<UnknownRecord-16 ...>
record 13:
<UnknownRecord-17 ...>
record 14:
<UnknownRecord-17 ...>
record 15:
<UnknownRecord-17 ...>
record 16:
<UnknownRecord-17 ...>
record 17:
<UnknownRecord-17 ...>
record 18:
<UnknownRecord-17 ...>
record 19:
<UnknownRecord-16 ...>
record 20:
<UnknownRecord-17 ...>
record 21:
<UnknownRecord-17 ...>
record 22:
<UnknownRecord-17 ...>
record 23:
<UnknownRecord-17 ...>
record 24:
<UnknownRecord-17 ...>
record 25:
<UnknownRecord-17 ...>
record 26:
<UnknownRecord-18 ...>
record 27:
<UnknownRecord-11 ...>
record 28:
<UnknownRecord-26 ...>
record 29:
<UnknownRecord-26 ...>
record 30:
<VariablesRecord ...>
record 31:
<HistoryRecord ...>
record 32:
<WaveRecord ...>
record 33:
<WaveRecord ...>
record 34:
<WaveRecord ...>
record 35:
<WaveRecord ...>
record 36:
<WaveRecord ...>
record 37:
<WaveRecord ...>
record 38:
<WaveRecord ...>
record 39:
<WaveRecord ...>
record 40:
<FolderStartRecord ...>
record 41:
<FolderStartRecord ...>
record 42:
<VariablesRecord ...>
record 43:
<FolderEndRecord ...>
record 44:
<FolderStartRecord ...>
record 45:
<VariablesRecord ...>
record 46:
<FolderEndRecord ...>
record 47:
<FolderEndRecord ...>
record 48:
<RecreationRecord ...>
record 49:
<GetHistoryRecord ...>
record 50:
<ProcedureRecord ...>
"""

import os.path
from pprint import pformat
import sys

from igor.binarywave import load as loadibw
from igor.packed import load as loadpxp


_this_dir = os.path.dirname(__file__)
_data_dir = os.path.join(_this_dir, 'data')

def dumpibw(filename, strict=True):
    sys.stderr.write('Testing {}\n'.format(filename))
    path = os.path.join(_data_dir, filename)
    data,bin_info,wave_info = loadibw(path, strict=strict)
    pprint(data)
    pprint(bin_info)
    pprint(wave_info)

def dumppxp(filename, strict=True):
    sys.stderr.write('Testing {}\n'.format(filename))
    path = os.path.join(_data_dir, filename)
    records = loadpxp(path, strict=strict)
    for i,record in enumerate(records):
        print('record {}:'.format(i))
        pprint(record)

def pprint(data):
    lines = pformat(data).splitlines()
    print('\n'.join([line.rstrip() for line in lines]))
