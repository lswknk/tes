from core.Base import *


class Storage(Base):
    """
        Define a class of Storage.
    """
    def __init__(self, name):
        super().__init__(name)
        self.input_variables = ['elec']
        self.output_variables = ['elec']
        self.nameChargeFlag = self.name + '_chargeFlag'
        self.nameDischargeFlag = self.name + '_dischargeFlag'
        self.nameSOC = name + '_SOC'
        # storage installation decay
        self.Installation_storage = 1000.0
        self.decay = 0.001
        self.Big_M = 1.0
        self.maxCap = self.Installation_storage * self.Big_M
        self.minCap = 0

        self.initSOC = 0.5
        self.pMaintenance = 10
        self.pLCOE = 0.3
        self.cost_char_and_dischar = 100
        self.charging_efficiency = 1
        self.discharging_efficiency = 1
        self.maxChargingRate = 0.5
        self.maxdisChargingRate = 0.5
        self.minSocPercent = 0.
        self.maxSOC = 2000
        self.minSOC = self.maxCap * self.minSocPercent

    def run(self):
        print_4s('# device: ' + self.name)
        self.declareVariable(varname=self.nameSOC, lowerbound=self.minSOC, upperbound=self.maxSOC)
        self.declareVariable(varname=self.nameElecIn, lowerbound=0, upperbound=self.maxChargingRate * self.maxCap)
        self.declareVariable(varname=self.nameElecOut, lowerbound=0,
                             upperbound=self.maxdisChargingRate * self.maxCap)
        self.declareVariable(varname=self.nameChargeFlag, lowerbound=0, upperbound=1, varType='LpInteger')
        self.declareVariable(varname=self.nameDischargeFlag, lowerbound=0, upperbound=1, varType='LpInteger')
        self.modelConstraints()
        print('')

    def modelConstraints(self):
        # either charging or discharging
        print_4s('# storage ')
        print_4s('for i in range(t_num):')
        print_8s('prob += ' + self.nameChargeFlag + '[i] + ' + str(self.nameDischargeFlag) + '[i] <= 1')
        print_8s('prob += ' + self.nameElecIn + '[i] <= ' + str(self.nameChargeFlag) + '[i] * ' + str(self.maxCap))
        print_8s('prob += ' + self.nameElecOut + '[i] <= ' + str(self.nameDischargeFlag) + '[i] * ' + str(self.maxCap))

        """ max allowable charging/discharging rate constraint """
        # 1. initial SOC[0]　charging/discharging rate constraints
        print_4s('prob += ' + str(self.initSOC) + ' + ' + str(self.charging_efficiency) + '*' +
              self.nameElecIn + '[0] - ' + str(self.discharging_efficiency) + '*' +
              self.nameElecOut + '[0] == ' + self.nameSOC + '[0]')
        # 2. SOC[i]　charging/discharging rate constraints
        print_4s('for i in range(t_num-1):')
        print_8s('prob += ' + self.nameSOC + '[i] + ' + str(
            self.charging_efficiency) + '*' + self.nameElecIn + '[i+1] - ' + str(
            self.discharging_efficiency) + '*' + self.nameElecOut + '[i+1] == ' + str(self.nameSOC) + '[i+1]')
