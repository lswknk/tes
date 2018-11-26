import numpy as np
import matplotlib.pyplot as plt
import json
from pylab import mpl
import matplotlib
import os
import configparser

# 项目路径
rootDir = os.path.split(os.path.realpath(__file__))[0]
# config.ini文件路径
configFilePath = os.path.join(rootDir, 'config.ini')

def get_config_values(section, option):
    """
    根据传入的section获取对应的value
    :param section: ini配置文件中用[]标识的内容
    :return:
    """
    config = configparser.ConfigParser()
    config.read(configFilePath)
    # return config.items(section=section)
    return config.get(section=section, option=option)

#####正：chp01_eE_out (CHP1发电量）， chp02_eE_out（CHP2发电量）, *pv01_eE_out（光伏发电量）, *stg01_eE_out（储能放电量）, s1_eE_out（不足网补电量）;
#####负：s1_eE_in（余电上网电量）, elecLoads_u1（用户总需求电量）, *stg01_eE_in（储能充电电量）



def draw_stable():
    plot_f = open('newjson.json', 'r')
    flag_pv = get_config_values('flag','flag_pv')
    flag_stg = get_config_values('flag','flag_stg')
    flag_good = get_config_values('flag','flag_good')
    flag_price = get_config_values('flag','flag_price')
    print(flag_pv)
    ###标题
    title = ""
    if flag_pv == '1':
        title += "光伏：开  "
    if flag_pv == '0':
        title += "光伏：关  "
    if flag_stg == '1':
        title += "存储：开  "
    if flag_stg == '0':
        title += "存储：关  "
    if flag_good == '1':
        title += "平稳：是  "
    if flag_good == '0':
        title += "平稳：关  "
    if flag_price == '0':
        title += "新价格：是  "
    if flag_price == '1':
        title += "新价格：否  "

    load_dic = json.load(plot_f)
    scene_1_value = [load_dic['chp01_eE_out'],load_dic['chp02_eE_out'],load_dic['pv01_eE_out'],load_dic['stg01_eE_out'],load_dic['s1_eE_out']]
    scene_11_value = [load_dic['s1_eE_in'],load_dic['elecLoads_u1'],load_dic['stg01_eE_in']]
    max_profit = "%0.2f" % load_dic['max_profit'][0]
    title += "最大利润  "+str(max_profit)

    stg01_eE_out = np.array(load_dic['stg01_eE_out'])
    stg01_eE_in = np.array(load_dic['stg01_eE_in'])
    s1_eE_in = np.array(load_dic['s1_eE_in'])
    elecloads_u1 = np.array(load_dic['elecLoads_u1'])
    elecloads_u1 = elecloads_u1 - stg01_eE_out
    data = np.array(load_dic['elecLoads_u1'])
    data2 = np.vstack([elecloads_u1,stg01_eE_in])
    #print(data.shape[0])


    width = 0.5
    color_list = ['#00FF7F', 'b','r','#EE82EE','#FFFF00']
    color_list2 = ['#8B4513','#FF8C00','#8B4513']
    X = np.arange(24)
    #legend = ('chp01_eE_out','chp02_eE_out','pv01_eE_out','stg01_eE_out','s1_eE_out','s1_eE_in','elecLoads_u1','stg01_eE_in')
    #legend = ('CHP1发电量','CHP2发电量','光伏发电量','储能放电量','不足网补电量','余电上网电量','用户总需求电量','储能充电电量')
    legend = ("用户总需求电量-储能放电量","储能","余电上网电量")
    legend2 = ("eleclaod_ul-储能放电量")
    fig = plt.figure(figsize = (12, 4),frameon=False,)
    fig.add_axes([0.07,0.1,0.85,0.83])

    mpl.rcParams['font.sans-serif'] = ['SimHei']
    matplotlib.rcParams['axes.unicode_minus'] = False

    plt.figure(1)
    plt.subplot(211)
    for i in range(data2.shape[0]):  # i表示list的索引值
        plt.bar(X, data2[i],
                width=width,
                bottom=np.sum(data2[:i], axis=0),
                color=color_list[i],
                #hatch="---"
                )
    plt.title(title)
    plt.ylim([0,16000])
    fig.legend(legend, loc="EastOutside")
    plt.subplot(212)
    plt.bar(X, data,
            width=width,
            color=color_list2[0]
            # hatch="\\\\\\\\"
            )
    plt.legend(["用户总需求电量"])
    plt.xlabel("时间(小时)")
    plt.ylabel("功率(千瓦)")
    plt.ylim([0, 16000])
    plt.show()

