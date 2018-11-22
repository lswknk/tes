from core.Device import *
from core.SOS import *


class GasEngine(Device):
    """ Define a class of gas engines """

    def __init__(self, name):
        super().__init__(name)
        self.input_variables = ['gas']
        self.output_variables = ['elec', 'smoke', 'co2']
        self.nameRate = self.name + '_Rate'

        self.maxCap = 1000
        self.minCap = 300
        self.pStartup = 10
        self.pShutDn = 5
        self.pMaintenance = 20
        self.MinUpTime = 1
        self.MinDnTime = 1
        self.IncRate = 0  # 爬坡速率
        self.DecRate = 0  # 爬坡速率
        # "x": input, "y":output
        self.pointList = [{"x": 0.0, "y": 3.666},
                          {"x": 58.24, "y": 3.63497},
                          {"x": 61.26, "y": 3.6699},
                          {"x": 68.12, "y": 3.7446},
                          {"x": 73.16, "y": 3.79489},
                          {"x": 77.77, "y": 3.8358},
                          {"x": 82.42, "y": 3.8691},
                          {"x": 86.05, "y": 3.876288},
                          ]

    def run(self):
        print_4s('# device: ' + self.name)
        self.declareBasicVars(self.input_variables, self.output_variables)
        self.declareOnOffVars()
        self.modelConstraints()
        print('')

    def modelConstraints(self):
        # Linearization for GasEngine model
        paraList = [self.pointList, self.nameFlag]
        SOS_ = SOS(paraList, self.nameGasIn, self.nameElecOut)
        SOS_.addSOS2()

        print_4s('for i in range(t_num):')
        # maximum and minimum capacity
        print_8s('prob += ' + self.nameSmokeOut + '[i] - ' + self.nameFlag + '[i] * ' + str(self.maxCap) + ' <= 0')
        print_8s('prob += ' + self.nameSmokeOut + '[i] - ' + self.nameFlag + '[i] * ' + str(self.minCap) + ' >= 0')
        # CO2 amount <-----> electricity
        print_8s('prob += ' + self.nameCo2Out + '[i] - 443*' + self.nameElecOut + '[i] == 0')
        # Output: 燃气内燃机输入为Gas,输出为smoke and electricity，功能比约：3:1
        # Gas -----> Smoke = Capacity * LoadRate
        print_8s('prob += ' + self.nameSmokeOut + '[i] - ' + self.nameElecOut + '[i] * 0.75 == 0')
