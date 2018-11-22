from core.SOS import *
from core.Device import *


class GasSteamBoiler(Device):
    """
    Define a class of gas steam boiler. 
    """

    def __init__(self, name):
        super().__init__(name)
        self.input_variables = ['gas', 'water']
        self.output_variables = ['steam']

        self.maxCap = 10
        self.minCap = 1.9
        self.pStartup = 180  # RMB per start-up
        self.pShutDn = 80  # RMB per shut-down
        self.pMaintenance = 10  # RMB per on
        self.pLCOE = 12.77  # RMB per kwh per day
        self.MinUpTime = 25
        self.MinDnTime = 10
        # "x": 负荷率， "y":能效
        multiple = 1
        self.pointList = [{"y": 3.0, "x": 252.1008403*multiple},
                          {"y": 3.5, "x": 292.8870293*multiple},
                          {"y": 4.0, "x": 333.3333333*multiple},
                          {"y": 4.5, "x": 373.4439834*multiple},
                          {"y": 5.0, "x": 413.2231405*multiple},
                          {"y": 5.5, "x": 452.6748971*multiple},
                          {"y": 6.0, "x": 491.8032787*multiple},
                          {"y": 6.5, "x": 530.6122449*multiple},
                          {"y": 7.0, "x": 569.1056911*multiple},
                          {"y": 7.5, "x": 607.2874494*multiple},
                          {"y": 8.0, "x": 645.1612903*multiple}]


    def run(self):
        print_4s('# device: ' + self.name)
        self.declareBasicVars(self.input_variables, self.output_variables)
        self.declareOnOffVars()
        self.modelConstraints()
        print('')

    def modelConstraints(self):
        # linearization for GasSteamBoiler model
        paraList = [self.pointList, self.nameFlag]
        SOS_ = SOS(paraList, self.nameGasIn, self.nameSteamOut)
        SOS_.addSOS2()

        # maximum and minimum capacity
        print_4s('for i in range(t_num):')
        print_8s('prob += ' + self.nameSteamOut + '[i] - ' + self.nameFlag + '[i] * ' + str(
            self.maxCap) + ' <= 0')
        print_8s('prob += ' + self.nameSteamOut + '[i] - ' + self.nameFlag + '[i] * ' + str(
            self.minCap) + ' >= 0')
