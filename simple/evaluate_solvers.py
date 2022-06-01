#!/bin/python3

import os

solvers = sorted(os.listdir('solvers'))
for solver in solvers:
    os.system('cp solvers/{} ./solver.py'.format(solver))
    os.system('python3 run_solver.py')
    os.system('mv result.csv results/{}_result.csv'.format(solver[:-3]))