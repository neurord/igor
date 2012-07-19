# Copyright

from ..binarywave import TYPE_TABLE as _TYPE_TABLE
from ..struct import Structure as _Structure
from ..struct import Field as _Field
from ..util import byte_order as _byte_order
from ..util import need_to_reorder_bytes as _need_to_reorder_bytes
from .base import Record


VarHeaderCommon = _Structure(
    name='VarHeaderCommon',
    fields=[
        _Field('h', 'version', help='Version number for this header.'),
        ])

# From Variables.h
VarHeader1 = _Structure(
    name='VarHeader1',
    fields=[
        _Field('h', 'version', help='Version number is 1 for this header.'),
        _Field('h', 'numSysVars', help='Number of system variables (K0, K1, ...).'),
        _Field('h', 'numUserVars', help='Number of user numeric variables -- may be zero.'),
        _Field('h', 'numUserStrs', help='Number of user string variables -- may be zero.'),
        ])

# From Variables.h
VarHeader2 = _Structure(
    name='VarHeader2',
    fields=[
        _Field('h', 'version', help='Version number is 2 for this header.'),
        _Field('h', 'numSysVars', help='Number of system variables (K0, K1, ...).'),
        _Field('h', 'numUserVars', help='Number of user numeric variables -- may be zero.'),
        _Field('h', 'numUserStrs', help='Number of user string variables -- may be zero.'),
        _Field('h', 'numDependentVars', help='Number of dependent numeric variables -- may be zero.'),
        _Field('h', 'numDependentStrs', help='Number of dependent string variables -- may be zero.'),
        ])

# From Variables.h
UserStrVarRec1 = _Structure(
    name='UserStrVarRec1',
    fields=[
        _Field('c', 'name', help='Name of the string variable.', count=32),
        _Field('h', 'strLen', help='The real size of the following array.'),
        _Field('c', 'data'),
        ])

# From Variables.h
UserStrVarRec2 = _Structure(
    name='UserStrVarRec2',
    fields=[
        _Field('c', 'name', help='Name of the string variable.', count=32),
        _Field('l', 'strLen', help='The real size of the following array.'),
        _Field('c', 'data'),
        ])

# From Variables.h
VarNumRec = _Structure(
    name='VarNumRec',
    fields=[
        _Field('h', 'numType', help='Type from binarywave.TYPE_TABLE'),
        _Field('d', 'realPart', help='The real part of the number.'),
        _Field('d', 'imagPart', help='The imag part if the number is complex.'),
        _Field('l', 'reserved', help='Reserved - set to zero.'),
        ])

# From Variables.h
UserNumVarRec = _Structure(
    name='UserNumVarRec',
    fields=[
        _Field('c', 'name', help='Name of the string variable.', count=32),
        _Field('h', 'type', help='0 = string, 1 = numeric.'),
        _Field(VarNumRec, 'num', help='Type and value of the variable if it is numeric.  Not used for string.'),
        ])

# From Variables.h
UserDependentVarRec = _Structure(
    name='UserDependentVarRec',
    fields=[
        _Field('c', 'name', help='Name of the string variable.', count=32),
        _Field('h', 'type', help='0 = string, 1 = numeric.'),
        _Field(VarNumRec, 'num', help='Type and value of the variable if it is numeric.  Not used for string.'),
        _Field('h', 'formulaLen', help='The length of the dependency formula.'),
        _Field('c', 'formula', help='Start of the dependency formula. A C string including null terminator.'),
        ])


