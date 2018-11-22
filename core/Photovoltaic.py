from core.Base import *
import numpy as np


class Photovoltaic(Base):
    """ Define a class of Photovoltaic """

    def __init__(self, name):
        super().__init__(name)
        self.input_variables = []
        self.output_variables = ['elec']
        self.maxOutputPower = [2000 for i in range(24)]
        self.maxCap = 2000
        self.minCap = 0
        self.pAbandoning = 100.0
        self.pMaintenance = 10
        self.pLCOE = 0.822

    def run(self):
        print_4s('# device: ' + self.name)
        # self.declareVariable(varname=self.nameElecOut, lowerbound=self.minCap, upperbound=self.maxCap)
        self.declareVariable(varname=self.nameElecOut)
        self.modelConstraints()
        print('')

    def modelConstraints(self):
        # maximum and minimum capacity
        print_4s('maxOutputPower = ' + str(self.maxOutputPower))
        print_4s('for i in range(t_num):')
        print_8s('prob += ' + self.nameElecOut + '[i] - ' + 'maxOutputPower[i] <= 0')
