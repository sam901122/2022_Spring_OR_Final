def solve(locations, distance):
    import gurobipy as gp
    model = gp.Model()

    # print(locations, distance)

    B = range(len(locations))
    d = distance
    M = 10000000.0
    x = [l[0] for l in locations]
    y = [l[1] for l in locations]

    x_range = max(x) - min(x)
    x_min, x_max = min(x) - x_range, max(x) + x_range
    y_range = max(y) - min(y)
    y_min, y_max = min(y) - y_range, max(y) + y_range

    a = [model.addVar(x_min, x_max, 0.0, gp.GRB.CONTINUOUS) for i in B]
    b = [model.addVar(y_min, y_max, 0.0, gp.GRB.CONTINUOUS) for i in B]
    s = [[model.addVar(0.0, 1.0, 0.0, gp.GRB.BINARY) for j in B] for i in B]
    u = [model.addVar(0.0, 1.0, 0.0, gp.GRB.BINARY) for i in B]

    for i in B:
        model.addConstr(sum(s[i]) >= 1)

    for i in B:
        for j in B:
            model.addConstr(x[i] - d - a[j] <= M * (1 - s[i][j]))
            model.addConstr(a[j] - x[i] - d <= M * (1 - s[i][j]))
            model.addConstr(y[i] - d - b[j] <= M * (1 - s[i][j]))
            model.addConstr(b[j] - y[i] - d <= M * (1 - s[i][j]))

    for j in B:
        model.addConstr(sum([s[i][j] for i in B]) <= M * u[j])

    model.setObjective(sum(u), gp.GRB.MINIMIZE)
    model.optimize()

    min_facility_cnt = model.getObjective().getValue()
    # print("min facility count:", min_facility_cnt)
    # for i in B:
    #     for j in B:
    #         print(s[i][j].X, end=' ')
    #     print()
    # facilities = []
    # for i in B:
    #     print(u[j].X, end=' ')
    # print()

    facilities = []
    for j in B:
        if u[j].X:
            facilities.append([a[j].X, b[j].X])
            # print(a[j].X, b[j].X)
    return facilities

def preprocess(path):
    import csv
    fp = open(path, 'r', newline = '')
    header = fp.readline()
    reader = csv.reader(fp, delimiter = ',') 
    all_data = [[row[i] for i in range(6)] for row in reader]
    return all_data, [[float(row[2]), float(row[3])] for row in all_data], float(all_data[0][5])

from math import *

def rotate(locations, theta):
    return [[cos(theta) * x - sin(theta) * y, sin(theta) * x + cos(theta) * y] for [x, y] in locations]

if __name__ == '__main__':
    import sys
    path = sys.argv[1]
    all_data, locations, distance = preprocess(path)
    solve(rotate(locations, pi / 4), distance / (2 ** 1/2))