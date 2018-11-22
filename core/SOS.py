import numpy as np
from core.utils import print_4s, print_8s


class SOS(object):

    def __init__(self, paraList, x, y):
        self.paraList = paraList
        self.x = x
        self.y = y

    def addSOS1(self):
        pass

    def addSOS2(self):
        pointList, nameFlag = self.paraList
        temX, temY = [], []
        for item in pointList:
            if item['y'] <= 0.000001:
                continue
            temX.append(item["x"])
            temY.append(item["y"])

        numPoints = len(temY)
        inputVar = np.array(temX)
        outputVar = np.array(temY)

        print('\n    ######## SOS2 ########')
        print_4s('# 1.add limit to the output variable')
        print_4s('for i in range(t_num):')
        print_8s('prob += ' + self.y + '[i] <= ' + str(max(outputVar)))

        print('\n    # 2-1.introduce non-negative continuous variables x_i, Number = number of endpoints')
        for i in range(1, numPoints + 1):
            print_4s(self.y + '_x' + str(i) + ' = LpVariable.dicts("' + self.y + '_x_' + str(
                i) + '", aList, 0, 1)')

        print('\n    # 2-2.introduce binary variables y_i, Number = number of endpoints - 1')
        for i in range(1, numPoints):
            print_4s(self.y + '_y' + str(i) + ' = LpVariable.dicts("' + self.y + '_y_' + str(
                i) + '", aList, 0, 1, LpInteger)')

        print('\n    # 3. output = x1*output(1) + x2*output(2) + x3*output(3)+.....')
        print_4s('for i in range(t_num):')
        print_8s('prob += ', end='')
        for i in range(1, numPoints + 1):
            print(self.y + '_x' + str(i) + '[i]' + ' * ' + str(outputVar[i - 1]), end='')
            if i != numPoints:
                print(' + ', end='')
            else:
                print('', end='')
        print(' == ' + self.y + '[i]')

        print('\n    # 4.sum of xi is equal to 1.0')
        print_4s('for i in range(t_num):')
        print_8s('prob += ', end='')
        for i in range(1, numPoints + 1):
            print(self.y + '_x' + str(i) + '[i]', end='')
            if i != numPoints:
                print(' + ', end='')
            else:
                print('', end='')
        print(' == ' + nameFlag + '[i]')

        print('\n    ##  5.SOS-2 Constrains ##')
        print_4s('# C1: sum of yi is equal to 1.0')
        print_4s('for i in range(t_num):')
        print_8s('prob += ', end='')
        for i in range(1, numPoints):
            print(self.y + '_y' + str(i) + '[i]', end='')
            if i != numPoints - 1:
                print(' + ', end='')
            else:
                print('', end='')
        print(' == ' + nameFlag + '[i]')

        print('\n    # C2: xi <= y(i-1) + yi')
        print_4s('for i in range(t_num):')
        for i in range(1, numPoints + 1):
            if i == 1:
                print_8s('prob += ' + self.y + '_x' + str(i) + '[i]' + ' - ' + self.y + '_y' + str(
                    i) + '[i]', end='')
                print(' <= 0')
            elif i == numPoints:
                print_8s('prob += ' + self.y + '_x' + str(i) + '[i]' + ' - ' + self.y + '_y' + str(
                    i - 1) + '[i]', end='')
                print(' <= 0')
            else:
                print_8s('prob += ' + self.y + '_x' + str(i) + '[i]' + ' - ' + self.y + '_y' + str(
                    i - 1) + '[i]' + ' - ' + self.y + '_y' + str(i) + '[i]', end='')
                print(' <= 0')

        # C3. Equivalent conversion rate for linear model
        print('\n    # C3: equality for input variable')
        print_4s('for i in range(t_num):')
        print_8s('prob += ', end='')
        for i in range(1, numPoints + 1):
            print(self.y + '_x' + str(i) + '[i]' + ' * ' + str(inputVar[i - 1]), end='')
            if i != numPoints:
                print(' + ', end='')
            else:
                print('', end='')
        print(' == ' + self.x + '[i]')
        print_4s('######## End of SOS2 ########')
        print()
