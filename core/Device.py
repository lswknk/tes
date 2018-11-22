from core.Base import *
from core.utils import print_4s, print_8s


class Device(Base):
    """
    Define a class of devices.
    """

    def __init__(self, name):
        super().__init__(name)
        self.nameFlag = self.name + '_flag'
        self.nameUpFlag = self.name + '_sUpflag'
        self.nameDnFlag = self.name + '_sDnflag'
        self.initState = name + '_initState'

    def declareBasicVars(self, input_variables, output_variables):
        # variables
        super().declareBasicVars(sublist=input_variables, in_out='in')
        super().declareBasicVars(sublist=output_variables, in_out='out')
        self.declareVariable(varname=self.nameFlag, lowerbound=0, upperbound=1, varType='LpInteger')

    def declareOnOffVars(self):
        # print(u"# 启停状态变量约束")
        self.declareVariable(varname=self.nameUpFlag, lowerbound=0, upperbound=1, varType='LpInteger')
        self.declareVariable(varname=self.nameDnFlag, lowerbound=0, upperbound=1, varType='LpInteger')

        # print(u"# 考虑设备初始状态")
        print_4s(self.initState + " = int(isOffMap['" + self.name + "'])")
        print_4s('prob += ' + self.nameFlag + '[0] - ' + str(
            self.initState) + ' - ' + self.nameUpFlag + '[0] + ' + self.nameDnFlag + '[0] == 0')

        print_4s('for i in range(t_num - 1):')
        print_8s(
            'prob += ' + self.nameFlag + '[i + 1] - ' + self.nameFlag + '[i] - ' + self.nameUpFlag + '[i + 1] + ' + self.nameDnFlag + '[i+1] == 0')
        print_8s('prob += ' + self.nameDnFlag + '[i] + ' + self.nameUpFlag + '[i] <= 1')
        print_4s('prob += ' + self.nameDnFlag + '[t_num - 1] + ' + self.nameUpFlag + '[t_num - 1] <= 1')
