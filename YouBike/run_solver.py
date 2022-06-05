from math import *
import pandas as pd
import numpy as np
from solver import solve


def preprocess(path):
    import csv

    fp = open(path, "r", newline="")
    header = fp.readline()
    reader = csv.reader(fp, delimiter=",")
    all_data = [[row[i] for i in range(6)] for row in reader]
    return (
        all_data,
        [[float(row[2]), float(row[3])] for row in all_data],
        [float(row[4]) for row in all_data],
        float(all_data[0][5]),
    )


def rotate(locations, theta):
    return [
        [cos(theta) * x - sin(theta) * y, sin(theta) * x + cos(theta) * y]
        for [x, y] in locations
    ]

def match(c_all, c_loc, c_weight, t_loc, dist):
    c_all_new = []
    c_loc_new = []
    c_weight_new = []
    for i in range(len(c_loc)):
        c = c_loc[i]
        a = True
        for t in t_loc:
            if abs(c[0] - t[0]) + abs(c[1] - t[1]) <= dist:
                a = False
                print("match {} to {}".format(c_all[i][1], t))
                break
        if a:
            c_all_new.append(c_all[i])
            c_loc_new.append(c)
            c_weight_new.append(c_weight[i])
    return c_all_new, c_loc_new, c_weight_new


def evaluate(c_all, t_all, distance, facilities, groups, uncovered):
    eps = 0.001

    def dist(x1, y1, x2, y2):
        return abs(x1 - x2) + abs(y1 - y2)

    c_loc = [[float(row[2]), float(row[3])] for row in c_all]
    t_loc = [[float(row[2]), float(row[3])] for row in t_all]

    all_dists = [
        min([dist(x1, y1, x2, y2) for [x2, y2] in facilities]) for [x1, y1] in c_loc
    ]
    max_dist = max(all_dists)
    avg_dist = sum(all_dists) / len(all_dists)
    real_uncovered = len([d for d in all_dists if d > distance - eps])

    r = []
    for j in range(len(t_all)):
        [tx, ty] = t_loc[j]
        max_group_dist = 0
        for k in groups[j]:
            max_group_dist = max(max_group_dist, dist(tx, ty, facilities[k][0], facilities[k][1]))
        r.append(max_group_dist)
    
    print("stations:")
    for i in range(len(facilities)):
        print("{}\t({},\t{})".format(i + 1, round(facilities[i][0], 5), round(facilities[i][1], 5)))

    print("groups:")
    for j in range(len(t_loc)):
        print("group {} ({}):".format(j + 1, t_all[j][1]))
        for k in groups[j]:
            print("\tstation {}\t({},\t{})".format(k + 1, round(facilities[i][0], 5), round(facilities[i][1], 5)))

    print("number of stations:", len(facilities))
    print("average distance: {}".format(sum(r) / len(t_loc)))
    print("uncovered: {}".format(uncovered))

    return max_dist, avg_dist, max_dist <= distance + eps


if __name__ == "__main__":
    c_path, t_path = "OR_cpoints.csv", "OR_tpoints.csv"

    c_all, c_loc, c_weight, dist = preprocess(c_path)
    t_all, t_loc, t_weight, _ = preprocess(t_path)
    c_all, c_loc, c_weight = match(c_all, c_loc, c_weight, t_loc, dist)

    c_loc = rotate(c_loc, pi / 4)
    t_loc = rotate(t_loc, pi / 4)

    # facilities, groups, uncovered = solve(c_loc, c_weight, t_loc, t_weight, dist / sqrt(2))
    facilities, groups, uncovered = solve(c_loc, c_weight, t_loc, t_weight, dist / sqrt(2))
    facilities = rotate(facilities, -pi / 4)

    evaluate(c_all, t_all, dist, facilities, groups, uncovered)
    # evaluate(c_all, t_all, c_loc, t_loc, dist, facilities, groups, uncovered)
    # max_dist, avg_dist, fea = evaluate(rotate(c_loc, -pi / 4), dist, facilities)
    # print(max_dist, avg_dist, fea)
    # result_df = result_df.append(
    #     {
    #         "Data name": data,
    #         "Number of facility": len(facilities) if feasibility else -1,
    #         "Max distance": max_dist if feasibility else -1,
    #         "Average distance": avg_dist if feasibility else -1,
    #     },
    #     ignore_index=True,
    # )
    # result_df.to_csv("result.csv", index=False)
