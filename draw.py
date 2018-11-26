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


def fig():
	print("KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK")

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



def draw():
    plot_f = open('newjson.json', 'r')
    config = open('config.ini','r')
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
    if flag_price == '1':
        title += "新价格：是  "
    if flag_price == '0':
        title += "新价格：否  "

    load_dic = json.load(plot_f)
    scene_1_value = [load_dic['chp01_eE_out'],load_dic['chp02_eE_out'],load_dic['pv01_eE_out'],load_dic['stg01_eE_out'],load_dic['s1_eE_out']]
    scene_11_value = [load_dic['s1_eE_in'],load_dic['elecLoads_u1'],load_dic['stg01_eE_in']]
    max_profit = "%0.2f" % load_dic['max_profit'][0]
    title += "最大利润  "+str(max_profit)

    width = 0.5
    lens = len(scene_1_value[0])
    index = np.arange(lens)
    data = np.array(scene_1_value)
    data2 = -1*np.array(scene_11_value)
    hight_max_value = np.max(np.sum(data,0),axis=0)+5000
    low_max_value = -(np.max(np.sum(np.array(scene_11_value),0),axis=0)+300)
    color_list = ['#00FF7F', 'b','r','#EE82EE','#FFFF00']
    color_list2 = ['#8B4513','#FF8C00','#8B4513']
    X = np.arange(data.shape[1])
    #legend = ('chp01_eE_out','chp02_eE_out','pv01_eE_out','stg01_eE_out','s1_eE_out','s1_eE_in','elecLoads_u1','stg01_eE_in')
    legend = ('CHP1发电量','CHP2发电量','光伏发电量','储能放电量','不足网补电量','余电上网电量','用户总需求电量','储能充电电量')
    fig = plt.figure(figsize = (12, 4),frameon=False,)
    fig.add_axes([0.07,0.1,0.8,0.83])

    mpl.rcParams['font.sans-serif'] = ['SimHei']
    matplotlib.rcParams['axes.unicode_minus'] = False
    ####  正的
    for i in range(data.shape[0]):  # i表示list的索引值
        #print("+")
        if i == 2:
            plt.bar(X, data[i],
                    width=width,
                    bottom=np.sum(data[:i], axis=0),
                    color=color_list[i],
                    hatch="//////"
                    )
        elif i == 3:
            plt.bar(X, data[i],
                    width=width,
                    bottom=np.sum(data[:i], axis=0),
                    color=color_list[i],
                    hatch="\\\\\\\\"
                    )
        else:
            plt.bar(X, data[i],
                    width=width,
                    bottom=np.sum(data[:i], axis=0),
                    color=color_list[i]
                    )


    ##### 画负的
    for i in range(data2.shape[0]):  # i表示list的索引值
        #print("-")
        if i == 2:
            plt.bar(X, data2[i],
                    width=width,
                    bottom=np.sum(data2[:i], axis=0),
                    color=color_list2[i % len(color_list2)],
                    hatch="---"
                    )
        else:
            plt.bar(X, data2[i],
                    width=width,
                    bottom=np.sum(data2[:i], axis=0),
                    color=color_list2[i % len(color_list2)]
                    )

    #plt.legend(legend)
    plt.ylim([low_max_value,hight_max_value])
    # plt.xlabel("time(h)")
    # plt.ylabel("power(kw)")
    # plt.title("system electric dispatch balance results")
    plt.xlabel("时间(小时)")
    plt.ylabel("功率(千瓦)")
    fig.legend(legend, loc="EastOutside")
    plt.title(title)
    plt.show()

#draw()