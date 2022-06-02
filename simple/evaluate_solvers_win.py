import os

# solvers = sorted( os.listdir( 'solvers' ) )[ 1: ]
# os.system( 'copy solvers/02_SC.py solver.py' )
os.system( 'python run_solver.py' )
os.system( 'move result.csv results/02_SC_result.csv' )
