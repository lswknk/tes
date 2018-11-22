import sys
from core.utils import print_4s, print_8s
from core.Source import *
from core.Photovoltaic import *

def connect_forward(fromUnit=None, toUnits=None, type=None):
    if not type:
        print_4s(fromUnit.name + ':Specify the type of energies transferred.')
        sys.exit()
    else:
        klen = len(toUnits)
        tempFrom = eval('fromUnit.name' + type.capitalize() + "Out")
        for unit in toUnits:
            tempTo = eval('unit.name' + type.capitalize() + "In")
            tempName = tempFrom + '__' + tempTo
            print_4s(tempName + ' = LpVariable.dicts("' + tempName + '", aList, 0, None)')
            # if isinstance(fromUnit, Source) and type == 'elec':
            # if isinstance(toUnits, Photovoltaic) and type == 'elec':
            #     print_4s(tempName + ' = LpVariable.dicts("' + tempName + '", aList, None, 0)')
            # else:
            #     print_4s(tempName + ' = LpVariable.dicts("' + tempName + '", aList, 0, None)')
        print_4s('for i in range(t_num):')
        print_8s('prob += ' + tempFrom + '[i]', end=' ')
        for k, unit in enumerate(toUnits):
            print('- ', end='')
            tempTo = eval('unit.name' + type.capitalize() + "In")
            tempName = tempFrom + '__' + tempTo
            print(tempName + '[i]', end=' ')
        print('== 0')


def connect_backward(fromUnits=None, toUnit=None, type=None):
    if not type:
        print_4s(toUnit.name + ':Specify the type of energies transferred.')
        sys.exit()
    else:
        tempTo = eval('toUnit.name' + type.capitalize() + "In")
        print_4s('for i in range(t_num):')
        print_8s('prob += ' + tempTo + '[i]', end=' ')
        for k, unit in enumerate(fromUnits):
            print('- ', end='')
            tempFrom = eval('unit.name' + type.capitalize() + "Out")
            tempName = tempFrom + '__' + tempTo
            print(tempName + '[i]', end=' ')
        print('== 0')
