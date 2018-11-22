from core.Base import *


class User(Base):
    """
    Define a class of Users. A user consumes cool, heat or electricity.
    The class uses three variables: nameEE (electricity), nameHESteam (hot steam), nameCE (cool).
    The other two variables are slack variables.
    """

    def __init__(self, name):
        super().__init__(name)
        self.name = name
        # self.input_variables = ['hotwater', 'steam', 'elec', 'cool']
        self.input_variables = []
        self.output_variables = []
        self.nameSlack1 = []
        self.nameSlack2 = []
        self.elecSlack1 = 10
        self.elecSlack2 = 10
        self.steamSlack1 = 0.2
        self.steamSlack2 = 0.1
        self.pSteam = [260 for i in range(24)]
        self.pElec = [0.662 for i in range(24)]

    def run(self):
        print_4s('# user: ' + self.name)
        self.declareBasicVars()
        print("")

    def declareBasicVars(self):
        super().declareBasicVars(sublist=self.input_variables)
        super().declareBasicVars(sublist=self.output_variables, in_out='out')
        for item in self.input_variables:
            self.nameSlack1.append(self.name + '_slack1_' + item)
            self.nameSlack2.append(self.name + '_slack2_' + item)
            if self.nameSlack1[-1][-4:] == "team":
                self.declareVariable(varname=self.nameSlack1[-1], upperbound=self.steamSlack1)
                self.declareVariable(varname=self.nameSlack2[-1], upperbound=self.steamSlack2)
            elif self.nameSlack1[-1][-4:] == "elec":
                self.declareVariable(varname=self.nameSlack1[-1], upperbound=self.elecSlack1)
                self.declareVariable(varname=self.nameSlack2[-1], upperbound=self.elecSlack2)

            temp = eval('self.name' + item.capitalize() + 'In')
            nameStr = "loads['" + item + "Loads']['" + self.name + "'][i] + " + self.nameSlack1[-1] + "[i] - " \
                      + self.nameSlack2[-1] + "[i]"
            print_4s("for i in range(t_num):")
            if item == 'elec':
                tempOut = eval('self.name' + item.capitalize() + 'Out')
                print_8s("prob += " + nameStr + " - " + temp + "[i] + " + tempOut + '[i] == 0')
            else:
                print_8s("prob += " + nameStr + " - " + temp + "[i] == 0")