class VariablesRecord (Record):
    def __init__(self, *args, **kwargs):
        super(VariablesRecord, self).__init__(*args, **kwargs)
        # self.header['version']  # record version always 0?
        version = self._set_byte_order_and_get_version()
        self.structure = self._get_structure(version)
        self.variables = self.structure.unpack_from(self.data)
        self.variables.update(self._unpack_variable_length_structures(version))
        self._normalize_variables()

    def _set_byte_order_and_get_version(self):
        if self.byte_order:
            VarHeaderCommon.set_byte_order(self.byte_order)
        else:
            VarHeaderCommon.set_byte_order('=')            
        version = VarHeaderCommon.unpack_from(self.data)['version']
        if not self.byte_order:
            need_to_reorder = _need_to_reorder_bytes(version)
            self.byte_order = _byte_order(need_to_reorder)
            if need_to_reorder:
                VarHeaderCommon.set_byte_order(self.byte_order)
                version = VarHeaderCommon.unpack_from(self.data)['version']
        return version

    def _get_structure(self, version):
        if version == 1:
            header_struct = VarHeader1
        elif version == 2:
            header_struct = VarHeader2
        else:
            raise NotImplementedError(
                'Variables record version {}'.format(version))
        header = header_struct.unpack_from(self.data)
        fields = [
            _Field(header_struct, 'header', help='VarHeader'),
            _Field('f', 'sysVars', help='system variables',
                   count=header['numSysVars']),
            _Field(UserNumVarRec, 'userVars', help='user variables',
                   count=header['numUserVars']),
            ]
        return _Structure(name='variables', fields=fields)

    def _unpack_variable_length_structures(self, version):
        data = {'userStrs': []}
        offset = self.structure.size

        if version == 1:
            user_str_var_struct = UserStrVarRec1
        elif version == 2:
            user_str_var_struct = UserStrVarRec2
        else:
            raise NotImplementedError(
                'Variables record version {}'.format(version))
        user_str_var_struct.set_byte_order(self.byte_order)
        for i in range(self.variables['header']['numUserStrs']):
            d = user_str_var_struct.unpack_from(self.data, offset)
            offset += user_str_var_struct.size
            end = offset + d['strLen'] - 1  # one character already in struct
            if d['strLen']:
                d['data'] = d['data'] + self.data[offset:end]
            else:
                d['data'] = ''
            offset = end
            data['userStrs'].append(d)

        if version == 2:
            data.update({'dependentVars': [], 'dependentStrs': []})
            UserDependentVarRec.set_byte_order(self.byte_order)
            for i in range(self.variables['header']['numDependentVars']):
                d,offset = self._unpack_dependent_variable(offset)
                data['dependentVars'].append(d)
            for i in range(self.variables['header']['numDependentStrs']):
                d,offset = self._unpack_dependent_variable(offset)
                data['dependentStrs'].append(d)

        if offset != len(self.data):
            raise ValueError('too much data ({} extra bytes)'.format(
                    len(self.data)-offset))
        return data

    def _unpack_dependent_variable(self, offset):
        d = UserDependentVarRec.unpack_from(self.data, offset)
        offset += UserDependentVarRec.size
        end = offset + d['formulaLen'] - 1  # one character already in struct
        if d['formulaLen']:
            d['formula'] = d['formula'] + self.data[offset:end]
        else:
            d['formula'] = ''
        offset = end
        return (d, offset)

    def _normalize_variables(self):
        user_vars = {}
        for num_var in self.variables['userVars']:
            key,value = self._normalize_user_numeric_variable(num_var)
            user_vars[key] = value
        self.variables['userVars'] = user_vars
        user_strs = {}
        for str_var in self.variables['userStrs']:
            name = self._normalize_null_terminated_string(str_var['name'])
            user_strs[name] = str_var['data']
        if self.variables['header']['version'] == 2:
            raise NotImplementedError('normalize dependent variables')
        self.variables['userStrs'] = user_strs

    def _normalize_null_terminated_string(self, string):
        return string.tostring().split('\x00', 1)[0]

    def _normalize_user_numeric_variable(self, user_num_var):
        user_num_var['name'] = self._normalize_null_terminated_string(
            user_num_var['name'])
        if user_num_var['type']:  # numeric
            value = self._normalize_numeric_variable(user_num_var['num'])
        else:  # string
            value = None
        return (user_num_var['name'], value)

    def _normalize_numeric_variable(self, num_var):
        t = _TYPE_TABLE[num_var['numType']]
        if num_var['numType'] % 2:  # complex number
            return t(complex(num_var['realPart'], num_var['imagPart']))
        else:
            return t(num_var['realPart'])
