from core.Device import *
from core.SOS import *


class HRSG(Device):
    """ Define a class of Heat recovery steam generator """

    def __init__(self, name):
        super().__init__(name)
        self.input_variables = ['smoke', 'water']
        self.output_variables = ['steam']
        self.nameRate = name + '_rate'
        self.maxCap = 4.0
        self.minCap = 1.0
        self.pStartup = 180
        self.pShutDn = 80
        self.pMaintenance = 10
        self.MinUpTime = 25
        self.MinDnTime = 10
        self.IncRate = 0
        self.DecRate = 0

        # "x": 负荷率， "y":能效
        self.pointList = [{"x": 41.4, "y": 0.02},
                          {"x": 46.4, "y": 0.013},
                          {"x": 51.4, "y": 0.012},
                          {"x": 54.4, "y": 0.014},
                          {"x": 61.4, "y": 0.013}]

    def run(self):
        print_4s('# device: ' + self.name)
        self.declareBasicVars(self.input_variables, self.output_variables)
        self.declareOnOffVars()
        self.modelConstraints()
        print('')

    def modelConstraints(self):
        # linearization for HeatRecoverrySteamGenerotor model
        paraList = [self.pointList, self.nameFlag]
        SOS_ = SOS(paraList, self.nameSmokeIn, self.nameSteamOut)
        SOS_.addSOS2()

        print_4s('for i in range(t_num):')
        # maximum and minimum capacity
        print_8s('prob += ' + self.nameSteamOut + '[i] - ' + self.nameFlag + '[i] * ' + str(
            self.maxCap) + ' <= 0')
        print_8s('prob += ' + self.nameSteamOut + '[i] - ' + self.nameFlag + '[i] * ' + str(
            self.minCap) + ' >= 0')
