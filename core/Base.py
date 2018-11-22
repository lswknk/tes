from core.utils import print_4s, print_8s


class Base:
    """
    Define a class of devices. A device contains only variables but without methods.
    """

    def __init__(self, name):
        self.name = name
        self.nameCoolIn = name + '_cE' + '_in'
        self.nameSteamIn = name + '_hESt' + '_in'
        self.nameSmokeIn = name + '_hESm' + '_in'
        self.nameHotwaterIn = name + '_hEWt' + '_in'
        self.nameElecIn = name + '_eE' + '_in'
        self.nameGasIn = name + '_gE' + '_in'
        self.nameWaterIn = name + '_wA' + '_in'
        self.nameCo2In = name + '_co2' + '_in'

        self.nameCoolOut = name + '_cE' + '_out'
        self.nameSteamOut = name + '_hESt' + '_out'
        self.nameSmokeOut = name + '_hESm' + '_out'
        self.nameHotwaterOut = name + '_hEWt' + '_out'
        self.nameElecOut = name + '_eE' + '_out'
        self.nameGasOut = name + '_gE' + '_out'
        self.nameWaterOut = name + '_wA' + '_out'
        self.nameCo2Out = name + '_co2' + '_out'

    def run(self):
        print_4s('# device: ' + self.name)
        self.declareBasicVars()
        print()

    def declareBasicVars(self, sublist=('cool', 'steam', 'smoke', 'hotwater', 'elec', 'gas', 'water', 'co2'),
                         lowerbound=0, upperbound=None, varType='LpContinuous', in_out='in'):
        # x = LpVariable.dicts("x", list, LB_ind, UB_ind, "Integer")
        for item in sublist:
            temp = eval('self.name' + item.capitalize() + in_out.capitalize())
            self.declareVariable(temp, lowerbound, upperbound, varType)

    @staticmethod
    def declareVariable(varname=None, lowerbound=0, upperbound=None, varType='LpContinuous'):
        print_4s(str(varname) + ' = LpVariable.dicts("' + str(varname)
                 + '", aList, ' + str(lowerbound) + ', ' + str(upperbound) + ', ' + varType + ')')
