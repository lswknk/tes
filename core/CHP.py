from core.SOS import *
from core.Device import *


class CHP(Device):
    """
    Define a class of CHP.
    """

    def __init__(self, name):
        super().__init__(name)
        self.input_variables = ['gas', 'water']
        self.output_variables = ['steam', 'elec']

        self.maxCap = 4300  # kW
        self.minCap = 1000
        self.pStartup = 180
        self.pShutDn = 80
        self.pMaintenance = 10
        self.pLCOE = 1.37
        self.MinUpTime = 25
        self.MinDnTime = 10
        self.elec_vs_steam = 1450
        # "x":input, "y": output
        self.pointList = [{"y": 1836.915819, "x":518.6894996},
                          {"y": 2252.918131, "x":614.480147},
                          {"y": 2504.618355, "x":689.0343857},
                          {"y": 2634.596652, "x":717.9003396},
                          {"y": 2929.227812, "x":782.262432},
                          {"y": 3146.116096, "x":829.0399983},
                          {"y": 3344.345436, "x":871.8672414},
                          {"y": 3544.128508, "x":916.0146866},
                          {"y": 3782.25761, "x": 974.7874015},
                          {"y": 4015.460475, "x":1031.210707}]

    def run(self):
        print_4s('# device: ' + self.name)
        self.declareBasicVars(self.input_variables, self.output_variables)
        self.declareOnOffVars()
        self.modelConstraints()
        print('')

    def modelConstraints(self):
        # linearization for CHP model
        paraList = [self.pointList, self.nameFlag]
        SOS_ = SOS(paraList, self.nameGasIn, self.nameElecOut)
        SOS_.addSOS2()
        # the ratio constraint of electricity and steam
        print_4s('for i in range(t_num):')
        print_8s('prob += ' + self.nameSteamOut + '[i] * ' + str(
            self.elec_vs_steam) + ' - ' + self.nameElecOut + '[i]' + ' == 0')
