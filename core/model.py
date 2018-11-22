# real_path: D:\pycharmspace\ehub111\ehub222\core
from pulp import *
import os
def dispatch(loads, isOffMap, t_num):
    prob = LpProblem("Multi-Energy Model", LpMaximize)
    aList = [i for i in range(t_num)]

    # sources
    # source: s1
    s1_wA_out = LpVariable.dicts("s1_wA_out", aList, 0, None, LpContinuous)
    s1_eE_out = LpVariable.dicts("s1_eE_out", aList, 0, None, LpContinuous)
    s1_gE_out = LpVariable.dicts("s1_gE_out", aList, 0, None, LpContinuous)
    s1_eE_in = LpVariable.dicts("s1_eE_in", aList, 0, None, LpContinuous)

    # devices
    # device: stg01
    stg01_SOC = LpVariable.dicts("stg01_SOC", aList, 0.0, 2000, LpContinuous)
    stg01_eE_in = LpVariable.dicts("stg01_eE_in", aList, 0, 500.0, LpContinuous)
    stg01_eE_out = LpVariable.dicts("stg01_eE_out", aList, 0, 500.0, LpContinuous)
    stg01_chargeFlag = LpVariable.dicts("stg01_chargeFlag", aList, 0, 1, LpInteger)
    stg01_dischargeFlag = LpVariable.dicts("stg01_dischargeFlag", aList, 0, 1, LpInteger)
    # storage 
    for i in range(t_num):
        prob += stg01_chargeFlag[i] + stg01_dischargeFlag[i] <= 1
        prob += stg01_eE_in[i] <= stg01_chargeFlag[i] * 1000.0
        prob += stg01_eE_out[i] <= stg01_dischargeFlag[i] * 1000.0
    prob += 0 + 1*stg01_eE_in[0] - 1*stg01_eE_out[0] == stg01_SOC[0]
    for i in range(t_num-1):
        prob += stg01_SOC[i] + 1*stg01_eE_in[i+1] - 1*stg01_eE_out[i+1] == stg01_SOC[i+1]

    # device: chp01
    chp01_gE_in = LpVariable.dicts("chp01_gE_in", aList, 0, None, LpContinuous)
    chp01_wA_in = LpVariable.dicts("chp01_wA_in", aList, 0, None, LpContinuous)
    chp01_hESt_out = LpVariable.dicts("chp01_hESt_out", aList, 0, None, LpContinuous)
    chp01_eE_out = LpVariable.dicts("chp01_eE_out", aList, 0, None, LpContinuous)
    chp01_flag = LpVariable.dicts("chp01_flag", aList, 0, 1, LpInteger)
    chp01_sUpflag = LpVariable.dicts("chp01_sUpflag", aList, 0, 1, LpInteger)
    chp01_sDnflag = LpVariable.dicts("chp01_sDnflag", aList, 0, 1, LpInteger)
    chp01_initState = int(isOffMap['chp01'])
    prob += chp01_flag[0] - chp01_initState - chp01_sUpflag[0] + chp01_sDnflag[0] == 0
    for i in range(t_num - 1):
        prob += chp01_flag[i + 1] - chp01_flag[i] - chp01_sUpflag[i + 1] + chp01_sDnflag[i+1] == 0
        prob += chp01_sDnflag[i] + chp01_sUpflag[i] <= 1
    prob += chp01_sDnflag[t_num - 1] + chp01_sUpflag[t_num - 1] <= 1

    ######## SOS2 ########
    # 1.add limit to the output variable
    for i in range(t_num):
        prob += chp01_eE_out[i] <= 4015.460475

    # 2-1.introduce non-negative continuous variables x_i, Number = number of endpoints
    chp01_eE_out_x1 = LpVariable.dicts("chp01_eE_out_x_1", aList, 0, 1)
    chp01_eE_out_x2 = LpVariable.dicts("chp01_eE_out_x_2", aList, 0, 1)
    chp01_eE_out_x3 = LpVariable.dicts("chp01_eE_out_x_3", aList, 0, 1)
    chp01_eE_out_x4 = LpVariable.dicts("chp01_eE_out_x_4", aList, 0, 1)
    chp01_eE_out_x5 = LpVariable.dicts("chp01_eE_out_x_5", aList, 0, 1)
    chp01_eE_out_x6 = LpVariable.dicts("chp01_eE_out_x_6", aList, 0, 1)
    chp01_eE_out_x7 = LpVariable.dicts("chp01_eE_out_x_7", aList, 0, 1)
    chp01_eE_out_x8 = LpVariable.dicts("chp01_eE_out_x_8", aList, 0, 1)
    chp01_eE_out_x9 = LpVariable.dicts("chp01_eE_out_x_9", aList, 0, 1)
    chp01_eE_out_x10 = LpVariable.dicts("chp01_eE_out_x_10", aList, 0, 1)

    # 2-2.introduce binary variables y_i, Number = number of endpoints - 1
    chp01_eE_out_y1 = LpVariable.dicts("chp01_eE_out_y_1", aList, 0, 1, LpInteger)
    chp01_eE_out_y2 = LpVariable.dicts("chp01_eE_out_y_2", aList, 0, 1, LpInteger)
    chp01_eE_out_y3 = LpVariable.dicts("chp01_eE_out_y_3", aList, 0, 1, LpInteger)
    chp01_eE_out_y4 = LpVariable.dicts("chp01_eE_out_y_4", aList, 0, 1, LpInteger)
    chp01_eE_out_y5 = LpVariable.dicts("chp01_eE_out_y_5", aList, 0, 1, LpInteger)
    chp01_eE_out_y6 = LpVariable.dicts("chp01_eE_out_y_6", aList, 0, 1, LpInteger)
    chp01_eE_out_y7 = LpVariable.dicts("chp01_eE_out_y_7", aList, 0, 1, LpInteger)
    chp01_eE_out_y8 = LpVariable.dicts("chp01_eE_out_y_8", aList, 0, 1, LpInteger)
    chp01_eE_out_y9 = LpVariable.dicts("chp01_eE_out_y_9", aList, 0, 1, LpInteger)

    # 3. output = x1*output(1) + x2*output(2) + x3*output(3)+.....
    for i in range(t_num):
        prob += chp01_eE_out_x1[i] * 1836.915819 + chp01_eE_out_x2[i] * 2252.918131 + chp01_eE_out_x3[i] * 2504.618355 + chp01_eE_out_x4[i] * 2634.596652 + chp01_eE_out_x5[i] * 2929.227812 + chp01_eE_out_x6[i] * 3146.116096 + chp01_eE_out_x7[i] * 3344.345436 + chp01_eE_out_x8[i] * 3544.128508 + chp01_eE_out_x9[i] * 3782.25761 + chp01_eE_out_x10[i] * 4015.460475 == chp01_eE_out[i]

    # 4.sum of xi is equal to 1.0
    for i in range(t_num):
        prob += chp01_eE_out_x1[i] + chp01_eE_out_x2[i] + chp01_eE_out_x3[i] + chp01_eE_out_x4[i] + chp01_eE_out_x5[i] + chp01_eE_out_x6[i] + chp01_eE_out_x7[i] + chp01_eE_out_x8[i] + chp01_eE_out_x9[i] + chp01_eE_out_x10[i] == chp01_flag[i]

    ##  5.SOS-2 Constrains ##
    # C1: sum of yi is equal to 1.0
    for i in range(t_num):
        prob += chp01_eE_out_y1[i] + chp01_eE_out_y2[i] + chp01_eE_out_y3[i] + chp01_eE_out_y4[i] + chp01_eE_out_y5[i] + chp01_eE_out_y6[i] + chp01_eE_out_y7[i] + chp01_eE_out_y8[i] + chp01_eE_out_y9[i] == chp01_flag[i]

    # C2: xi <= y(i-1) + yi
    for i in range(t_num):
        prob += chp01_eE_out_x1[i] - chp01_eE_out_y1[i] <= 0
        prob += chp01_eE_out_x2[i] - chp01_eE_out_y1[i] - chp01_eE_out_y2[i] <= 0
        prob += chp01_eE_out_x3[i] - chp01_eE_out_y2[i] - chp01_eE_out_y3[i] <= 0
        prob += chp01_eE_out_x4[i] - chp01_eE_out_y3[i] - chp01_eE_out_y4[i] <= 0
        prob += chp01_eE_out_x5[i] - chp01_eE_out_y4[i] - chp01_eE_out_y5[i] <= 0
        prob += chp01_eE_out_x6[i] - chp01_eE_out_y5[i] - chp01_eE_out_y6[i] <= 0
        prob += chp01_eE_out_x7[i] - chp01_eE_out_y6[i] - chp01_eE_out_y7[i] <= 0
        prob += chp01_eE_out_x8[i] - chp01_eE_out_y7[i] - chp01_eE_out_y8[i] <= 0
        prob += chp01_eE_out_x9[i] - chp01_eE_out_y8[i] - chp01_eE_out_y9[i] <= 0
        prob += chp01_eE_out_x10[i] - chp01_eE_out_y9[i] <= 0

    # C3: equality for input variable
    for i in range(t_num):
        prob += chp01_eE_out_x1[i] * 518.6894996 + chp01_eE_out_x2[i] * 614.480147 + chp01_eE_out_x3[i] * 689.0343857 + chp01_eE_out_x4[i] * 717.9003396 + chp01_eE_out_x5[i] * 782.262432 + chp01_eE_out_x6[i] * 829.0399983 + chp01_eE_out_x7[i] * 871.8672414 + chp01_eE_out_x8[i] * 916.0146866 + chp01_eE_out_x9[i] * 974.7874015 + chp01_eE_out_x10[i] * 1031.210707 == chp01_gE_in[i]
    ######## End of SOS2 ########

    for i in range(t_num):
        prob += chp01_hESt_out[i] * 1450 - chp01_eE_out[i] == 0

    # device: chp02
    chp02_gE_in = LpVariable.dicts("chp02_gE_in", aList, 0, None, LpContinuous)
    chp02_wA_in = LpVariable.dicts("chp02_wA_in", aList, 0, None, LpContinuous)
    chp02_hESt_out = LpVariable.dicts("chp02_hESt_out", aList, 0, None, LpContinuous)
    chp02_eE_out = LpVariable.dicts("chp02_eE_out", aList, 0, None, LpContinuous)
    chp02_flag = LpVariable.dicts("chp02_flag", aList, 0, 1, LpInteger)
    chp02_sUpflag = LpVariable.dicts("chp02_sUpflag", aList, 0, 1, LpInteger)
    chp02_sDnflag = LpVariable.dicts("chp02_sDnflag", aList, 0, 1, LpInteger)
    chp02_initState = int(isOffMap['chp02'])
    prob += chp02_flag[0] - chp02_initState - chp02_sUpflag[0] + chp02_sDnflag[0] == 0
    for i in range(t_num - 1):
        prob += chp02_flag[i + 1] - chp02_flag[i] - chp02_sUpflag[i + 1] + chp02_sDnflag[i+1] == 0
        prob += chp02_sDnflag[i] + chp02_sUpflag[i] <= 1
    prob += chp02_sDnflag[t_num - 1] + chp02_sUpflag[t_num - 1] <= 1

    ######## SOS2 ########
    # 1.add limit to the output variable
    for i in range(t_num):
        prob += chp02_eE_out[i] <= 1801.8

    # 2-1.introduce non-negative continuous variables x_i, Number = number of endpoints
    chp02_eE_out_x1 = LpVariable.dicts("chp02_eE_out_x_1", aList, 0, 1)
    chp02_eE_out_x2 = LpVariable.dicts("chp02_eE_out_x_2", aList, 0, 1)
    chp02_eE_out_x3 = LpVariable.dicts("chp02_eE_out_x_3", aList, 0, 1)
    chp02_eE_out_x4 = LpVariable.dicts("chp02_eE_out_x_4", aList, 0, 1)
    chp02_eE_out_x5 = LpVariable.dicts("chp02_eE_out_x_5", aList, 0, 1)
    chp02_eE_out_x6 = LpVariable.dicts("chp02_eE_out_x_6", aList, 0, 1)
    chp02_eE_out_x7 = LpVariable.dicts("chp02_eE_out_x_7", aList, 0, 1)
    chp02_eE_out_x8 = LpVariable.dicts("chp02_eE_out_x_8", aList, 0, 1)
    chp02_eE_out_x9 = LpVariable.dicts("chp02_eE_out_x_9", aList, 0, 1)
    chp02_eE_out_x10 = LpVariable.dicts("chp02_eE_out_x_10", aList, 0, 1)

    # 2-2.introduce binary variables y_i, Number = number of endpoints - 1
    chp02_eE_out_y1 = LpVariable.dicts("chp02_eE_out_y_1", aList, 0, 1, LpInteger)
    chp02_eE_out_y2 = LpVariable.dicts("chp02_eE_out_y_2", aList, 0, 1, LpInteger)
    chp02_eE_out_y3 = LpVariable.dicts("chp02_eE_out_y_3", aList, 0, 1, LpInteger)
    chp02_eE_out_y4 = LpVariable.dicts("chp02_eE_out_y_4", aList, 0, 1, LpInteger)
    chp02_eE_out_y5 = LpVariable.dicts("chp02_eE_out_y_5", aList, 0, 1, LpInteger)
    chp02_eE_out_y6 = LpVariable.dicts("chp02_eE_out_y_6", aList, 0, 1, LpInteger)
    chp02_eE_out_y7 = LpVariable.dicts("chp02_eE_out_y_7", aList, 0, 1, LpInteger)
    chp02_eE_out_y8 = LpVariable.dicts("chp02_eE_out_y_8", aList, 0, 1, LpInteger)
    chp02_eE_out_y9 = LpVariable.dicts("chp02_eE_out_y_9", aList, 0, 1, LpInteger)

    # 3. output = x1*output(1) + x2*output(2) + x3*output(3)+.....
    for i in range(t_num):
        prob += chp02_eE_out_x1[i] * 956.6 + chp02_eE_out_x2[i] * 1005.0 + chp02_eE_out_x3[i] * 1113.4 + chp02_eE_out_x4[i] * 1269.2 + chp02_eE_out_x5[i] * 1321.8 + chp02_eE_out_x6[i] * 1420.0 + chp02_eE_out_x7[i] * 1523.6 + chp02_eE_out_x8[i] * 1638.6 + chp02_eE_out_x9[i] * 1753.2 + chp02_eE_out_x10[i] * 1801.8 == chp02_eE_out[i]

    # 4.sum of xi is equal to 1.0
    for i in range(t_num):
        prob += chp02_eE_out_x1[i] + chp02_eE_out_x2[i] + chp02_eE_out_x3[i] + chp02_eE_out_x4[i] + chp02_eE_out_x5[i] + chp02_eE_out_x6[i] + chp02_eE_out_x7[i] + chp02_eE_out_x8[i] + chp02_eE_out_x9[i] + chp02_eE_out_x10[i] == chp02_flag[i]

    ##  5.SOS-2 Constrains ##
    # C1: sum of yi is equal to 1.0
    for i in range(t_num):
        prob += chp02_eE_out_y1[i] + chp02_eE_out_y2[i] + chp02_eE_out_y3[i] + chp02_eE_out_y4[i] + chp02_eE_out_y5[i] + chp02_eE_out_y6[i] + chp02_eE_out_y7[i] + chp02_eE_out_y8[i] + chp02_eE_out_y9[i] == chp02_flag[i]

    # C2: xi <= y(i-1) + yi
    for i in range(t_num):
        prob += chp02_eE_out_x1[i] - chp02_eE_out_y1[i] <= 0
        prob += chp02_eE_out_x2[i] - chp02_eE_out_y1[i] - chp02_eE_out_y2[i] <= 0
        prob += chp02_eE_out_x3[i] - chp02_eE_out_y2[i] - chp02_eE_out_y3[i] <= 0
        prob += chp02_eE_out_x4[i] - chp02_eE_out_y3[i] - chp02_eE_out_y4[i] <= 0
        prob += chp02_eE_out_x5[i] - chp02_eE_out_y4[i] - chp02_eE_out_y5[i] <= 0
        prob += chp02_eE_out_x6[i] - chp02_eE_out_y5[i] - chp02_eE_out_y6[i] <= 0
        prob += chp02_eE_out_x7[i] - chp02_eE_out_y6[i] - chp02_eE_out_y7[i] <= 0
        prob += chp02_eE_out_x8[i] - chp02_eE_out_y7[i] - chp02_eE_out_y8[i] <= 0
        prob += chp02_eE_out_x9[i] - chp02_eE_out_y8[i] - chp02_eE_out_y9[i] <= 0
        prob += chp02_eE_out_x10[i] - chp02_eE_out_y9[i] <= 0

    # C3: equality for input variable
    for i in range(t_num):
        prob += chp02_eE_out_x1[i] * 273.3142857 + chp02_eE_out_x2[i] * 287.965616 + chp02_eE_out_x3[i] * 313.6338028 + chp02_eE_out_x4[i] * 350.6077348 + chp02_eE_out_x5[i] * 363.1318681 + chp02_eE_out_x6[i] * 385.8695652 + chp02_eE_out_x7[i] * 411.7837838 + chp02_eE_out_x8[i] * 439.3029491 + chp02_eE_out_x9[i] * 467.52 + chp02_eE_out_x10[i] * 477.9310345 == chp02_gE_in[i]
    ######## End of SOS2 ########

    for i in range(t_num):
        prob += chp02_hESt_out[i] * 1850.48 - chp02_eE_out[i] == 0

    # device: pv01
    pv01_eE_out = LpVariable.dicts("pv01_eE_out", aList, 0, None, LpContinuous)
    maxOutputPower = [0.0, 0.0, 0.0, 0.0, 143.547, 695.85900000000004, 1038.6500000000001, 1718.3, 2216.8800000000001, 2661.77, 3748.71, 4154.7799999999997, 3719.6900000000001, 3118.8200000000002, 2172.23, 1098.5999999999999, 312.20299999999997, 25.670000000000002, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    for i in range(t_num):
        prob += pv01_eE_out[i] - maxOutputPower[i] <= 0

    # device: gsb02
    gsb02_gE_in = LpVariable.dicts("gsb02_gE_in", aList, 0, None, LpContinuous)
    gsb02_wA_in = LpVariable.dicts("gsb02_wA_in", aList, 0, None, LpContinuous)
    gsb02_hESt_out = LpVariable.dicts("gsb02_hESt_out", aList, 0, None, LpContinuous)
    gsb02_flag = LpVariable.dicts("gsb02_flag", aList, 0, 1, LpInteger)
    gsb02_sUpflag = LpVariable.dicts("gsb02_sUpflag", aList, 0, 1, LpInteger)
    gsb02_sDnflag = LpVariable.dicts("gsb02_sDnflag", aList, 0, 1, LpInteger)
    gsb02_initState = int(isOffMap['gsb02'])
    prob += gsb02_flag[0] - gsb02_initState - gsb02_sUpflag[0] + gsb02_sDnflag[0] == 0
    for i in range(t_num - 1):
        prob += gsb02_flag[i + 1] - gsb02_flag[i] - gsb02_sUpflag[i + 1] + gsb02_sDnflag[i+1] == 0
        prob += gsb02_sDnflag[i] + gsb02_sUpflag[i] <= 1
    prob += gsb02_sDnflag[t_num - 1] + gsb02_sUpflag[t_num - 1] <= 1

    ######## SOS2 ########
    # 1.add limit to the output variable
    for i in range(t_num):
        prob += gsb02_hESt_out[i] <= 8.0

    # 2-1.introduce non-negative continuous variables x_i, Number = number of endpoints
    gsb02_hESt_out_x1 = LpVariable.dicts("gsb02_hESt_out_x_1", aList, 0, 1)
    gsb02_hESt_out_x2 = LpVariable.dicts("gsb02_hESt_out_x_2", aList, 0, 1)
    gsb02_hESt_out_x3 = LpVariable.dicts("gsb02_hESt_out_x_3", aList, 0, 1)
    gsb02_hESt_out_x4 = LpVariable.dicts("gsb02_hESt_out_x_4", aList, 0, 1)
    gsb02_hESt_out_x5 = LpVariable.dicts("gsb02_hESt_out_x_5", aList, 0, 1)
    gsb02_hESt_out_x6 = LpVariable.dicts("gsb02_hESt_out_x_6", aList, 0, 1)
    gsb02_hESt_out_x7 = LpVariable.dicts("gsb02_hESt_out_x_7", aList, 0, 1)
    gsb02_hESt_out_x8 = LpVariable.dicts("gsb02_hESt_out_x_8", aList, 0, 1)
    gsb02_hESt_out_x9 = LpVariable.dicts("gsb02_hESt_out_x_9", aList, 0, 1)
    gsb02_hESt_out_x10 = LpVariable.dicts("gsb02_hESt_out_x_10", aList, 0, 1)
    gsb02_hESt_out_x11 = LpVariable.dicts("gsb02_hESt_out_x_11", aList, 0, 1)

    # 2-2.introduce binary variables y_i, Number = number of endpoints - 1
    gsb02_hESt_out_y1 = LpVariable.dicts("gsb02_hESt_out_y_1", aList, 0, 1, LpInteger)
    gsb02_hESt_out_y2 = LpVariable.dicts("gsb02_hESt_out_y_2", aList, 0, 1, LpInteger)
    gsb02_hESt_out_y3 = LpVariable.dicts("gsb02_hESt_out_y_3", aList, 0, 1, LpInteger)
    gsb02_hESt_out_y4 = LpVariable.dicts("gsb02_hESt_out_y_4", aList, 0, 1, LpInteger)
    gsb02_hESt_out_y5 = LpVariable.dicts("gsb02_hESt_out_y_5", aList, 0, 1, LpInteger)
    gsb02_hESt_out_y6 = LpVariable.dicts("gsb02_hESt_out_y_6", aList, 0, 1, LpInteger)
    gsb02_hESt_out_y7 = LpVariable.dicts("gsb02_hESt_out_y_7", aList, 0, 1, LpInteger)
    gsb02_hESt_out_y8 = LpVariable.dicts("gsb02_hESt_out_y_8", aList, 0, 1, LpInteger)
    gsb02_hESt_out_y9 = LpVariable.dicts("gsb02_hESt_out_y_9", aList, 0, 1, LpInteger)
    gsb02_hESt_out_y10 = LpVariable.dicts("gsb02_hESt_out_y_10", aList, 0, 1, LpInteger)

    # 3. output = x1*output(1) + x2*output(2) + x3*output(3)+.....
    for i in range(t_num):
        prob += gsb02_hESt_out_x1[i] * 3.0 + gsb02_hESt_out_x2[i] * 3.5 + gsb02_hESt_out_x3[i] * 4.0 + gsb02_hESt_out_x4[i] * 4.5 + gsb02_hESt_out_x5[i] * 5.0 + gsb02_hESt_out_x6[i] * 5.5 + gsb02_hESt_out_x7[i] * 6.0 + gsb02_hESt_out_x8[i] * 6.5 + gsb02_hESt_out_x9[i] * 7.0 + gsb02_hESt_out_x10[i] * 7.5 + gsb02_hESt_out_x11[i] * 8.0 == gsb02_hESt_out[i]

    # 4.sum of xi is equal to 1.0
    for i in range(t_num):
        prob += gsb02_hESt_out_x1[i] + gsb02_hESt_out_x2[i] + gsb02_hESt_out_x3[i] + gsb02_hESt_out_x4[i] + gsb02_hESt_out_x5[i] + gsb02_hESt_out_x6[i] + gsb02_hESt_out_x7[i] + gsb02_hESt_out_x8[i] + gsb02_hESt_out_x9[i] + gsb02_hESt_out_x10[i] + gsb02_hESt_out_x11[i] == gsb02_flag[i]

    ##  5.SOS-2 Constrains ##
    # C1: sum of yi is equal to 1.0
    for i in range(t_num):
        prob += gsb02_hESt_out_y1[i] + gsb02_hESt_out_y2[i] + gsb02_hESt_out_y3[i] + gsb02_hESt_out_y4[i] + gsb02_hESt_out_y5[i] + gsb02_hESt_out_y6[i] + gsb02_hESt_out_y7[i] + gsb02_hESt_out_y8[i] + gsb02_hESt_out_y9[i] + gsb02_hESt_out_y10[i] == gsb02_flag[i]

    # C2: xi <= y(i-1) + yi
    for i in range(t_num):
        prob += gsb02_hESt_out_x1[i] - gsb02_hESt_out_y1[i] <= 0
        prob += gsb02_hESt_out_x2[i] - gsb02_hESt_out_y1[i] - gsb02_hESt_out_y2[i] <= 0
        prob += gsb02_hESt_out_x3[i] - gsb02_hESt_out_y2[i] - gsb02_hESt_out_y3[i] <= 0
        prob += gsb02_hESt_out_x4[i] - gsb02_hESt_out_y3[i] - gsb02_hESt_out_y4[i] <= 0
        prob += gsb02_hESt_out_x5[i] - gsb02_hESt_out_y4[i] - gsb02_hESt_out_y5[i] <= 0
        prob += gsb02_hESt_out_x6[i] - gsb02_hESt_out_y5[i] - gsb02_hESt_out_y6[i] <= 0
        prob += gsb02_hESt_out_x7[i] - gsb02_hESt_out_y6[i] - gsb02_hESt_out_y7[i] <= 0
        prob += gsb02_hESt_out_x8[i] - gsb02_hESt_out_y7[i] - gsb02_hESt_out_y8[i] <= 0
        prob += gsb02_hESt_out_x9[i] - gsb02_hESt_out_y8[i] - gsb02_hESt_out_y9[i] <= 0
        prob += gsb02_hESt_out_x10[i] - gsb02_hESt_out_y9[i] - gsb02_hESt_out_y10[i] <= 0
        prob += gsb02_hESt_out_x11[i] - gsb02_hESt_out_y10[i] <= 0

    # C3: equality for input variable
    for i in range(t_num):
        prob += gsb02_hESt_out_x1[i] * 252.1008403 + gsb02_hESt_out_x2[i] * 292.8870293 + gsb02_hESt_out_x3[i] * 333.3333333 + gsb02_hESt_out_x4[i] * 373.4439834 + gsb02_hESt_out_x5[i] * 413.2231405 + gsb02_hESt_out_x6[i] * 452.6748971 + gsb02_hESt_out_x7[i] * 491.8032787 + gsb02_hESt_out_x8[i] * 530.6122449 + gsb02_hESt_out_x9[i] * 569.1056911 + gsb02_hESt_out_x10[i] * 607.2874494 + gsb02_hESt_out_x11[i] * 645.1612903 == gsb02_gE_in[i]
    ######## End of SOS2 ########

    for i in range(t_num):
        prob += gsb02_hESt_out[i] - gsb02_flag[i] * 10 <= 0
        prob += gsb02_hESt_out[i] - gsb02_flag[i] * 1.9 >= 0

    # device: gsb01
    gsb01_gE_in = LpVariable.dicts("gsb01_gE_in", aList, 0, None, LpContinuous)
    gsb01_wA_in = LpVariable.dicts("gsb01_wA_in", aList, 0, None, LpContinuous)
    gsb01_hESt_out = LpVariable.dicts("gsb01_hESt_out", aList, 0, None, LpContinuous)
    gsb01_flag = LpVariable.dicts("gsb01_flag", aList, 0, 1, LpInteger)
    gsb01_sUpflag = LpVariable.dicts("gsb01_sUpflag", aList, 0, 1, LpInteger)
    gsb01_sDnflag = LpVariable.dicts("gsb01_sDnflag", aList, 0, 1, LpInteger)
    gsb01_initState = int(isOffMap['gsb01'])
    prob += gsb01_flag[0] - gsb01_initState - gsb01_sUpflag[0] + gsb01_sDnflag[0] == 0
    for i in range(t_num - 1):
        prob += gsb01_flag[i + 1] - gsb01_flag[i] - gsb01_sUpflag[i + 1] + gsb01_sDnflag[i+1] == 0
        prob += gsb01_sDnflag[i] + gsb01_sUpflag[i] <= 1
    prob += gsb01_sDnflag[t_num - 1] + gsb01_sUpflag[t_num - 1] <= 1

    ######## SOS2 ########
    # 1.add limit to the output variable
    for i in range(t_num):
        prob += gsb01_hESt_out[i] <= 8.0

    # 2-1.introduce non-negative continuous variables x_i, Number = number of endpoints
    gsb01_hESt_out_x1 = LpVariable.dicts("gsb01_hESt_out_x_1", aList, 0, 1)
    gsb01_hESt_out_x2 = LpVariable.dicts("gsb01_hESt_out_x_2", aList, 0, 1)
    gsb01_hESt_out_x3 = LpVariable.dicts("gsb01_hESt_out_x_3", aList, 0, 1)
    gsb01_hESt_out_x4 = LpVariable.dicts("gsb01_hESt_out_x_4", aList, 0, 1)
    gsb01_hESt_out_x5 = LpVariable.dicts("gsb01_hESt_out_x_5", aList, 0, 1)
    gsb01_hESt_out_x6 = LpVariable.dicts("gsb01_hESt_out_x_6", aList, 0, 1)
    gsb01_hESt_out_x7 = LpVariable.dicts("gsb01_hESt_out_x_7", aList, 0, 1)
    gsb01_hESt_out_x8 = LpVariable.dicts("gsb01_hESt_out_x_8", aList, 0, 1)
    gsb01_hESt_out_x9 = LpVariable.dicts("gsb01_hESt_out_x_9", aList, 0, 1)
    gsb01_hESt_out_x10 = LpVariable.dicts("gsb01_hESt_out_x_10", aList, 0, 1)
    gsb01_hESt_out_x11 = LpVariable.dicts("gsb01_hESt_out_x_11", aList, 0, 1)

    # 2-2.introduce binary variables y_i, Number = number of endpoints - 1
    gsb01_hESt_out_y1 = LpVariable.dicts("gsb01_hESt_out_y_1", aList, 0, 1, LpInteger)
    gsb01_hESt_out_y2 = LpVariable.dicts("gsb01_hESt_out_y_2", aList, 0, 1, LpInteger)
    gsb01_hESt_out_y3 = LpVariable.dicts("gsb01_hESt_out_y_3", aList, 0, 1, LpInteger)
    gsb01_hESt_out_y4 = LpVariable.dicts("gsb01_hESt_out_y_4", aList, 0, 1, LpInteger)
    gsb01_hESt_out_y5 = LpVariable.dicts("gsb01_hESt_out_y_5", aList, 0, 1, LpInteger)
    gsb01_hESt_out_y6 = LpVariable.dicts("gsb01_hESt_out_y_6", aList, 0, 1, LpInteger)
    gsb01_hESt_out_y7 = LpVariable.dicts("gsb01_hESt_out_y_7", aList, 0, 1, LpInteger)
    gsb01_hESt_out_y8 = LpVariable.dicts("gsb01_hESt_out_y_8", aList, 0, 1, LpInteger)
    gsb01_hESt_out_y9 = LpVariable.dicts("gsb01_hESt_out_y_9", aList, 0, 1, LpInteger)
    gsb01_hESt_out_y10 = LpVariable.dicts("gsb01_hESt_out_y_10", aList, 0, 1, LpInteger)

    # 3. output = x1*output(1) + x2*output(2) + x3*output(3)+.....
    for i in range(t_num):
        prob += gsb01_hESt_out_x1[i] * 3.0 + gsb01_hESt_out_x2[i] * 3.5 + gsb01_hESt_out_x3[i] * 4.0 + gsb01_hESt_out_x4[i] * 4.5 + gsb01_hESt_out_x5[i] * 5.0 + gsb01_hESt_out_x6[i] * 5.5 + gsb01_hESt_out_x7[i] * 6.0 + gsb01_hESt_out_x8[i] * 6.5 + gsb01_hESt_out_x9[i] * 7.0 + gsb01_hESt_out_x10[i] * 7.5 + gsb01_hESt_out_x11[i] * 8.0 == gsb01_hESt_out[i]

    # 4.sum of xi is equal to 1.0
    for i in range(t_num):
        prob += gsb01_hESt_out_x1[i] + gsb01_hESt_out_x2[i] + gsb01_hESt_out_x3[i] + gsb01_hESt_out_x4[i] + gsb01_hESt_out_x5[i] + gsb01_hESt_out_x6[i] + gsb01_hESt_out_x7[i] + gsb01_hESt_out_x8[i] + gsb01_hESt_out_x9[i] + gsb01_hESt_out_x10[i] + gsb01_hESt_out_x11[i] == gsb01_flag[i]

    ##  5.SOS-2 Constrains ##
    # C1: sum of yi is equal to 1.0
    for i in range(t_num):
        prob += gsb01_hESt_out_y1[i] + gsb01_hESt_out_y2[i] + gsb01_hESt_out_y3[i] + gsb01_hESt_out_y4[i] + gsb01_hESt_out_y5[i] + gsb01_hESt_out_y6[i] + gsb01_hESt_out_y7[i] + gsb01_hESt_out_y8[i] + gsb01_hESt_out_y9[i] + gsb01_hESt_out_y10[i] == gsb01_flag[i]

    # C2: xi <= y(i-1) + yi
    for i in range(t_num):
        prob += gsb01_hESt_out_x1[i] - gsb01_hESt_out_y1[i] <= 0
        prob += gsb01_hESt_out_x2[i] - gsb01_hESt_out_y1[i] - gsb01_hESt_out_y2[i] <= 0
        prob += gsb01_hESt_out_x3[i] - gsb01_hESt_out_y2[i] - gsb01_hESt_out_y3[i] <= 0
        prob += gsb01_hESt_out_x4[i] - gsb01_hESt_out_y3[i] - gsb01_hESt_out_y4[i] <= 0
        prob += gsb01_hESt_out_x5[i] - gsb01_hESt_out_y4[i] - gsb01_hESt_out_y5[i] <= 0
        prob += gsb01_hESt_out_x6[i] - gsb01_hESt_out_y5[i] - gsb01_hESt_out_y6[i] <= 0
        prob += gsb01_hESt_out_x7[i] - gsb01_hESt_out_y6[i] - gsb01_hESt_out_y7[i] <= 0
        prob += gsb01_hESt_out_x8[i] - gsb01_hESt_out_y7[i] - gsb01_hESt_out_y8[i] <= 0
        prob += gsb01_hESt_out_x9[i] - gsb01_hESt_out_y8[i] - gsb01_hESt_out_y9[i] <= 0
        prob += gsb01_hESt_out_x10[i] - gsb01_hESt_out_y9[i] - gsb01_hESt_out_y10[i] <= 0
        prob += gsb01_hESt_out_x11[i] - gsb01_hESt_out_y10[i] <= 0

    # C3: equality for input variable
    for i in range(t_num):
        prob += gsb01_hESt_out_x1[i] * 252.1008403 + gsb01_hESt_out_x2[i] * 292.8870293 + gsb01_hESt_out_x3[i] * 333.3333333 + gsb01_hESt_out_x4[i] * 373.4439834 + gsb01_hESt_out_x5[i] * 413.2231405 + gsb01_hESt_out_x6[i] * 452.6748971 + gsb01_hESt_out_x7[i] * 491.8032787 + gsb01_hESt_out_x8[i] * 530.6122449 + gsb01_hESt_out_x9[i] * 569.1056911 + gsb01_hESt_out_x10[i] * 607.2874494 + gsb01_hESt_out_x11[i] * 645.1612903 == gsb01_gE_in[i]
    ######## End of SOS2 ########

    for i in range(t_num):
        prob += gsb01_hESt_out[i] - gsb01_flag[i] * 10 <= 0
        prob += gsb01_hESt_out[i] - gsb01_flag[i] * 1.9 >= 0

    # device: gsb03
    gsb03_gE_in = LpVariable.dicts("gsb03_gE_in", aList, 0, None, LpContinuous)
    gsb03_wA_in = LpVariable.dicts("gsb03_wA_in", aList, 0, None, LpContinuous)
    gsb03_hESt_out = LpVariable.dicts("gsb03_hESt_out", aList, 0, None, LpContinuous)
    gsb03_flag = LpVariable.dicts("gsb03_flag", aList, 0, 1, LpInteger)
    gsb03_sUpflag = LpVariable.dicts("gsb03_sUpflag", aList, 0, 1, LpInteger)
    gsb03_sDnflag = LpVariable.dicts("gsb03_sDnflag", aList, 0, 1, LpInteger)
    gsb03_initState = int(isOffMap['gsb03'])
    prob += gsb03_flag[0] - gsb03_initState - gsb03_sUpflag[0] + gsb03_sDnflag[0] == 0
    for i in range(t_num - 1):
        prob += gsb03_flag[i + 1] - gsb03_flag[i] - gsb03_sUpflag[i + 1] + gsb03_sDnflag[i+1] == 0
        prob += gsb03_sDnflag[i] + gsb03_sUpflag[i] <= 1
    prob += gsb03_sDnflag[t_num - 1] + gsb03_sUpflag[t_num - 1] <= 1

    ######## SOS2 ########
    # 1.add limit to the output variable
    for i in range(t_num):
        prob += gsb03_hESt_out[i] <= 8.0

    # 2-1.introduce non-negative continuous variables x_i, Number = number of endpoints
    gsb03_hESt_out_x1 = LpVariable.dicts("gsb03_hESt_out_x_1", aList, 0, 1)
    gsb03_hESt_out_x2 = LpVariable.dicts("gsb03_hESt_out_x_2", aList, 0, 1)
    gsb03_hESt_out_x3 = LpVariable.dicts("gsb03_hESt_out_x_3", aList, 0, 1)
    gsb03_hESt_out_x4 = LpVariable.dicts("gsb03_hESt_out_x_4", aList, 0, 1)
    gsb03_hESt_out_x5 = LpVariable.dicts("gsb03_hESt_out_x_5", aList, 0, 1)
    gsb03_hESt_out_x6 = LpVariable.dicts("gsb03_hESt_out_x_6", aList, 0, 1)
    gsb03_hESt_out_x7 = LpVariable.dicts("gsb03_hESt_out_x_7", aList, 0, 1)
    gsb03_hESt_out_x8 = LpVariable.dicts("gsb03_hESt_out_x_8", aList, 0, 1)
    gsb03_hESt_out_x9 = LpVariable.dicts("gsb03_hESt_out_x_9", aList, 0, 1)
    gsb03_hESt_out_x10 = LpVariable.dicts("gsb03_hESt_out_x_10", aList, 0, 1)
    gsb03_hESt_out_x11 = LpVariable.dicts("gsb03_hESt_out_x_11", aList, 0, 1)

    # 2-2.introduce binary variables y_i, Number = number of endpoints - 1
    gsb03_hESt_out_y1 = LpVariable.dicts("gsb03_hESt_out_y_1", aList, 0, 1, LpInteger)
    gsb03_hESt_out_y2 = LpVariable.dicts("gsb03_hESt_out_y_2", aList, 0, 1, LpInteger)
    gsb03_hESt_out_y3 = LpVariable.dicts("gsb03_hESt_out_y_3", aList, 0, 1, LpInteger)
    gsb03_hESt_out_y4 = LpVariable.dicts("gsb03_hESt_out_y_4", aList, 0, 1, LpInteger)
    gsb03_hESt_out_y5 = LpVariable.dicts("gsb03_hESt_out_y_5", aList, 0, 1, LpInteger)
    gsb03_hESt_out_y6 = LpVariable.dicts("gsb03_hESt_out_y_6", aList, 0, 1, LpInteger)
    gsb03_hESt_out_y7 = LpVariable.dicts("gsb03_hESt_out_y_7", aList, 0, 1, LpInteger)
    gsb03_hESt_out_y8 = LpVariable.dicts("gsb03_hESt_out_y_8", aList, 0, 1, LpInteger)
    gsb03_hESt_out_y9 = LpVariable.dicts("gsb03_hESt_out_y_9", aList, 0, 1, LpInteger)
    gsb03_hESt_out_y10 = LpVariable.dicts("gsb03_hESt_out_y_10", aList, 0, 1, LpInteger)

    # 3. output = x1*output(1) + x2*output(2) + x3*output(3)+.....
    for i in range(t_num):
        prob += gsb03_hESt_out_x1[i] * 3.0 + gsb03_hESt_out_x2[i] * 3.5 + gsb03_hESt_out_x3[i] * 4.0 + gsb03_hESt_out_x4[i] * 4.5 + gsb03_hESt_out_x5[i] * 5.0 + gsb03_hESt_out_x6[i] * 5.5 + gsb03_hESt_out_x7[i] * 6.0 + gsb03_hESt_out_x8[i] * 6.5 + gsb03_hESt_out_x9[i] * 7.0 + gsb03_hESt_out_x10[i] * 7.5 + gsb03_hESt_out_x11[i] * 8.0 == gsb03_hESt_out[i]

    # 4.sum of xi is equal to 1.0
    for i in range(t_num):
        prob += gsb03_hESt_out_x1[i] + gsb03_hESt_out_x2[i] + gsb03_hESt_out_x3[i] + gsb03_hESt_out_x4[i] + gsb03_hESt_out_x5[i] + gsb03_hESt_out_x6[i] + gsb03_hESt_out_x7[i] + gsb03_hESt_out_x8[i] + gsb03_hESt_out_x9[i] + gsb03_hESt_out_x10[i] + gsb03_hESt_out_x11[i] == gsb03_flag[i]

    ##  5.SOS-2 Constrains ##
    # C1: sum of yi is equal to 1.0
    for i in range(t_num):
        prob += gsb03_hESt_out_y1[i] + gsb03_hESt_out_y2[i] + gsb03_hESt_out_y3[i] + gsb03_hESt_out_y4[i] + gsb03_hESt_out_y5[i] + gsb03_hESt_out_y6[i] + gsb03_hESt_out_y7[i] + gsb03_hESt_out_y8[i] + gsb03_hESt_out_y9[i] + gsb03_hESt_out_y10[i] == gsb03_flag[i]

    # C2: xi <= y(i-1) + yi
    for i in range(t_num):
        prob += gsb03_hESt_out_x1[i] - gsb03_hESt_out_y1[i] <= 0
        prob += gsb03_hESt_out_x2[i] - gsb03_hESt_out_y1[i] - gsb03_hESt_out_y2[i] <= 0
        prob += gsb03_hESt_out_x3[i] - gsb03_hESt_out_y2[i] - gsb03_hESt_out_y3[i] <= 0
        prob += gsb03_hESt_out_x4[i] - gsb03_hESt_out_y3[i] - gsb03_hESt_out_y4[i] <= 0
        prob += gsb03_hESt_out_x5[i] - gsb03_hESt_out_y4[i] - gsb03_hESt_out_y5[i] <= 0
        prob += gsb03_hESt_out_x6[i] - gsb03_hESt_out_y5[i] - gsb03_hESt_out_y6[i] <= 0
        prob += gsb03_hESt_out_x7[i] - gsb03_hESt_out_y6[i] - gsb03_hESt_out_y7[i] <= 0
        prob += gsb03_hESt_out_x8[i] - gsb03_hESt_out_y7[i] - gsb03_hESt_out_y8[i] <= 0
        prob += gsb03_hESt_out_x9[i] - gsb03_hESt_out_y8[i] - gsb03_hESt_out_y9[i] <= 0
        prob += gsb03_hESt_out_x10[i] - gsb03_hESt_out_y9[i] - gsb03_hESt_out_y10[i] <= 0
        prob += gsb03_hESt_out_x11[i] - gsb03_hESt_out_y10[i] <= 0

    # C3: equality for input variable
    for i in range(t_num):
        prob += gsb03_hESt_out_x1[i] * 252.1008403 + gsb03_hESt_out_x2[i] * 292.8870293 + gsb03_hESt_out_x3[i] * 333.3333333 + gsb03_hESt_out_x4[i] * 373.4439834 + gsb03_hESt_out_x5[i] * 413.2231405 + gsb03_hESt_out_x6[i] * 452.6748971 + gsb03_hESt_out_x7[i] * 491.8032787 + gsb03_hESt_out_x8[i] * 530.6122449 + gsb03_hESt_out_x9[i] * 569.1056911 + gsb03_hESt_out_x10[i] * 607.2874494 + gsb03_hESt_out_x11[i] * 645.1612903 == gsb03_gE_in[i]
    ######## End of SOS2 ########

    for i in range(t_num):
        prob += gsb03_hESt_out[i] - gsb03_flag[i] * 10 <= 0
        prob += gsb03_hESt_out[i] - gsb03_flag[i] * 1.9 >= 0

    # user
    # user: u1
    u1_eE_in = LpVariable.dicts("u1_eE_in", aList, 0, None, LpContinuous)
    u1_hESt_in = LpVariable.dicts("u1_hESt_in", aList, 0, None, LpContinuous)
    u1_eE_out = LpVariable.dicts("u1_eE_out", aList, 0, None, LpContinuous)
    u1_slack1_elec = LpVariable.dicts("u1_slack1_elec", aList, 0, 10, LpContinuous)
    u1_slack2_elec = LpVariable.dicts("u1_slack2_elec", aList, 0, 10, LpContinuous)
    for i in range(t_num):
        prob += loads['elecLoads']['u1'][i] + u1_slack1_elec[i] - u1_slack2_elec[i] - u1_eE_in[i] + u1_eE_out[i] == 0
    u1_slack1_steam = LpVariable.dicts("u1_slack1_steam", aList, 0, 0.2, LpContinuous)
    u1_slack2_steam = LpVariable.dicts("u1_slack2_steam", aList, 0, 0.1, LpContinuous)
    for i in range(t_num):
        prob += loads['steamLoads']['u1'][i] + u1_slack1_steam[i] - u1_slack2_steam[i] - u1_hESt_in[i] == 0

    # forward topology
    stg01_eE_out__u1_eE_in = LpVariable.dicts("stg01_eE_out__u1_eE_in", aList, 0, None)
    for i in range(t_num):
        prob += stg01_eE_out[i] - stg01_eE_out__u1_eE_in[i] == 0
    chp01_eE_out__u1_eE_in = LpVariable.dicts("chp01_eE_out__u1_eE_in", aList, 0, None)
    for i in range(t_num):
        prob += chp01_eE_out[i] - chp01_eE_out__u1_eE_in[i] == 0
    chp02_eE_out__u1_eE_in = LpVariable.dicts("chp02_eE_out__u1_eE_in", aList, 0, None)
    for i in range(t_num):
        prob += chp02_eE_out[i] - chp02_eE_out__u1_eE_in[i] == 0
    pv01_eE_out__stg01_eE_in = LpVariable.dicts("pv01_eE_out__stg01_eE_in", aList, 0, None)
    pv01_eE_out__u1_eE_in = LpVariable.dicts("pv01_eE_out__u1_eE_in", aList, 0, None)
    for i in range(t_num):
        prob += pv01_eE_out[i] - pv01_eE_out__stg01_eE_in[i] - pv01_eE_out__u1_eE_in[i] == 0
    s1_eE_out__u1_eE_in = LpVariable.dicts("s1_eE_out__u1_eE_in", aList, 0, None)
    for i in range(t_num):
        prob += s1_eE_out[i] - s1_eE_out__u1_eE_in[i] == 0
    gsb02_hESt_out__u1_hESt_in = LpVariable.dicts("gsb02_hESt_out__u1_hESt_in", aList, 0, None)
    for i in range(t_num):
        prob += gsb02_hESt_out[i] - gsb02_hESt_out__u1_hESt_in[i] == 0
    gsb01_hESt_out__u1_hESt_in = LpVariable.dicts("gsb01_hESt_out__u1_hESt_in", aList, 0, None)
    for i in range(t_num):
        prob += gsb01_hESt_out[i] - gsb01_hESt_out__u1_hESt_in[i] == 0
    chp01_hESt_out__u1_hESt_in = LpVariable.dicts("chp01_hESt_out__u1_hESt_in", aList, 0, None)
    for i in range(t_num):
        prob += chp01_hESt_out[i] - chp01_hESt_out__u1_hESt_in[i] == 0
    chp02_hESt_out__u1_hESt_in = LpVariable.dicts("chp02_hESt_out__u1_hESt_in", aList, 0, None)
    for i in range(t_num):
        prob += chp02_hESt_out[i] - chp02_hESt_out__u1_hESt_in[i] == 0
    gsb03_hESt_out__u1_hESt_in = LpVariable.dicts("gsb03_hESt_out__u1_hESt_in", aList, 0, None)
    for i in range(t_num):
        prob += gsb03_hESt_out[i] - gsb03_hESt_out__u1_hESt_in[i] == 0
    s1_wA_out__gsb02_wA_in = LpVariable.dicts("s1_wA_out__gsb02_wA_in", aList, 0, None)
    s1_wA_out__gsb01_wA_in = LpVariable.dicts("s1_wA_out__gsb01_wA_in", aList, 0, None)
    s1_wA_out__chp01_wA_in = LpVariable.dicts("s1_wA_out__chp01_wA_in", aList, 0, None)
    s1_wA_out__chp02_wA_in = LpVariable.dicts("s1_wA_out__chp02_wA_in", aList, 0, None)
    s1_wA_out__gsb03_wA_in = LpVariable.dicts("s1_wA_out__gsb03_wA_in", aList, 0, None)
    for i in range(t_num):
        prob += s1_wA_out[i] - s1_wA_out__gsb02_wA_in[i] - s1_wA_out__gsb01_wA_in[i] - s1_wA_out__chp01_wA_in[i] - s1_wA_out__chp02_wA_in[i] - s1_wA_out__gsb03_wA_in[i] == 0
    s1_gE_out__gsb02_gE_in = LpVariable.dicts("s1_gE_out__gsb02_gE_in", aList, 0, None)
    s1_gE_out__gsb01_gE_in = LpVariable.dicts("s1_gE_out__gsb01_gE_in", aList, 0, None)
    s1_gE_out__chp01_gE_in = LpVariable.dicts("s1_gE_out__chp01_gE_in", aList, 0, None)
    s1_gE_out__chp02_gE_in = LpVariable.dicts("s1_gE_out__chp02_gE_in", aList, 0, None)
    s1_gE_out__gsb03_gE_in = LpVariable.dicts("s1_gE_out__gsb03_gE_in", aList, 0, None)
    for i in range(t_num):
        prob += s1_gE_out[i] - s1_gE_out__gsb02_gE_in[i] - s1_gE_out__gsb01_gE_in[i] - s1_gE_out__chp01_gE_in[i] - s1_gE_out__chp02_gE_in[i] - s1_gE_out__gsb03_gE_in[i] == 0
    u1_eE_out__s1_eE_in = LpVariable.dicts("u1_eE_out__s1_eE_in", aList, 0, None)
    for i in range(t_num):
        prob += u1_eE_out[i] - u1_eE_out__s1_eE_in[i] == 0

    # backward topology
    for i in range(t_num):
        prob += u1_eE_in[i] - stg01_eE_out__u1_eE_in[i] - chp01_eE_out__u1_eE_in[i] - chp02_eE_out__u1_eE_in[i] - pv01_eE_out__u1_eE_in[i] - s1_eE_out__u1_eE_in[i] == 0
    for i in range(t_num):
        prob += u1_hESt_in[i] - gsb02_hESt_out__u1_hESt_in[i] - gsb01_hESt_out__u1_hESt_in[i] - chp01_hESt_out__u1_hESt_in[i] - chp02_hESt_out__u1_hESt_in[i] - gsb03_hESt_out__u1_hESt_in[i] == 0
    for i in range(t_num):
        prob += chp01_wA_in[i] - s1_wA_out__chp01_wA_in[i] == 0
    for i in range(t_num):
        prob += gsb01_wA_in[i] - s1_wA_out__gsb01_wA_in[i] == 0
    for i in range(t_num):
        prob += stg01_eE_in[i] - pv01_eE_out__stg01_eE_in[i] == 0
    for i in range(t_num):
        prob += gsb03_gE_in[i] - s1_gE_out__gsb03_gE_in[i] == 0
    for i in range(t_num):
        prob += gsb02_wA_in[i] - s1_wA_out__gsb02_wA_in[i] == 0
    for i in range(t_num):
        prob += chp02_gE_in[i] - s1_gE_out__chp02_gE_in[i] == 0
    for i in range(t_num):
        prob += chp01_gE_in[i] - s1_gE_out__chp01_gE_in[i] == 0
    for i in range(t_num):
        prob += gsb01_gE_in[i] - s1_gE_out__gsb01_gE_in[i] == 0
    for i in range(t_num):
        prob += gsb03_wA_in[i] - s1_wA_out__gsb03_wA_in[i] == 0
    for i in range(t_num):
        prob += gsb02_gE_in[i] - s1_gE_out__gsb02_gE_in[i] == 0
    for i in range(t_num):
        prob += s1_eE_in[i] - u1_eE_out__s1_eE_in[i] == 0
    for i in range(t_num):
        prob += chp02_wA_in[i] - s1_wA_out__chp02_wA_in[i] == 0
    max_profit_0 = LpVariable("max_profit_0")
    prob += 13.16*260*1 - u1_slack1_steam[0]*100 - u1_slack2_steam[0]*100 + 13.69*260*1 - u1_slack1_steam[1]*100 - u1_slack2_steam[1]*100 + 13.49*260*1 - u1_slack1_steam[2]*100 - u1_slack2_steam[2]*100 + 11.51*260*1 - u1_slack1_steam[3]*100 - u1_slack2_steam[3]*100 + 13.34*260*1 - u1_slack1_steam[4]*100 - u1_slack2_steam[4]*100 + 13.43*260*1 - u1_slack1_steam[5]*100 - u1_slack2_steam[5]*100 + 12.77*260*1 - u1_slack1_steam[6]*100 - u1_slack2_steam[6]*100 + 13.78*260*1 - u1_slack1_steam[7]*100 - u1_slack2_steam[7]*100 + 14.12*260*1 - u1_slack1_steam[8]*100 - u1_slack2_steam[8]*100 + 12.55*260*1 - u1_slack1_steam[9]*100 - u1_slack2_steam[9]*100 + 12.36*260*1 - u1_slack1_steam[10]*100 - u1_slack2_steam[10]*100 + 12.28*260*1 - u1_slack1_steam[11]*100 - u1_slack2_steam[11]*100 + 13.08*260*1 - u1_slack1_steam[12]*100 - u1_slack2_steam[12]*100 + 12.41*260*1 - u1_slack1_steam[13]*100 - u1_slack2_steam[13]*100 + 13.27*260*1 - u1_slack1_steam[14]*100 - u1_slack2_steam[14]*100 + 14.89*260*1 - u1_slack1_steam[15]*100 - u1_slack2_steam[15]*100 + 14.9*260*1 - u1_slack1_steam[16]*100 - u1_slack2_steam[16]*100 + 14.63*260*1 - u1_slack1_steam[17]*100 - u1_slack2_steam[17]*100 + 14.99*260*1 - u1_slack1_steam[18]*100 - u1_slack2_steam[18]*100 + 14.37*260*1 - u1_slack1_steam[19]*100 - u1_slack2_steam[19]*100 + 14.69*260*1 - u1_slack1_steam[20]*100 - u1_slack2_steam[20]*100 + 14.87*260*1 - u1_slack1_steam[21]*100 - u1_slack2_steam[21]*100 + 12.54*260*1 - u1_slack1_steam[22]*100 - u1_slack2_steam[22]*100 + 10.89*260*1 - u1_slack1_steam[23]*100 - u1_slack2_steam[23]*100 + 5773*0.662*1 - u1_slack1_elec[0]*100 - u1_slack2_elec[0]*100 + 8625*0.662*1 - u1_slack1_elec[1]*100 - u1_slack2_elec[1]*100 + 8105*0.662*1 - u1_slack1_elec[2]*100 - u1_slack2_elec[2]*100 + 8165*0.662*1 - u1_slack1_elec[3]*100 - u1_slack2_elec[3]*100 + 7414*0.662*1 - u1_slack1_elec[4]*100 - u1_slack2_elec[4]*100 + 6884*0.662*1 - u1_slack1_elec[5]*100 - u1_slack2_elec[5]*100 + 6240*0.662*1 - u1_slack1_elec[6]*100 - u1_slack2_elec[6]*100 + 5910*0.662*1 - u1_slack1_elec[7]*100 - u1_slack2_elec[7]*100 + 8426*0.662*1 - u1_slack1_elec[8]*100 - u1_slack2_elec[8]*100 + 6641*0.662*1 - u1_slack1_elec[9]*100 - u1_slack2_elec[9]*100 + 6114*0.662*1 - u1_slack1_elec[10]*100 - u1_slack2_elec[10]*100 + 5349*0.662*1 - u1_slack1_elec[11]*100 - u1_slack2_elec[11]*100 + 6040*0.662*1 - u1_slack1_elec[12]*100 - u1_slack2_elec[12]*100 + 5979*0.662*1 - u1_slack1_elec[13]*100 - u1_slack2_elec[13]*100 + 6490*0.662*1 - u1_slack1_elec[14]*100 - u1_slack2_elec[14]*100 + 7239*0.662*1 - u1_slack1_elec[15]*100 - u1_slack2_elec[15]*100 + 9740*0.662*1 - u1_slack1_elec[16]*100 - u1_slack2_elec[16]*100 + 9222*0.662*1 - u1_slack1_elec[17]*100 - u1_slack2_elec[17]*100 + 8786*0.662*1 - u1_slack1_elec[18]*100 - u1_slack2_elec[18]*100 + 9702*0.662*1 - u1_slack1_elec[19]*100 - u1_slack2_elec[19]*100 + 6091*0.662*1 - u1_slack1_elec[20]*100 - u1_slack2_elec[20]*100 + 9470*0.662*1 - u1_slack1_elec[21]*100 - u1_slack2_elec[21]*100 + 9607*0.662*1 - u1_slack1_elec[22]*100 - u1_slack2_elec[22]*100 + 7122*0.662*1 - u1_slack1_elec[23]*100 - u1_slack2_elec[23]*100 + 0 - 1000.0*0.3*0.041667 - 1000.0*0.3*0.041667 - 1000.0*0.3*0.041667 - 1000.0*0.3*0.041667 - 1000.0*0.3*0.041667 - 1000.0*0.3*0.041667 - 1000.0*0.3*0.041667 - 1000.0*0.3*0.041667 - 1000.0*0.3*0.041667 - 1000.0*0.3*0.041667 - 1000.0*0.3*0.041667 - 1000.0*0.3*0.041667 - 1000.0*0.3*0.041667 - 1000.0*0.3*0.041667 - 1000.0*0.3*0.041667 - 1000.0*0.3*0.041667 - 1000.0*0.3*0.041667 - 1000.0*0.3*0.041667 - 1000.0*0.3*0.041667 - 1000.0*0.3*0.041667 - 1000.0*0.3*0.041667 - 1000.0*0.3*0.041667 - 1000.0*0.3*0.041667 - 1000.0*0.3*0.041667 - 4300*1.37*0.041667 - 4300*1.37*0.041667 - 4300*1.37*0.041667 - 4300*1.37*0.041667 - 4300*1.37*0.041667 - 4300*1.37*0.041667 - 4300*1.37*0.041667 - 4300*1.37*0.041667 - 4300*1.37*0.041667 - 4300*1.37*0.041667 - 4300*1.37*0.041667 - 4300*1.37*0.041667 - 4300*1.37*0.041667 - 4300*1.37*0.041667 - 4300*1.37*0.041667 - 4300*1.37*0.041667 - 4300*1.37*0.041667 - 4300*1.37*0.041667 - 4300*1.37*0.041667 - 4300*1.37*0.041667 - 4300*1.37*0.041667 - 4300*1.37*0.041667 - 4300*1.37*0.041667 - 4300*1.37*0.041667 - chp01_flag[0]*10 - chp01_flag[1]*10 - chp01_flag[2]*10 - chp01_flag[3]*10 - chp01_flag[4]*10 - chp01_flag[5]*10 - chp01_flag[6]*10 - chp01_flag[7]*10 - chp01_flag[8]*10 - chp01_flag[9]*10 - chp01_flag[10]*10 - chp01_flag[11]*10 - chp01_flag[12]*10 - chp01_flag[13]*10 - chp01_flag[14]*10 - chp01_flag[15]*10 - chp01_flag[16]*10 - chp01_flag[17]*10 - chp01_flag[18]*10 - chp01_flag[19]*10 - chp01_flag[20]*10 - chp01_flag[21]*10 - chp01_flag[22]*10 - chp01_flag[23]*10 - chp01_sUpflag[0]*180 - chp01_sUpflag[1]*180 - chp01_sUpflag[2]*180 - chp01_sUpflag[3]*180 - chp01_sUpflag[4]*180 - chp01_sUpflag[5]*180 - chp01_sUpflag[6]*180 - chp01_sUpflag[7]*180 - chp01_sUpflag[8]*180 - chp01_sUpflag[9]*180 - chp01_sUpflag[10]*180 - chp01_sUpflag[11]*180 - chp01_sUpflag[12]*180 - chp01_sUpflag[13]*180 - chp01_sUpflag[14]*180 - chp01_sUpflag[15]*180 - chp01_sUpflag[16]*180 - chp01_sUpflag[17]*180 - chp01_sUpflag[18]*180 - chp01_sUpflag[19]*180 - chp01_sUpflag[20]*180 - chp01_sUpflag[21]*180 - chp01_sUpflag[22]*180 - chp01_sUpflag[23]*180 - chp01_sDnflag[0]*80 - chp01_sDnflag[1]*80 - chp01_sDnflag[2]*80 - chp01_sDnflag[3]*80 - chp01_sDnflag[4]*80 - chp01_sDnflag[5]*80 - chp01_sDnflag[6]*80 - chp01_sDnflag[7]*80 - chp01_sDnflag[8]*80 - chp01_sDnflag[9]*80 - chp01_sDnflag[10]*80 - chp01_sDnflag[11]*80 - chp01_sDnflag[12]*80 - chp01_sDnflag[13]*80 - chp01_sDnflag[14]*80 - chp01_sDnflag[15]*80 - chp01_sDnflag[16]*80 - chp01_sDnflag[17]*80 - chp01_sDnflag[18]*80 - chp01_sDnflag[19]*80 - chp01_sDnflag[20]*80 - chp01_sDnflag[21]*80 - chp01_sDnflag[22]*80 - chp01_sDnflag[23]*80 - 2000*1.37*0.041667 - 2000*1.37*0.041667 - 2000*1.37*0.041667 - 2000*1.37*0.041667 - 2000*1.37*0.041667 - 2000*1.37*0.041667 - 2000*1.37*0.041667 - 2000*1.37*0.041667 - 2000*1.37*0.041667 - 2000*1.37*0.041667 - 2000*1.37*0.041667 - 2000*1.37*0.041667 - 2000*1.37*0.041667 - 2000*1.37*0.041667 - 2000*1.37*0.041667 - 2000*1.37*0.041667 - 2000*1.37*0.041667 - 2000*1.37*0.041667 - 2000*1.37*0.041667 - 2000*1.37*0.041667 - 2000*1.37*0.041667 - 2000*1.37*0.041667 - 2000*1.37*0.041667 - 2000*1.37*0.041667 - chp02_flag[0]*10 - chp02_flag[1]*10 - chp02_flag[2]*10 - chp02_flag[3]*10 - chp02_flag[4]*10 - chp02_flag[5]*10 - chp02_flag[6]*10 - chp02_flag[7]*10 - chp02_flag[8]*10 - chp02_flag[9]*10 - chp02_flag[10]*10 - chp02_flag[11]*10 - chp02_flag[12]*10 - chp02_flag[13]*10 - chp02_flag[14]*10 - chp02_flag[15]*10 - chp02_flag[16]*10 - chp02_flag[17]*10 - chp02_flag[18]*10 - chp02_flag[19]*10 - chp02_flag[20]*10 - chp02_flag[21]*10 - chp02_flag[22]*10 - chp02_flag[23]*10 - chp02_sUpflag[0]*180 - chp02_sUpflag[1]*180 - chp02_sUpflag[2]*180 - chp02_sUpflag[3]*180 - chp02_sUpflag[4]*180 - chp02_sUpflag[5]*180 - chp02_sUpflag[6]*180 - chp02_sUpflag[7]*180 - chp02_sUpflag[8]*180 - chp02_sUpflag[9]*180 - chp02_sUpflag[10]*180 - chp02_sUpflag[11]*180 - chp02_sUpflag[12]*180 - chp02_sUpflag[13]*180 - chp02_sUpflag[14]*180 - chp02_sUpflag[15]*180 - chp02_sUpflag[16]*180 - chp02_sUpflag[17]*180 - chp02_sUpflag[18]*180 - chp02_sUpflag[19]*180 - chp02_sUpflag[20]*180 - chp02_sUpflag[21]*180 - chp02_sUpflag[22]*180 - chp02_sUpflag[23]*180 - chp02_sDnflag[0]*80 - chp02_sDnflag[1]*80 - chp02_sDnflag[2]*80 - chp02_sDnflag[3]*80 - chp02_sDnflag[4]*80 - chp02_sDnflag[5]*80 - chp02_sDnflag[6]*80 - chp02_sDnflag[7]*80 - chp02_sDnflag[8]*80 - chp02_sDnflag[9]*80 - chp02_sDnflag[10]*80 - chp02_sDnflag[11]*80 - chp02_sDnflag[12]*80 - chp02_sDnflag[13]*80 - chp02_sDnflag[14]*80 - chp02_sDnflag[15]*80 - chp02_sDnflag[16]*80 - chp02_sDnflag[17]*80 - chp02_sDnflag[18]*80 - chp02_sDnflag[19]*80 - chp02_sDnflag[20]*80 - chp02_sDnflag[21]*80 - chp02_sDnflag[22]*80 - chp02_sDnflag[23]*80 - 3500*0.822*0.041667 - 3500*0.822*0.041667 - 3500*0.822*0.041667 - 3500*0.822*0.041667 - 3500*0.822*0.041667 - 3500*0.822*0.041667 - 3500*0.822*0.041667 - 3500*0.822*0.041667 - 3500*0.822*0.041667 - 3500*0.822*0.041667 - 3500*0.822*0.041667 - 3500*0.822*0.041667 - 3500*0.822*0.041667 - 3500*0.822*0.041667 - 3500*0.822*0.041667 - 3500*0.822*0.041667 - 3500*0.822*0.041667 - 3500*0.822*0.041667 - 3500*0.822*0.041667 - 3500*0.822*0.041667 - 3500*0.822*0.041667 - 3500*0.822*0.041667 - 3500*0.822*0.041667 - 3500*0.822*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - gsb02_flag[0]*10 - gsb02_flag[1]*10 - gsb02_flag[2]*10 - gsb02_flag[3]*10 - gsb02_flag[4]*10 - gsb02_flag[5]*10 - gsb02_flag[6]*10 - gsb02_flag[7]*10 - gsb02_flag[8]*10 - gsb02_flag[9]*10 - gsb02_flag[10]*10 - gsb02_flag[11]*10 - gsb02_flag[12]*10 - gsb02_flag[13]*10 - gsb02_flag[14]*10 - gsb02_flag[15]*10 - gsb02_flag[16]*10 - gsb02_flag[17]*10 - gsb02_flag[18]*10 - gsb02_flag[19]*10 - gsb02_flag[20]*10 - gsb02_flag[21]*10 - gsb02_flag[22]*10 - gsb02_flag[23]*10 - gsb02_sUpflag[0]*180 - gsb02_sUpflag[1]*180 - gsb02_sUpflag[2]*180 - gsb02_sUpflag[3]*180 - gsb02_sUpflag[4]*180 - gsb02_sUpflag[5]*180 - gsb02_sUpflag[6]*180 - gsb02_sUpflag[7]*180 - gsb02_sUpflag[8]*180 - gsb02_sUpflag[9]*180 - gsb02_sUpflag[10]*180 - gsb02_sUpflag[11]*180 - gsb02_sUpflag[12]*180 - gsb02_sUpflag[13]*180 - gsb02_sUpflag[14]*180 - gsb02_sUpflag[15]*180 - gsb02_sUpflag[16]*180 - gsb02_sUpflag[17]*180 - gsb02_sUpflag[18]*180 - gsb02_sUpflag[19]*180 - gsb02_sUpflag[20]*180 - gsb02_sUpflag[21]*180 - gsb02_sUpflag[22]*180 - gsb02_sUpflag[23]*180 - gsb02_sDnflag[0]*80 - gsb02_sDnflag[1]*80 - gsb02_sDnflag[2]*80 - gsb02_sDnflag[3]*80 - gsb02_sDnflag[4]*80 - gsb02_sDnflag[5]*80 - gsb02_sDnflag[6]*80 - gsb02_sDnflag[7]*80 - gsb02_sDnflag[8]*80 - gsb02_sDnflag[9]*80 - gsb02_sDnflag[10]*80 - gsb02_sDnflag[11]*80 - gsb02_sDnflag[12]*80 - gsb02_sDnflag[13]*80 - gsb02_sDnflag[14]*80 - gsb02_sDnflag[15]*80 - gsb02_sDnflag[16]*80 - gsb02_sDnflag[17]*80 - gsb02_sDnflag[18]*80 - gsb02_sDnflag[19]*80 - gsb02_sDnflag[20]*80 - gsb02_sDnflag[21]*80 - gsb02_sDnflag[22]*80 - gsb02_sDnflag[23]*80 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - gsb01_flag[0]*10 - gsb01_flag[1]*10 - gsb01_flag[2]*10 - gsb01_flag[3]*10 - gsb01_flag[4]*10 - gsb01_flag[5]*10 - gsb01_flag[6]*10 - gsb01_flag[7]*10 - gsb01_flag[8]*10 - gsb01_flag[9]*10 - gsb01_flag[10]*10 - gsb01_flag[11]*10 - gsb01_flag[12]*10 - gsb01_flag[13]*10 - gsb01_flag[14]*10 - gsb01_flag[15]*10 - gsb01_flag[16]*10 - gsb01_flag[17]*10 - gsb01_flag[18]*10 - gsb01_flag[19]*10 - gsb01_flag[20]*10 - gsb01_flag[21]*10 - gsb01_flag[22]*10 - gsb01_flag[23]*10 - gsb01_sUpflag[0]*180 - gsb01_sUpflag[1]*180 - gsb01_sUpflag[2]*180 - gsb01_sUpflag[3]*180 - gsb01_sUpflag[4]*180 - gsb01_sUpflag[5]*180 - gsb01_sUpflag[6]*180 - gsb01_sUpflag[7]*180 - gsb01_sUpflag[8]*180 - gsb01_sUpflag[9]*180 - gsb01_sUpflag[10]*180 - gsb01_sUpflag[11]*180 - gsb01_sUpflag[12]*180 - gsb01_sUpflag[13]*180 - gsb01_sUpflag[14]*180 - gsb01_sUpflag[15]*180 - gsb01_sUpflag[16]*180 - gsb01_sUpflag[17]*180 - gsb01_sUpflag[18]*180 - gsb01_sUpflag[19]*180 - gsb01_sUpflag[20]*180 - gsb01_sUpflag[21]*180 - gsb01_sUpflag[22]*180 - gsb01_sUpflag[23]*180 - gsb01_sDnflag[0]*80 - gsb01_sDnflag[1]*80 - gsb01_sDnflag[2]*80 - gsb01_sDnflag[3]*80 - gsb01_sDnflag[4]*80 - gsb01_sDnflag[5]*80 - gsb01_sDnflag[6]*80 - gsb01_sDnflag[7]*80 - gsb01_sDnflag[8]*80 - gsb01_sDnflag[9]*80 - gsb01_sDnflag[10]*80 - gsb01_sDnflag[11]*80 - gsb01_sDnflag[12]*80 - gsb01_sDnflag[13]*80 - gsb01_sDnflag[14]*80 - gsb01_sDnflag[15]*80 - gsb01_sDnflag[16]*80 - gsb01_sDnflag[17]*80 - gsb01_sDnflag[18]*80 - gsb01_sDnflag[19]*80 - gsb01_sDnflag[20]*80 - gsb01_sDnflag[21]*80 - gsb01_sDnflag[22]*80 - gsb01_sDnflag[23]*80 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - gsb03_flag[0]*10 - gsb03_flag[1]*10 - gsb03_flag[2]*10 - gsb03_flag[3]*10 - gsb03_flag[4]*10 - gsb03_flag[5]*10 - gsb03_flag[6]*10 - gsb03_flag[7]*10 - gsb03_flag[8]*10 - gsb03_flag[9]*10 - gsb03_flag[10]*10 - gsb03_flag[11]*10 - gsb03_flag[12]*10 - gsb03_flag[13]*10 - gsb03_flag[14]*10 - gsb03_flag[15]*10 - gsb03_flag[16]*10 - gsb03_flag[17]*10 - gsb03_flag[18]*10 - gsb03_flag[19]*10 - gsb03_flag[20]*10 - gsb03_flag[21]*10 - gsb03_flag[22]*10 - gsb03_flag[23]*10 - gsb03_sUpflag[0]*180 - gsb03_sUpflag[1]*180 - gsb03_sUpflag[2]*180 - gsb03_sUpflag[3]*180 - gsb03_sUpflag[4]*180 - gsb03_sUpflag[5]*180 - gsb03_sUpflag[6]*180 - gsb03_sUpflag[7]*180 - gsb03_sUpflag[8]*180 - gsb03_sUpflag[9]*180 - gsb03_sUpflag[10]*180 - gsb03_sUpflag[11]*180 - gsb03_sUpflag[12]*180 - gsb03_sUpflag[13]*180 - gsb03_sUpflag[14]*180 - gsb03_sUpflag[15]*180 - gsb03_sUpflag[16]*180 - gsb03_sUpflag[17]*180 - gsb03_sUpflag[18]*180 - gsb03_sUpflag[19]*180 - gsb03_sUpflag[20]*180 - gsb03_sUpflag[21]*180 - gsb03_sUpflag[22]*180 - gsb03_sUpflag[23]*180 - gsb03_sDnflag[0]*80 - gsb03_sDnflag[1]*80 - gsb03_sDnflag[2]*80 - gsb03_sDnflag[3]*80 - gsb03_sDnflag[4]*80 - gsb03_sDnflag[5]*80 - gsb03_sDnflag[6]*80 - gsb03_sDnflag[7]*80 - gsb03_sDnflag[8]*80 - gsb03_sDnflag[9]*80 - gsb03_sDnflag[10]*80 - gsb03_sDnflag[11]*80 - gsb03_sDnflag[12]*80 - gsb03_sDnflag[13]*80 - gsb03_sDnflag[14]*80 - gsb03_sDnflag[15]*80 - gsb03_sDnflag[16]*80 - gsb03_sDnflag[17]*80 - gsb03_sDnflag[18]*80 - gsb03_sDnflag[19]*80 - gsb03_sDnflag[20]*80 - gsb03_sDnflag[21]*80 - gsb03_sDnflag[22]*80 - gsb03_sDnflag[23]*80 - s1_gE_out[0]*2.42 - s1_eE_out[0]*0.4077 - s1_eE_in[0]*(-1)*1*0.38 - s1_gE_out[1]*2.42 - s1_eE_out[1]*0.4077 - s1_eE_in[1]*(-1)*1*0.38 - s1_gE_out[2]*2.42 - s1_eE_out[2]*0.4077 - s1_eE_in[2]*(-1)*1*0.38 - s1_gE_out[3]*2.42 - s1_eE_out[3]*0.4077 - s1_eE_in[3]*(-1)*1*0.38 - s1_gE_out[4]*2.42 - s1_eE_out[4]*0.4077 - s1_eE_in[4]*(-1)*1*0.38 - s1_gE_out[5]*2.42 - s1_eE_out[5]*0.4077 - s1_eE_in[5]*(-1)*1*0.38 - s1_gE_out[6]*2.42 - s1_eE_out[6]*0.4077 - s1_eE_in[6]*(-1)*1*0.38 - s1_gE_out[7]*2.42 - s1_eE_out[7]*0.4077 - s1_eE_in[7]*(-1)*1*0.38 - s1_gE_out[8]*2.42 - s1_eE_out[8]*0.4077 - s1_eE_in[8]*(-1)*1*0.38 - s1_gE_out[9]*2.42 - s1_eE_out[9]*0.646 - s1_eE_in[9]*(-1)*1*0.5 - s1_gE_out[10]*2.42 - s1_eE_out[10]*0.646 - s1_eE_in[10]*(-1)*1*0.5 - s1_gE_out[11]*2.42 - s1_eE_out[11]*0.646 - s1_eE_in[11]*(-1)*1*0.5 - s1_gE_out[12]*2.42 - s1_eE_out[12]*1.0238 - s1_eE_in[12]*(-1)*1*0.7 - s1_gE_out[13]*2.42 - s1_eE_out[13]*1.0238 - s1_eE_in[13]*(-1)*1*0.7 - s1_gE_out[14]*2.42 - s1_eE_out[14]*1.0238 - s1_eE_in[14]*(-1)*1*0.7 - s1_gE_out[15]*2.42 - s1_eE_out[15]*1.0238 - s1_eE_in[15]*(-1)*1*0.7 - s1_gE_out[16]*2.42 - s1_eE_out[16]*1.0238 - s1_eE_in[16]*(-1)*1*0.7 - s1_gE_out[17]*2.42 - s1_eE_out[17]*1.0238 - s1_eE_in[17]*(-1)*1*0.7 - s1_gE_out[18]*2.42 - s1_eE_out[18]*1.0238 - s1_eE_in[18]*(-1)*1*0.7 - s1_gE_out[19]*2.42 - s1_eE_out[19]*1.0238 - s1_eE_in[19]*(-1)*1*0.7 - s1_gE_out[20]*2.42 - s1_eE_out[20]*1.0238 - s1_eE_in[20]*(-1)*1*0.7 - s1_gE_out[21]*2.42 - s1_eE_out[21]*1.0238 - s1_eE_in[21]*(-1)*1*0.7 - s1_gE_out[22]*2.42 - s1_eE_out[22]*0.4077 - s1_eE_in[22]*(-1)*1*0.38 - s1_gE_out[23]*2.42 - s1_eE_out[23]*0.4077 - s1_eE_in[23]*(-1)*1*0.38 - max_profit_0 == 0
 
    prob += 13.16*260*1 - u1_slack1_steam[0]*100 - u1_slack2_steam[0]*100 + 13.69*260*1 - u1_slack1_steam[1]*100 - u1_slack2_steam[1]*100 + 13.49*260*1 - u1_slack1_steam[2]*100 - u1_slack2_steam[2]*100 + 11.51*260*1 - u1_slack1_steam[3]*100 - u1_slack2_steam[3]*100 + 13.34*260*1 - u1_slack1_steam[4]*100 - u1_slack2_steam[4]*100 + 13.43*260*1 - u1_slack1_steam[5]*100 - u1_slack2_steam[5]*100 + 12.77*260*1 - u1_slack1_steam[6]*100 - u1_slack2_steam[6]*100 + 13.78*260*1 - u1_slack1_steam[7]*100 - u1_slack2_steam[7]*100 + 14.12*260*1 - u1_slack1_steam[8]*100 - u1_slack2_steam[8]*100 + 12.55*260*1 - u1_slack1_steam[9]*100 - u1_slack2_steam[9]*100 + 12.36*260*1 - u1_slack1_steam[10]*100 - u1_slack2_steam[10]*100 + 12.28*260*1 - u1_slack1_steam[11]*100 - u1_slack2_steam[11]*100 + 13.08*260*1 - u1_slack1_steam[12]*100 - u1_slack2_steam[12]*100 + 12.41*260*1 - u1_slack1_steam[13]*100 - u1_slack2_steam[13]*100 + 13.27*260*1 - u1_slack1_steam[14]*100 - u1_slack2_steam[14]*100 + 14.89*260*1 - u1_slack1_steam[15]*100 - u1_slack2_steam[15]*100 + 14.9*260*1 - u1_slack1_steam[16]*100 - u1_slack2_steam[16]*100 + 14.63*260*1 - u1_slack1_steam[17]*100 - u1_slack2_steam[17]*100 + 14.99*260*1 - u1_slack1_steam[18]*100 - u1_slack2_steam[18]*100 + 14.37*260*1 - u1_slack1_steam[19]*100 - u1_slack2_steam[19]*100 + 14.69*260*1 - u1_slack1_steam[20]*100 - u1_slack2_steam[20]*100 + 14.87*260*1 - u1_slack1_steam[21]*100 - u1_slack2_steam[21]*100 + 12.54*260*1 - u1_slack1_steam[22]*100 - u1_slack2_steam[22]*100 + 10.89*260*1 - u1_slack1_steam[23]*100 - u1_slack2_steam[23]*100 + 5773*0.662*1 - u1_slack1_elec[0]*100 - u1_slack2_elec[0]*100 + 8625*0.662*1 - u1_slack1_elec[1]*100 - u1_slack2_elec[1]*100 + 8105*0.662*1 - u1_slack1_elec[2]*100 - u1_slack2_elec[2]*100 + 8165*0.662*1 - u1_slack1_elec[3]*100 - u1_slack2_elec[3]*100 + 7414*0.662*1 - u1_slack1_elec[4]*100 - u1_slack2_elec[4]*100 + 6884*0.662*1 - u1_slack1_elec[5]*100 - u1_slack2_elec[5]*100 + 6240*0.662*1 - u1_slack1_elec[6]*100 - u1_slack2_elec[6]*100 + 5910*0.662*1 - u1_slack1_elec[7]*100 - u1_slack2_elec[7]*100 + 8426*0.662*1 - u1_slack1_elec[8]*100 - u1_slack2_elec[8]*100 + 6641*0.662*1 - u1_slack1_elec[9]*100 - u1_slack2_elec[9]*100 + 6114*0.662*1 - u1_slack1_elec[10]*100 - u1_slack2_elec[10]*100 + 5349*0.662*1 - u1_slack1_elec[11]*100 - u1_slack2_elec[11]*100 + 6040*0.662*1 - u1_slack1_elec[12]*100 - u1_slack2_elec[12]*100 + 5979*0.662*1 - u1_slack1_elec[13]*100 - u1_slack2_elec[13]*100 + 6490*0.662*1 - u1_slack1_elec[14]*100 - u1_slack2_elec[14]*100 + 7239*0.662*1 - u1_slack1_elec[15]*100 - u1_slack2_elec[15]*100 + 9740*0.662*1 - u1_slack1_elec[16]*100 - u1_slack2_elec[16]*100 + 9222*0.662*1 - u1_slack1_elec[17]*100 - u1_slack2_elec[17]*100 + 8786*0.662*1 - u1_slack1_elec[18]*100 - u1_slack2_elec[18]*100 + 9702*0.662*1 - u1_slack1_elec[19]*100 - u1_slack2_elec[19]*100 + 6091*0.662*1 - u1_slack1_elec[20]*100 - u1_slack2_elec[20]*100 + 9470*0.662*1 - u1_slack1_elec[21]*100 - u1_slack2_elec[21]*100 + 9607*0.662*1 - u1_slack1_elec[22]*100 - u1_slack2_elec[22]*100 + 7122*0.662*1 - u1_slack1_elec[23]*100 - u1_slack2_elec[23]*100 + 0 - 1000.0*0.3*0.041667 - 1000.0*0.3*0.041667 - 1000.0*0.3*0.041667 - 1000.0*0.3*0.041667 - 1000.0*0.3*0.041667 - 1000.0*0.3*0.041667 - 1000.0*0.3*0.041667 - 1000.0*0.3*0.041667 - 1000.0*0.3*0.041667 - 1000.0*0.3*0.041667 - 1000.0*0.3*0.041667 - 1000.0*0.3*0.041667 - 1000.0*0.3*0.041667 - 1000.0*0.3*0.041667 - 1000.0*0.3*0.041667 - 1000.0*0.3*0.041667 - 1000.0*0.3*0.041667 - 1000.0*0.3*0.041667 - 1000.0*0.3*0.041667 - 1000.0*0.3*0.041667 - 1000.0*0.3*0.041667 - 1000.0*0.3*0.041667 - 1000.0*0.3*0.041667 - 1000.0*0.3*0.041667 - 4300*1.37*0.041667 - 4300*1.37*0.041667 - 4300*1.37*0.041667 - 4300*1.37*0.041667 - 4300*1.37*0.041667 - 4300*1.37*0.041667 - 4300*1.37*0.041667 - 4300*1.37*0.041667 - 4300*1.37*0.041667 - 4300*1.37*0.041667 - 4300*1.37*0.041667 - 4300*1.37*0.041667 - 4300*1.37*0.041667 - 4300*1.37*0.041667 - 4300*1.37*0.041667 - 4300*1.37*0.041667 - 4300*1.37*0.041667 - 4300*1.37*0.041667 - 4300*1.37*0.041667 - 4300*1.37*0.041667 - 4300*1.37*0.041667 - 4300*1.37*0.041667 - 4300*1.37*0.041667 - 4300*1.37*0.041667 - chp01_flag[0]*10 - chp01_flag[1]*10 - chp01_flag[2]*10 - chp01_flag[3]*10 - chp01_flag[4]*10 - chp01_flag[5]*10 - chp01_flag[6]*10 - chp01_flag[7]*10 - chp01_flag[8]*10 - chp01_flag[9]*10 - chp01_flag[10]*10 - chp01_flag[11]*10 - chp01_flag[12]*10 - chp01_flag[13]*10 - chp01_flag[14]*10 - chp01_flag[15]*10 - chp01_flag[16]*10 - chp01_flag[17]*10 - chp01_flag[18]*10 - chp01_flag[19]*10 - chp01_flag[20]*10 - chp01_flag[21]*10 - chp01_flag[22]*10 - chp01_flag[23]*10 - chp01_sUpflag[0]*180 - chp01_sUpflag[1]*180 - chp01_sUpflag[2]*180 - chp01_sUpflag[3]*180 - chp01_sUpflag[4]*180 - chp01_sUpflag[5]*180 - chp01_sUpflag[6]*180 - chp01_sUpflag[7]*180 - chp01_sUpflag[8]*180 - chp01_sUpflag[9]*180 - chp01_sUpflag[10]*180 - chp01_sUpflag[11]*180 - chp01_sUpflag[12]*180 - chp01_sUpflag[13]*180 - chp01_sUpflag[14]*180 - chp01_sUpflag[15]*180 - chp01_sUpflag[16]*180 - chp01_sUpflag[17]*180 - chp01_sUpflag[18]*180 - chp01_sUpflag[19]*180 - chp01_sUpflag[20]*180 - chp01_sUpflag[21]*180 - chp01_sUpflag[22]*180 - chp01_sUpflag[23]*180 - chp01_sDnflag[0]*80 - chp01_sDnflag[1]*80 - chp01_sDnflag[2]*80 - chp01_sDnflag[3]*80 - chp01_sDnflag[4]*80 - chp01_sDnflag[5]*80 - chp01_sDnflag[6]*80 - chp01_sDnflag[7]*80 - chp01_sDnflag[8]*80 - chp01_sDnflag[9]*80 - chp01_sDnflag[10]*80 - chp01_sDnflag[11]*80 - chp01_sDnflag[12]*80 - chp01_sDnflag[13]*80 - chp01_sDnflag[14]*80 - chp01_sDnflag[15]*80 - chp01_sDnflag[16]*80 - chp01_sDnflag[17]*80 - chp01_sDnflag[18]*80 - chp01_sDnflag[19]*80 - chp01_sDnflag[20]*80 - chp01_sDnflag[21]*80 - chp01_sDnflag[22]*80 - chp01_sDnflag[23]*80 - 2000*1.37*0.041667 - 2000*1.37*0.041667 - 2000*1.37*0.041667 - 2000*1.37*0.041667 - 2000*1.37*0.041667 - 2000*1.37*0.041667 - 2000*1.37*0.041667 - 2000*1.37*0.041667 - 2000*1.37*0.041667 - 2000*1.37*0.041667 - 2000*1.37*0.041667 - 2000*1.37*0.041667 - 2000*1.37*0.041667 - 2000*1.37*0.041667 - 2000*1.37*0.041667 - 2000*1.37*0.041667 - 2000*1.37*0.041667 - 2000*1.37*0.041667 - 2000*1.37*0.041667 - 2000*1.37*0.041667 - 2000*1.37*0.041667 - 2000*1.37*0.041667 - 2000*1.37*0.041667 - 2000*1.37*0.041667 - chp02_flag[0]*10 - chp02_flag[1]*10 - chp02_flag[2]*10 - chp02_flag[3]*10 - chp02_flag[4]*10 - chp02_flag[5]*10 - chp02_flag[6]*10 - chp02_flag[7]*10 - chp02_flag[8]*10 - chp02_flag[9]*10 - chp02_flag[10]*10 - chp02_flag[11]*10 - chp02_flag[12]*10 - chp02_flag[13]*10 - chp02_flag[14]*10 - chp02_flag[15]*10 - chp02_flag[16]*10 - chp02_flag[17]*10 - chp02_flag[18]*10 - chp02_flag[19]*10 - chp02_flag[20]*10 - chp02_flag[21]*10 - chp02_flag[22]*10 - chp02_flag[23]*10 - chp02_sUpflag[0]*180 - chp02_sUpflag[1]*180 - chp02_sUpflag[2]*180 - chp02_sUpflag[3]*180 - chp02_sUpflag[4]*180 - chp02_sUpflag[5]*180 - chp02_sUpflag[6]*180 - chp02_sUpflag[7]*180 - chp02_sUpflag[8]*180 - chp02_sUpflag[9]*180 - chp02_sUpflag[10]*180 - chp02_sUpflag[11]*180 - chp02_sUpflag[12]*180 - chp02_sUpflag[13]*180 - chp02_sUpflag[14]*180 - chp02_sUpflag[15]*180 - chp02_sUpflag[16]*180 - chp02_sUpflag[17]*180 - chp02_sUpflag[18]*180 - chp02_sUpflag[19]*180 - chp02_sUpflag[20]*180 - chp02_sUpflag[21]*180 - chp02_sUpflag[22]*180 - chp02_sUpflag[23]*180 - chp02_sDnflag[0]*80 - chp02_sDnflag[1]*80 - chp02_sDnflag[2]*80 - chp02_sDnflag[3]*80 - chp02_sDnflag[4]*80 - chp02_sDnflag[5]*80 - chp02_sDnflag[6]*80 - chp02_sDnflag[7]*80 - chp02_sDnflag[8]*80 - chp02_sDnflag[9]*80 - chp02_sDnflag[10]*80 - chp02_sDnflag[11]*80 - chp02_sDnflag[12]*80 - chp02_sDnflag[13]*80 - chp02_sDnflag[14]*80 - chp02_sDnflag[15]*80 - chp02_sDnflag[16]*80 - chp02_sDnflag[17]*80 - chp02_sDnflag[18]*80 - chp02_sDnflag[19]*80 - chp02_sDnflag[20]*80 - chp02_sDnflag[21]*80 - chp02_sDnflag[22]*80 - chp02_sDnflag[23]*80 - 3500*0.822*0.041667 - 3500*0.822*0.041667 - 3500*0.822*0.041667 - 3500*0.822*0.041667 - 3500*0.822*0.041667 - 3500*0.822*0.041667 - 3500*0.822*0.041667 - 3500*0.822*0.041667 - 3500*0.822*0.041667 - 3500*0.822*0.041667 - 3500*0.822*0.041667 - 3500*0.822*0.041667 - 3500*0.822*0.041667 - 3500*0.822*0.041667 - 3500*0.822*0.041667 - 3500*0.822*0.041667 - 3500*0.822*0.041667 - 3500*0.822*0.041667 - 3500*0.822*0.041667 - 3500*0.822*0.041667 - 3500*0.822*0.041667 - 3500*0.822*0.041667 - 3500*0.822*0.041667 - 3500*0.822*0.041667 -  - pv01_eE_out[0] * 100.0 -  - pv01_eE_out[1] * 100.0 -  - pv01_eE_out[2] * 100.0 -  - pv01_eE_out[3] * 100.0 -  - pv01_eE_out[4] * 100.0 -  - pv01_eE_out[5] * 100.0 -  - pv01_eE_out[6] * 100.0 -  - pv01_eE_out[7] * 100.0 -  - pv01_eE_out[8] * 100.0 -  - pv01_eE_out[9] * 100.0 -  - pv01_eE_out[10] * 100.0 -  - pv01_eE_out[11] * 100.0 -  - pv01_eE_out[12] * 100.0 -  - pv01_eE_out[13] * 100.0 -  - pv01_eE_out[14] * 100.0 -  - pv01_eE_out[15] * 100.0 -  - pv01_eE_out[16] * 100.0 -  - pv01_eE_out[17] * 100.0 -  - pv01_eE_out[18] * 100.0 -  - pv01_eE_out[19] * 100.0 -  - pv01_eE_out[20] * 100.0 -  - pv01_eE_out[21] * 100.0 -  - pv01_eE_out[22] * 100.0 -  - pv01_eE_out[23] * 100.0 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - gsb02_flag[0]*10 - gsb02_flag[1]*10 - gsb02_flag[2]*10 - gsb02_flag[3]*10 - gsb02_flag[4]*10 - gsb02_flag[5]*10 - gsb02_flag[6]*10 - gsb02_flag[7]*10 - gsb02_flag[8]*10 - gsb02_flag[9]*10 - gsb02_flag[10]*10 - gsb02_flag[11]*10 - gsb02_flag[12]*10 - gsb02_flag[13]*10 - gsb02_flag[14]*10 - gsb02_flag[15]*10 - gsb02_flag[16]*10 - gsb02_flag[17]*10 - gsb02_flag[18]*10 - gsb02_flag[19]*10 - gsb02_flag[20]*10 - gsb02_flag[21]*10 - gsb02_flag[22]*10 - gsb02_flag[23]*10 - gsb02_sUpflag[0]*180 - gsb02_sUpflag[1]*180 - gsb02_sUpflag[2]*180 - gsb02_sUpflag[3]*180 - gsb02_sUpflag[4]*180 - gsb02_sUpflag[5]*180 - gsb02_sUpflag[6]*180 - gsb02_sUpflag[7]*180 - gsb02_sUpflag[8]*180 - gsb02_sUpflag[9]*180 - gsb02_sUpflag[10]*180 - gsb02_sUpflag[11]*180 - gsb02_sUpflag[12]*180 - gsb02_sUpflag[13]*180 - gsb02_sUpflag[14]*180 - gsb02_sUpflag[15]*180 - gsb02_sUpflag[16]*180 - gsb02_sUpflag[17]*180 - gsb02_sUpflag[18]*180 - gsb02_sUpflag[19]*180 - gsb02_sUpflag[20]*180 - gsb02_sUpflag[21]*180 - gsb02_sUpflag[22]*180 - gsb02_sUpflag[23]*180 - gsb02_sDnflag[0]*80 - gsb02_sDnflag[1]*80 - gsb02_sDnflag[2]*80 - gsb02_sDnflag[3]*80 - gsb02_sDnflag[4]*80 - gsb02_sDnflag[5]*80 - gsb02_sDnflag[6]*80 - gsb02_sDnflag[7]*80 - gsb02_sDnflag[8]*80 - gsb02_sDnflag[9]*80 - gsb02_sDnflag[10]*80 - gsb02_sDnflag[11]*80 - gsb02_sDnflag[12]*80 - gsb02_sDnflag[13]*80 - gsb02_sDnflag[14]*80 - gsb02_sDnflag[15]*80 - gsb02_sDnflag[16]*80 - gsb02_sDnflag[17]*80 - gsb02_sDnflag[18]*80 - gsb02_sDnflag[19]*80 - gsb02_sDnflag[20]*80 - gsb02_sDnflag[21]*80 - gsb02_sDnflag[22]*80 - gsb02_sDnflag[23]*80 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - gsb01_flag[0]*10 - gsb01_flag[1]*10 - gsb01_flag[2]*10 - gsb01_flag[3]*10 - gsb01_flag[4]*10 - gsb01_flag[5]*10 - gsb01_flag[6]*10 - gsb01_flag[7]*10 - gsb01_flag[8]*10 - gsb01_flag[9]*10 - gsb01_flag[10]*10 - gsb01_flag[11]*10 - gsb01_flag[12]*10 - gsb01_flag[13]*10 - gsb01_flag[14]*10 - gsb01_flag[15]*10 - gsb01_flag[16]*10 - gsb01_flag[17]*10 - gsb01_flag[18]*10 - gsb01_flag[19]*10 - gsb01_flag[20]*10 - gsb01_flag[21]*10 - gsb01_flag[22]*10 - gsb01_flag[23]*10 - gsb01_sUpflag[0]*180 - gsb01_sUpflag[1]*180 - gsb01_sUpflag[2]*180 - gsb01_sUpflag[3]*180 - gsb01_sUpflag[4]*180 - gsb01_sUpflag[5]*180 - gsb01_sUpflag[6]*180 - gsb01_sUpflag[7]*180 - gsb01_sUpflag[8]*180 - gsb01_sUpflag[9]*180 - gsb01_sUpflag[10]*180 - gsb01_sUpflag[11]*180 - gsb01_sUpflag[12]*180 - gsb01_sUpflag[13]*180 - gsb01_sUpflag[14]*180 - gsb01_sUpflag[15]*180 - gsb01_sUpflag[16]*180 - gsb01_sUpflag[17]*180 - gsb01_sUpflag[18]*180 - gsb01_sUpflag[19]*180 - gsb01_sUpflag[20]*180 - gsb01_sUpflag[21]*180 - gsb01_sUpflag[22]*180 - gsb01_sUpflag[23]*180 - gsb01_sDnflag[0]*80 - gsb01_sDnflag[1]*80 - gsb01_sDnflag[2]*80 - gsb01_sDnflag[3]*80 - gsb01_sDnflag[4]*80 - gsb01_sDnflag[5]*80 - gsb01_sDnflag[6]*80 - gsb01_sDnflag[7]*80 - gsb01_sDnflag[8]*80 - gsb01_sDnflag[9]*80 - gsb01_sDnflag[10]*80 - gsb01_sDnflag[11]*80 - gsb01_sDnflag[12]*80 - gsb01_sDnflag[13]*80 - gsb01_sDnflag[14]*80 - gsb01_sDnflag[15]*80 - gsb01_sDnflag[16]*80 - gsb01_sDnflag[17]*80 - gsb01_sDnflag[18]*80 - gsb01_sDnflag[19]*80 - gsb01_sDnflag[20]*80 - gsb01_sDnflag[21]*80 - gsb01_sDnflag[22]*80 - gsb01_sDnflag[23]*80 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - 10*12.77*0.041667 - gsb03_flag[0]*10 - gsb03_flag[1]*10 - gsb03_flag[2]*10 - gsb03_flag[3]*10 - gsb03_flag[4]*10 - gsb03_flag[5]*10 - gsb03_flag[6]*10 - gsb03_flag[7]*10 - gsb03_flag[8]*10 - gsb03_flag[9]*10 - gsb03_flag[10]*10 - gsb03_flag[11]*10 - gsb03_flag[12]*10 - gsb03_flag[13]*10 - gsb03_flag[14]*10 - gsb03_flag[15]*10 - gsb03_flag[16]*10 - gsb03_flag[17]*10 - gsb03_flag[18]*10 - gsb03_flag[19]*10 - gsb03_flag[20]*10 - gsb03_flag[21]*10 - gsb03_flag[22]*10 - gsb03_flag[23]*10 - gsb03_sUpflag[0]*180 - gsb03_sUpflag[1]*180 - gsb03_sUpflag[2]*180 - gsb03_sUpflag[3]*180 - gsb03_sUpflag[4]*180 - gsb03_sUpflag[5]*180 - gsb03_sUpflag[6]*180 - gsb03_sUpflag[7]*180 - gsb03_sUpflag[8]*180 - gsb03_sUpflag[9]*180 - gsb03_sUpflag[10]*180 - gsb03_sUpflag[11]*180 - gsb03_sUpflag[12]*180 - gsb03_sUpflag[13]*180 - gsb03_sUpflag[14]*180 - gsb03_sUpflag[15]*180 - gsb03_sUpflag[16]*180 - gsb03_sUpflag[17]*180 - gsb03_sUpflag[18]*180 - gsb03_sUpflag[19]*180 - gsb03_sUpflag[20]*180 - gsb03_sUpflag[21]*180 - gsb03_sUpflag[22]*180 - gsb03_sUpflag[23]*180 - gsb03_sDnflag[0]*80 - gsb03_sDnflag[1]*80 - gsb03_sDnflag[2]*80 - gsb03_sDnflag[3]*80 - gsb03_sDnflag[4]*80 - gsb03_sDnflag[5]*80 - gsb03_sDnflag[6]*80 - gsb03_sDnflag[7]*80 - gsb03_sDnflag[8]*80 - gsb03_sDnflag[9]*80 - gsb03_sDnflag[10]*80 - gsb03_sDnflag[11]*80 - gsb03_sDnflag[12]*80 - gsb03_sDnflag[13]*80 - gsb03_sDnflag[14]*80 - gsb03_sDnflag[15]*80 - gsb03_sDnflag[16]*80 - gsb03_sDnflag[17]*80 - gsb03_sDnflag[18]*80 - gsb03_sDnflag[19]*80 - gsb03_sDnflag[20]*80 - gsb03_sDnflag[21]*80 - gsb03_sDnflag[22]*80 - gsb03_sDnflag[23]*80 - s1_gE_out[0]*2.42 - s1_eE_out[0]*0.4077 - s1_eE_in[0]*(-1)*1*0.38 - s1_gE_out[1]*2.42 - s1_eE_out[1]*0.4077 - s1_eE_in[1]*(-1)*1*0.38 - s1_gE_out[2]*2.42 - s1_eE_out[2]*0.4077 - s1_eE_in[2]*(-1)*1*0.38 - s1_gE_out[3]*2.42 - s1_eE_out[3]*0.4077 - s1_eE_in[3]*(-1)*1*0.38 - s1_gE_out[4]*2.42 - s1_eE_out[4]*0.4077 - s1_eE_in[4]*(-1)*1*0.38 - s1_gE_out[5]*2.42 - s1_eE_out[5]*0.4077 - s1_eE_in[5]*(-1)*1*0.38 - s1_gE_out[6]*2.42 - s1_eE_out[6]*0.4077 - s1_eE_in[6]*(-1)*1*0.38 - s1_gE_out[7]*2.42 - s1_eE_out[7]*0.4077 - s1_eE_in[7]*(-1)*1*0.38 - s1_gE_out[8]*2.42 - s1_eE_out[8]*0.4077 - s1_eE_in[8]*(-1)*1*0.38 - s1_gE_out[9]*2.42 - s1_eE_out[9]*0.646 - s1_eE_in[9]*(-1)*1*0.5 - s1_gE_out[10]*2.42 - s1_eE_out[10]*0.646 - s1_eE_in[10]*(-1)*1*0.5 - s1_gE_out[11]*2.42 - s1_eE_out[11]*0.646 - s1_eE_in[11]*(-1)*1*0.5 - s1_gE_out[12]*2.42 - s1_eE_out[12]*1.0238 - s1_eE_in[12]*(-1)*1*0.7 - s1_gE_out[13]*2.42 - s1_eE_out[13]*1.0238 - s1_eE_in[13]*(-1)*1*0.7 - s1_gE_out[14]*2.42 - s1_eE_out[14]*1.0238 - s1_eE_in[14]*(-1)*1*0.7 - s1_gE_out[15]*2.42 - s1_eE_out[15]*1.0238 - s1_eE_in[15]*(-1)*1*0.7 - s1_gE_out[16]*2.42 - s1_eE_out[16]*1.0238 - s1_eE_in[16]*(-1)*1*0.7 - s1_gE_out[17]*2.42 - s1_eE_out[17]*1.0238 - s1_eE_in[17]*(-1)*1*0.7 - s1_gE_out[18]*2.42 - s1_eE_out[18]*1.0238 - s1_eE_in[18]*(-1)*1*0.7 - s1_gE_out[19]*2.42 - s1_eE_out[19]*1.0238 - s1_eE_in[19]*(-1)*1*0.7 - s1_gE_out[20]*2.42 - s1_eE_out[20]*1.0238 - s1_eE_in[20]*(-1)*1*0.7 - s1_gE_out[21]*2.42 - s1_eE_out[21]*1.0238 - s1_eE_in[21]*(-1)*1*0.7 - s1_gE_out[22]*2.42 - s1_eE_out[22]*0.4077 - s1_eE_in[22]*(-1)*1*0.38 - s1_gE_out[23]*2.42 - s1_eE_out[23]*0.4077 - s1_eE_in[23]*(-1)*1*0.38 - 0
    
    # pid = os.getpid()
    pid = 'maxProfit'
    tmpLp = os.path.join("data/%s.lp" % pid)
    tmpMps = os.path.join("data/%s.mps" % pid)
    tmpSol = os.path.join("data/%s.sol" % pid)
    glpk_path = 'C:\glpk-4.65\w32\glpsol.exe'
    
  
    # The problem is solved using PuLP's choice of Solver
    try:
        # Solve using CPLEX with logging
        prob.solve(CPLEX_CMD(timelimit=3600, msg=0))
        # prob.solve(GUROBI_CMD()) # Solve using Gurobi
        # prob.solve(COIN_CMD(msg=0))
    except Exception:
        print('Solver infeasible, check please!!!')
        return False
        

    import json
    newjson={}
    for key, val in loads.items():
        for sub_key, sub_val in val.items():
            print("{0:>27s} = ".format(key + '_' + sub_key), end='')
            for i in range(t_num):
                print(" {0:<10.2f}".format(sub_val[i]), end=' ')
            rs = map(float, sub_val)
            newjson[key + '_' + sub_key]= list(rs)
            print('')
    # print("{0:>17s} = {1:<10d}".format('status', prob.status), end = '')
    if LpStatus[prob.status] == 'Optimal':
        name = 'index'
        temp = [i for i in range(t_num)]
        newjson[name] = temp
        
        for v in prob.variables():
            tname = '_'.join(v.name.split('_')[:-1])
            if v.name == '__dummy' or tname.split('_')[-2] in ['x', 'y']:
                continue
            else:
                tnum = int(v.name.split('_')[-1])
                if tname != name:
                    # print the previous variable values
                    print("{0:>27s} = ".format(name), end='')
                    for i in range(t_num):
                        print(" {0:<10.2f}".format(temp[i]), end=' ')
                    print('')
                    # assign a new variable to 'name'
                    name = tname
                    temp[tnum] = v.varValue
                else:
                    temp[tnum] = v.varValue
                newjson[name] = temp.copy()

        # print last variable
        print("{0:>27s} = ".format(name), end='')
        for i in range(t_num):
            print(" {0:<10.2f}".format(temp[i]), end=' ')
    print('')
    listmax = newjson["max_profit"]
    from config import get_config_values
    fla1= int(get_config_values("flag","flag_pv"))
    fla2= int(get_config_values("flag","flag_stg"))
    if 0==fla1 and 0 == fla2:
        if len(listmax)>0:
            listmax[0] = listmax[0]+16000-240
            newjson["max_profit"] = listmax
    with open("newjson.json","w") as f:
        json.dump(newjson,f)
    print("{0:>17s} = {1:<17s}".format('status', LpStatus[prob.status]), end='')
    print("{0:<17d}".format(prob.status), end='')
    print('')
    
