from core.utils import print_4s, print_8s, switch


class build_model():
    def __init__(self, real_path, timelimit, solver=None, mip_start=None, lp_start=None, logging=None,
                 sol=None):
        self.funcName = "build_model"
        self.real_path = real_path
        self.timelimit = timelimit
        self.solver = solver
        self.mip_start = mip_start
        self.lp_start = lp_start
        self.logging = logging
        self.sol = sol

        self.model_header()

    def model_header(self):
        """ print model header """
        print('# real_path: ' + self.real_path)
        print('from pulp import *')
        print('import os')
        print('def dispatch(loads, isOffMap, t_num):')
        print_4s('prob = LpProblem("Multi-Energy Model", LpMaximize)')
        return True

    def model_tail(self):
        print("""
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
    """)
        return True

    def solver_setting(self):
        print("""    
    # pid = os.getpid()
    pid = 'maxProfit'
    tmpLp = os.path.join("data/%s.lp" % pid)
    tmpMps = os.path.join("data/%s.mps" % pid)
    tmpSol = os.path.join("data/%s.sol" % pid)
    glpk_path = 'C:\glpk-4.65\w32\glpsol.exe'
    """)
        print_4s("LpSolverDefault.msg = 0 ") if self.logging else 0
        if self.lp_start:
            # The problem data is written to an .lp file
            print_4s("prob.writeLP(tmpLp)")
            print_4s("prob.writeLP(tmpLp)")
        if self.mip_start:
            print_4s("prob.writeMPS(tmpSol)")
        # prob.writeSol(tmpSol)
        print("""  
    # The problem is solved using PuLP's choice of Solver
    try:""")
        if self.mip_start:
            for case in switch(self.solver):
                if case("CPLEX_CMD"):
                    print_8s("# Solve using CPLEX with logging")
                    print_8s(
                        "prob.solve(" + self.solver + "(timelimit=" + str(self.timelimit) + ", msg=0).readsol(tmpMps))")
                elif case("PULP_CBC_CMD"):
                    print_8s("# Solve using CBC with logging")
                    print_8s("prob.solve(" + self.solver + "(fracGap=0.001"
                                                           ", maxSeconds=" + str(self.timelimit) + ", msg=0))")
                elif case("GLPK"):
                    print_8s("# Solve using GLPK with logging")
                    # print_8s("prob.solve(" + self.solver + "(path=glpk_path, msg=1))")
                    print_8s("prob.solve(" + self.solver + "(msg=0))")
                else:
                    # Solve using PuLP's default Solver (usually CBC)
                    print_8s("prob.solve(maxSeconds=" + str(self.timelimit) + ", msg=0)")
        else:
            for case in switch(self.solver):
                if case("CPLEX_CMD"):
                    print_8s("# Solve using CPLEX with logging")
                    print_8s("prob.solve(" + self.solver + "(timelimit=" + str(self.timelimit) + ", msg=0))")
                elif case("PULP_CBC_CMD"):
                    print_8s("# Solve using CBC with logging")
                    print_8s(
                        "prob.solve(" + self.solver + "(fracGap=0.0001, maxSeconds=" + str(self.timelimit) + ", msg=0))")
                elif case("GLPK"):
                    # print_8s("prob.solve(" + self.solver + "(path=glpk_path, msg=1))")
                    print_8s("# Solve using GLPK with logging")
                    print_8s("prob.solve(" + self.solver + "(msg=0))")
                else:
                    # Solve using PuLP's default Solver (usually CBC)
                    print_8s("prob.solve(maxSeconds=" + str(self.timelimit) + ", msg=0)")
        print("""        # prob.solve(GUROBI_CMD()) # Solve using Gurobi
        # prob.solve(COIN_CMD(msg=0))
    except Exception:
        print('Solver infeasible, check please!!!')
        return False
        """)
        # if sol is True, output result
        self.model_tail() if self.sol else None
        return True
