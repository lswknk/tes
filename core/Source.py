from core.Base import *


class Source(Base):
    """
    Define a class of Source. Source provides natural gas, electricity and water.
    The class uses four variables: nameGE (gas), nameEE (electricity), nameWA (water), nameCO2 (CO_2).
    """

    def __init__(self, name):
        super().__init__(name)
        self.input_variables = []
        self.output_variables = []
        temp_sell = []
        temp_purchase = []
        for i in range(24):
            if i <= 8 or 21 < i < 24:
                temp_sell.append(0.4077)
                temp_purchase.append(0.38)
            elif i < 12:
                temp_purchase.append(0.5)
                temp_sell.append(0.6460)
            else:
                temp_purchase.append(0.7)
                temp_sell.append(1.0238)

        # self.pElecSell = [0.49 for i in range(24)]
        self.pElecSell = temp_sell  # source 向泛能站卖电
        self.pPurchase = temp_purchase  # Source 向泛能站买电
        self.pGas = 2.42
        self.pWater = 4.0

    def run(self):
        print_4s('# source: ' + self.name)
        self.declareBasicVars()
        # self.co2_constraint()
        print('')

    def co2_constraint(self):
        print_4s('for i in range(t_num):')
        print_8s('prob += ' + self.nameCo2 + '[i] - 960*' + self.nameElec + '[i] >= 0')

    def declareBasicVars(self):
        # def declareBasicVars(self, in_out='out'):
        for item in self.output_variables:
            temp = eval('self.name' + item.capitalize() + 'Out')
            super().declareVariable(varname=temp)

        for item in self.input_variables:
            temp = eval('self.name' + item.capitalize() + 'In')
            super().declareVariable(varname=temp)
