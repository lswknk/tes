import os
from core.utils import *
from core.build_model import build_model
from core.objective import *
from core.Connection import connect_forward, connect_backward


class EnergyHub(object):
    """
    Create a class of EnergyHubs. An energy hub contains sources, devices and users.
    """

    def __init__(self, source=None, devices=None, user=None, topology=None,
                 onoffmap=None, loads=None):
        self.source = {}
        self.devices = {}
        self.user = {}
        self.allDevices = {}
        self.onOffMap = {}
        self.topology = {}
        self.backTopology = {}
        self.loads = loads
        self.gapTime = 3600  # 3600 seconds = 1 hour
        self.t_num = 0
        # self.model["gapTime"] = 3600
        # self.model["solver"] = 'CPLEX_CMD'
        # self.solver = 'GLPK'
        self.solver = 'CPLEX_CMD'
        # self.solver = 'PULP_CBC_CMD'
        self.mip_start = False
        self.lp_start = False
        self.logging = False
        self.sol = True
        self.objective = 'maxProfit'
        self.real_path = os.path.dirname(os.path.realpath(__file__))

        for item in self.loads.values():
            for val in item.values():
                self.t_num = max(self.t_num, len(val))

        # self.subTopology, self.subBackTopology, self.source, self.devices, self.onOffMap
        self.extractSubTopology(source, devices, user, topology, onoffmap)

    def run(self):
        print_4s('aList = [i for i in range(t_num)]')
        print('')

        # sources
        print_4s('# sources')
        for item in self.source.keys():
            self.source[item].output_variables = list(set(self.source[item].output_variables))
            self.source[item].input_variables = list(set(self.source[item].input_variables))
            self.source[item].run()

        # devices
        print(u'    # devices')
        for item in self.devices.keys():
            self.devices[item].run()

        # user
        print(u'    # user')
        for item in self.user.keys():
            self.user[item].input_variables = list(set(self.user[item].input_variables))
            self.user[item].output_variables = list(set(self.user[item].output_variables))
            self.user[item].run()

        # connections
        print(u'    # forward topology')
        for item, subDevices in self.topology.items():
            toDevices = []
            for temp in subDevices:
                toDevices.append(self.allDevices[temp])
            connect_forward(fromUnit=self.allDevices[item[0]], toUnits=toDevices, type=item[1])
        print('')
        print(u'    # backward topology')
        for item, supDevices in self.backTopology.items():
            fromDevices = []
            for temp in supDevices:
                fromDevices.append(self.allDevices[temp])
            connect_backward(fromUnits=fromDevices, toUnit=self.allDevices[item[0]], type=item[1])

    def solve(self):
        # open file 'model.py', a file to save all outputs.
        file = File(self.real_path)
        fileName, output = file.open()
        model = build_model(self.real_path, self.gapTime, solver=self.solver, mip_start=self.mip_start,
                            lp_start=self.lp_start, logging=self.logging, sol=self.sol)
        # load all devices constraints
        self.run()
        # objective
        deviceInstances = tuple(self.devices.values())
        if self.objective == 'maxProfit' or self.objective == 'minCost':
            maxProfit(self.t_num, tuple(self.source.values()), self.user, deviceInstances, self.loads)
        """ solver setting (to model.py) """
        model.solver_setting()
        file.close(fileName, output)

        # model warm start
        try:
            from core.model import dispatch
            dispatch(self.loads, self.onOffMap, self.t_num)
        except ImportError:
            print("file %s import Error" % fileName)
            return False

    def extractSubTopology(self, source, devices, user, topology, onoffmap):
        backTopology = {}
        for item in topology:
            for element in item[2]:
                if backTopology.get((element, item[1]), None):
                    backTopology[(element, item[1])] = backTopology[(element, item[1])].union({item[0], })
                else:
                    backTopology[(element, item[1])] = {item[0], }

        position = set()
        for item, value in self.loads.items():
            itemName = item.replace('Loads', '')
            for userid in value.keys():
                user[userid].input_variables.append(itemName)
                if itemName == 'elec':
                    user[userid].output_variables.append(itemName)
                position = position.union({(userid, itemName), })
                self.user[userid] = user[userid]

        self.subGraph(position, backTopology, source, devices, onoffmap)
        # update self.topology, self.allDevices
        for item, value in self.backTopology.items():
            for element in value:
                if self.topology.get((element, item[1]), None):
                    self.topology[(element, item[1])] = self.topology[(element, item[1])].union({item[0], })
                else:
                    self.topology[(element, item[1])] = {item[0], }
        # update self.allDevices
        self.allDevices.update(self.user)
        self.allDevices.update(self.devices)
        self.allDevices.update(self.source)
        for key, val in self.allDevices.items():
            for name in val.output_variables:
                if not self.topology.get((key, name), None):
                    self.topology[(key, name)] = set()

    def subGraph(self, position, backTopology, source, devices, onoffmap):
        parent = set()
        gone = set()
        for item in position:
            self.backTopology[item] = self.backTopology.get(item, set()).union(backTopology.get(item, set()))
            gone = gone.union({item[0], })
            if backTopology.get(item, None):
                for p_item in backTopology[item]:
                    if p_item not in gone and p_item not in source.keys() and p_item not in self.user.keys():
                        self.devices[p_item] = devices[p_item]
                        self.onOffMap[p_item] = onoffmap[p_item]
                        for var in devices[p_item].input_variables:
                            parent = parent.union({(p_item, var)})
                        gone = gone.union({p_item, })
                    if p_item in source.keys():
                        self.source[p_item] = source[p_item]
                        self.source[p_item].output_variables.append(item[1])
                        if item[1] == 'elec':
                            self.source[p_item].input_variables.append(item[1])
                        for var in source[p_item].input_variables:
                            parent = parent.union({(p_item, var)})
                    if p_item in self.user.keys():
                        continue

        if parent:
            self.subGraph(parent, backTopology, source, devices, onoffmap)
