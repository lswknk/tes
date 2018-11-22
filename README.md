# Optimizer based on ehub model provided by ENN

09/12/2018
->改进:
    1.批量的import module 移入classes.py，以from core.classes import *实现；
    2.函数化model.py的函数头及solver设置， 暂存于utils.py;
    3.增加__init__.py;
    4.计算内核改用CPLEX_CMD，求解效率比cbc高；
    ==================================================================================
    # The problem is solved using PuLP's choice of Solver
    try:
        prob.solve(CPLEX_CMD(timelimit=500, msg=1))
    except Exception:
        print('Problem infeasible, check model please!!!')

    # prob.solve(PULP_CBC_CMD(fracGap = 0.001, maxSeconds = 500, threads = None, msg=1))
    # prob.solve(GLPK(path='glpsol',msg = 1))
    # prob.solve()    # Solve using PuLP's default Solver (usually CBC)
    # prob.solve(GUROBI_CMD()) # Solve using Gurobi
    # prob.solve(COIN_CMD(msg=1)) # Solve using CBC with logging
    ==================================================================================
->修复：
    1.Photovoltaic拼写错误；


09/13/2018

    LP/MILP_Solver support:
        1. Three solvers are available: 
            CPLEX:IBM(R) ILOG(R) CPLEX(R) Interactive Optimizer 12.6.3.0
                  with Simplex, Mixed Integer & Barrier Optimizers
            cbc(COIN-OR Branch and Cuts);
            GLPK(LP/MIP Solver, v4.65), path must be configured


class COIN_CMD(LpSolver_CMD):
    """The COIN CLP/CBC LP solver now only uses cbc """

    def defaultPath(self):
        return self.executableExtension(cbc_path)

    def __init__(self, path = None, keepFiles = 0, mip = 1,
            msg = 0, cuts = None, presolve = None, dual = None,
            strong = None, options = [],
            fracGap = None, maxSeconds = None, threads = None)

    
09/14/2018
    1. fix bug of Storage
    2. add print_4s(Object), print_8s(Object) to utils.py
    
09/17/2018
    1. linear.py -> class SOS():    addSOS1, addSOS2.
    2. add class File() to utils.py.
    3. dynamic price.
    4. not output auxiliary variables. 
    5. rename HeatRecoverySteamGenerator.


"""
flag_pv= 0 无光伏   1 有光伏
flag_stg = 0 无储能  1 有储能
flag_good =0 好的   1 不好的
flag_price = 0 旧价格  1 新价格
scene =0 flag_pv=0 flag_stg =0 flag_good=0 flag_price =0
scene =1 flag_pv=1 flag_stg =0 flag_good=0 flag_price =0
scene =2 flag_pv=1 flag_stg =1 flag_good=0 flag_price =0
scene =3 flag_pv=0 flag_stg =0 flag_good=1 flag_price =0
scene =4 flag_pv=1 flag_stg =0 flag_good=1 flag_price =0
scene =5 flag_pv=1 flag_stg =1 flag_good=1 flag_price =0

scene =6 flag_pv=0 flag_stg =0 flag_good=0 flag_price =1
scene =7 flag_pv=1 flag_stg =0 flag_good=0 flag_price =1
scene =8 flag_pv=1 flag_stg =1 flag_good=0 flag_price =1
scene =9 flag_pv=0 flag_stg =0 flag_good=1 flag_price =1
scene =10 flag_pv=1 flag_stg =0 flag_good=1 flag_price =1
scene =11 flag_pv=1 flag_stg =1 flag_good=1 flag_price =1
"""