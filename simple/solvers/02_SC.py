import gurobipy as gp
import pandas as pd
from math import *

ALLOW_EP = True
EPSILON = 0.0001


def rotate( locations, theta ):
    return [ [ cos( theta ) * x - sin( theta ) * y, sin( theta ) * x + cos( theta ) * y ] for [ x, y ] in locations ]


class Location:

    def __init__( self, id: int, x: float, y: float ) -> None:
        self.id = id
        self.x = x
        self.y = y

    def __str__( self ) -> str:
        return f'id: {self.id}, ( {self.x}, {self.y} )'


def find_set( locations, distance ):
    listOfSets = list()
    setCenterLocations = list()
    locationList = []
    for i in range( len( locations ) ):
        locationList.append( Location( i, locations[ i ][ 0 ], locations[ i ][ 1 ] ) )

    xList = sorted( set( [ l[ 0 ] for l in locations ] ) )
    for startX in xList:
        endX = startX + 2*distance
        if ALLOW_EP == True:
            startX = startX - EPSILON
            endX = endX + EPSILON
        tempLocList = []
        for loc in locationList:
            if startX <= loc.x <= endX:
                tempLocList.append( loc )

        tempYList = sorted( set( [ loc.y for loc in tempLocList ] ) )

        for startY in tempYList:
            endY = startY + 2*distance
            if ALLOW_EP == True:
                startY = startY - EPSILON
                endY = endY + EPSILON
            inBlockSet = set()

            for loc in locationList:
                if ( startX <= loc.x <= endX ) and ( startY <= loc.y <= endY ):
                    inBlockSet.add( loc )

            if tuple( inBlockSet ) not in listOfSets:
                listOfSets.append( tuple( inBlockSet ) )

                xMax = max( inBlockSet, key=lambda loc: loc.x ).x
                xMin = min( inBlockSet, key=lambda loc: loc.x ).x
                yMax = max( inBlockSet, key=lambda loc: loc.y ).y
                yMin = min( inBlockSet, key=lambda loc: loc.y ).y

                centerX = ( xMax+xMin ) / 2
                centerY = ( yMax+yMin ) / 2
                setCenterLocations.append( ( centerX, centerY ) )

    return listOfSets, setCenterLocations, locationList


def solve( locations, distance ):

    listOfSets, setCenterLocations, locationList = list( find_set( locations, distance ) )

    # Model
    sc_model = gp.Model()

    # Sets
    S = range( len( listOfSets ) )
    L = range( len( locations ) )

    # Parameters
    w = []
    for l in L:
        w.append( [] )
        for s in S:
            w[ l ].append( int( locationList[ l ] in listOfSets[ s ] ) )

    # Decision variables
    c = [ sc_model.addVar( vtype=gp.GRB.BINARY ) for s in S ]

    # Objective function
    sc_model.setObjective( sum( c ), gp.GRB.MINIMIZE )

    # Constraints
    for l in L:
        sc_model.addConstr( gp.quicksum( w[ l ][ s ] * c[ s ] for s in S ) >= 1 )

    # optimize
    sc_model.optimize()

    # result
    facilities = []
    for i in range( len( c ) ):
        if c[ i ].x == 1:
            facilities.append( [ setCenterLocations[ i ][ 0 ], setCenterLocations[ i ][ 1 ] ] )

    return facilities


def debug() -> None:
    df = pd.read_csv(
        'C:\\PuSung\\University\\Sophomore\\110-2 Academic\\OR\\2022_Spring_OR_Final\\simple\\data\\006.csv' )
    x = df[ 'x' ]
    y = df[ 'y' ]
    distance = df[ 'distance' ][ 0 ]
    locations = []
    for i in range( len( x ) ):
        locations.append( [ x[ i ], y[ i ] ] )
    print( solve( rotate( locations, pi / 4 ), distance / sqrt( 2 ) ) )
    return


if __name__ == '__main__':
    debug()