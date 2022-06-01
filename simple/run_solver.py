from dis import dis
import os
import sys
import csv
from math import *
import pandas as pd
import numpy as np
from solver import solve

def preprocess(path):
    import csv
    fp = open(path, 'r', newline = '')
    header = fp.readline()
    reader = csv.reader(fp, delimiter = ',') 
    all_data = [[row[i] for i in range(6)] for row in reader]
    return all_data, [[float(row[2]), float(row[3])] for row in all_data], float(all_data[0][5])

def rotate(locations, theta):
    return [[cos(theta) * x - sin(theta) * y, sin(theta) * x + cos(theta) * y] for [x, y] in locations]

def evaluate(locations, distance, facilities):
    eps = 0.001
    def dist(x1, y1, x2, y2):
        return abs(x1 - x2) + abs(y1 - y2)

    for [x1, y1] in locations:
        for [x2, y2] in facilities:
            print(dist(x1, y1, x2, y2), end=' ')
        print()

    all_dists = [min([dist(x1, y1, x2, y2) for [x2, y2] in facilities]) for [x1, y1] in locations]
    max_dist = max(all_dists)
    avg_dist = sum(all_dists) / len(all_dists)
    return max_dist, avg_dist, max_dist <= distance + eps

if __name__ == '__main__':
    datas = sorted(os.listdir('data'))
    result_df = pd.DataFrame(columns = ['Data name', 'Number of facility', 'Max distance'])
    # datas = ['001.csv']

    for data in datas:
        path = 'data/' + data
        all_data, locations, distance = preprocess(path)
        print(locations, distance)
        facilities = rotate(solve(rotate(locations, pi / 4), distance / sqrt(2)), -pi / 4)
        print(facilities)
        max_dist, avg_dist, feasibility = evaluate(locations, distance, facilities)
        result_df = result_df.append({'Data name': data, 
                                      'Number of facility': len(facilities) if feasibility else -1,
                                      'Max distance': max_dist if feasibility else -1,
                                      'Average distance': avg_dist if feasibility else -1}, ignore_index = True)
    result_df.to_csv('result.csv', index = False)







