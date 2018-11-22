from core.User import *
from core.Source import *
from core.Device import *
from core.utils import print_4s


def maxProfit(t_num, s1, u1, devices, loads):
    print_4s('max_profit_0 = LpVariable("max_profit_0")')
    print_4s('prob += ', end='')
    tax_elec = 0
    tax_steam = 0
    income_elec = 1 - tax_elec
    income_steam = 1 - tax_steam

    # earnings
    for item in loads:
        # tempName1 = "val.name" + item.replace('Loads', '').capitalize()
        tempName2 = 'u1[user].p' + item.replace('Loads', '').capitalize()
        if item == 'elecLoads':
            for user, val in loads[item].items():
                pValue = eval(tempName2)
                for i in range(t_num):
                    print(str(val[i]) + '*' + str(pValue[i]) + '*' + str(income_elec), end=' - ')
                    for num in range(len(u1[user].nameSlack1)):
                        if u1[user].nameSlack1[num].split('_')[-1] == item.replace('Loads', ''):
                            print(u1[user].nameSlack1[num] + '[' + str(i) + ']*100 - ' \
                                  + u1[user].nameSlack2[num] + '[' + str(i) + ']*100', end='')
                    print(' + ', end='')
        else:
            for user, val in loads[item].items():
                pValue = eval(tempName2)
                for i in range(t_num):
                    print(str(val[i]) + '*' + str(pValue[i]) + '*' + str(income_steam), end=' - ')
                    for num in range(len(u1[user].nameSlack1)):
                        if u1[user].nameSlack1[num].split('_')[-1] == item.replace('Loads', ''):
                            print(u1[user].nameSlack1[num] + '[' + str(i) + ']*100 - ' \
                                  + u1[user].nameSlack2[num] + '[' + str(i) + ']*100', end='')
                    print(' + ', end='')
    print('0 - ', end='')

    for dev in devices:
        if not isinstance(dev, User) and not isinstance(dev, Source):
            for i in range(t_num):
                print(str(dev.maxCap) + '*' + str(dev.pLCOE) + '*0.041667', end=' - ')
        if isinstance(dev, Device):
            for i in range(t_num):
                print(dev.nameFlag + '[' + str(i) + ']*' + str(dev.pMaintenance), end=' - ')
            for i in range(t_num):
                print(dev.nameUpFlag + '[' + str(i) + ']*' + str(dev.pStartup), end=' - ')
            for i in range(t_num):
                print(dev.nameDnFlag + '[' + str(i) + ']*' + str(dev.pShutDn), end=' - ')

    for source in s1:
        for i in range(t_num):
            print(source.nameGasOut + '[' + str(i) + ']*' + str(source.pGas), end=' - ')
            # print(source.nameWater + '[' + str(i) + ']*' + str(source.pWater), end = ' - ')
            if 'elec' in source.input_variables:
                # source 向泛能站卖电
                print(source.nameElecOut + '[' + str(i) + ']*' + str(source.pElecSell[i]), end=' - ')
                # Source 向泛能站买电
                print(source.nameElecIn + '[' + str(i) + ']*(-1)*' + str(income_elec) + '*' + str(source.pPurchase[i]), end=' - ')
    print('max_profit_0 == 0')

    print(' ')
    # print('OBJ: ')
    print_4s('prob += ', end='')
    # earnings
    for item in loads:
        # tempName1 = "val.name" + item.replace('Loads', '').capitalize()
        tempName2 = 'u1[user].p' + item.replace('Loads', '').capitalize()
        if item == 'elecLoads':
            for user, val in loads[item].items():
                pValue = eval(tempName2)
                for i in range(t_num):
                    print(str(val[i]) + '*' + str(pValue[i]) + '*' + str(income_elec), end=' - ')
                    for num in range(len(u1[user].nameSlack1)):
                        if u1[user].nameSlack1[num].split('_')[-1] == item.replace('Loads', ''):
                            print(u1[user].nameSlack1[num] + '[' + str(i) + ']*100 - ' \
                                  + u1[user].nameSlack2[num] + '[' + str(i) + ']*100', end='')
                    print(' + ', end='')
        else:
            for user, val in loads[item].items():
                pValue = eval(tempName2)
                for i in range(t_num):
                    print(str(val[i]) + '*' + str(pValue[i]) + '*' + str(income_steam), end=' - ')
                    for num in range(len(u1[user].nameSlack1)):
                        if u1[user].nameSlack1[num].split('_')[-1] == item.replace('Loads', ''):
                            print(u1[user].nameSlack1[num] + '[' + str(i) + ']*100 - ' \
                                  + u1[user].nameSlack2[num] + '[' + str(i) + ']*100', end='')
                    print(' + ', end='')
    print('0 - ', end='')

    for dev in devices:
        if not isinstance(dev, User) and not isinstance(dev, Source):
            for i in range(t_num):
                print(str(dev.maxCap) + '*' + str(dev.pLCOE) + '*0.041667', end=' - ')
        if isinstance(dev, Device):
            for i in range(t_num):
                print(dev.nameFlag + '[' + str(i) + ']*' + str(dev.pMaintenance), end=' - ')
            for i in range(t_num):
                print(dev.nameUpFlag + '[' + str(i) + ']*' + str(dev.pStartup), end=' - ')
            for i in range(t_num):
                print(dev.nameDnFlag + '[' + str(i) + ']*' + str(dev.pShutDn), end=' - ')
        if any([dev.name[0:2] == 'pv', dev.name[0:2] == 'wg']):
            for i in range(t_num):
                print(' - ' + dev.nameElecOut + '[' + str(i) + '] * ' + str(dev.pAbandoning), end=' - ')

    for source in s1:
        for i in range(t_num):
            print(source.nameGasOut + '[' + str(i) + ']*' + str(source.pGas), end=' - ')
            # print(source.nameWater + '[' + str(i) + ']*' + str(source.pWater), end = ' - ')
            if 'elec' in source.input_variables:
                # source 向泛能站卖电
                print(source.nameElecOut + '[' + str(i) + ']*' + str(source.pElecSell[i]), end=' - ')
                # Source 向泛能站买电
                print(source.nameElecIn + '[' + str(i) + ']*(-1)*' + str(income_elec) + '*' + str(source.pPurchase[i]), end=' - ')
    print('0')
