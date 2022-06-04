import os

solver = sorted( os.listdir( 'solvers' ) )[ 0 ]
'''
for solver in solvers:
    os.system( 'copy solvers\\{} .\\solver.py'.format( solver ) )
    os.system( 'python run_solver.py' )
    os.system( 'move result.csv results\\{}_result.csv'.format( solver[ :-3 ] ) )
'''

os.system( 'copy solvers\\{} .\\solver.py'.format( solver ) )
os.system( 'python run_solver.py' )
os.system( 'move result.csv results\\{}_result.csv'.format( solver[ :-3 ] ) )
