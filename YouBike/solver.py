from math import *


def solve(c_loc, c_weight, t_loc, t_weight, dist):

    eps = 0.0001

    # print(c_loc, dist)

    def rotate(locations, theta):
        return [
            [cos(theta) * x - sin(theta) * y, sin(theta) * x + cos(theta) * y]
            for [x, y] in locations
        ]

    def distance(x1, y1, x2, y2):
        rotated = rotate([[x1, y1], [x2, y2]], pi / 4)
        return abs(rotated[0][0] - rotated[1][0]) + abs(rotated[0][1] - rotated[1][1])

    def find_sets(loc, dist):
        def get_center(set, dist):
            # max1 = max2 = max3 = max4 = 0
            # for i in range(len(set)):
            #     [x, y] = set[i]
            #     if x + y > set[max1][0] + set[max1][1]:
            #         max1 = i
            #     if -x + y > -set[max2][0] + set[max2][1]:
            #         max2 = i
            #     if -x - y > -set[max3][0] - set[max3][1]:
            #         max3 = i
            #     if x - y > set[max4][0] - set[max4][1]:
            #         max4 = i
            # dist1 = distance(set[max1][0], set[max1][1], set[max3][0], set[max3][1])
            # dist2 = distance(set[max2][0], set[max2][1], set[max4][0], set[max4][1])
            # if dist1 > dist2:
            #     return [
            #         (set[max1][0] + set[max3][0]) / 2,
            #         (set[max1][1] + set[max3][1]) / 2,
            #     ]
            # else:
            #     return [
            #         (set[max2][0] + set[max4][0]) / 2,
            #         (set[max2][1] + set[max4][1]) / 2,
            #     ]

            xs = [l[0] for l in set]
            ys = [l[1] for l in set]
            return [(min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2]

        dist += eps
        sets = []
        centers = []
        for i in loc:
            for j in loc:
                x, y = i[0] - eps, j[1] - eps
                # print(x, y)
                s = [
                    k
                    for k in range(len(loc))
                    if x <= loc[k][0] <= x + dist * 2 and y <= loc[k][1] <= y + dist * 2
                ]
                if len(s) == 0 or sorted(s) in sets:
                    continue
                sets.append(sorted(s))
                centers.append([x + dist, y + dist])

        sets = sorted(sets)
        centers = [get_center([loc[k] for k in s], dist) for s in sets]

        return sets, centers

    import gurobipy as gp

    c_sum = sum(c_weight)
    t_sum = sum(t_weight)
    c_weight = [100 * w / c_sum for w in c_weight]
    t_weight = [100 * w / t_sum for w in t_weight]
    ppc = 100 / len(c_weight) / len(t_weight)

    sets, centers = find_sets(c_loc, dist)
    # print(sorted(sets))

    model = gp.Model()

    B = range(len(c_loc))  # i
    T = range(len(t_loc))  # j
    S = range(len(sets))  # k

    M = 100000000

    s = [[1 if i in set else 0 for i in B] for set in sets]
    d = [
        [distance(centers[k][0], centers[k][1], t_loc[j][0], t_loc[j][1]) for j in T]
        for k in S
    ]

    c = [model.addVar(0.0, 1.0, 0.0, gp.GRB.BINARY) for k in S]
    cov = [model.addVar(0.0, 1.0, 0.0, gp.GRB.BINARY) for i in B]

    # for i in B:
    #     model.addConstr(sum([c[k] * s[k][i] for k in S]) >= 1)

    for i in B:
        model.addConstr(sum([c[k] * s[k][i] for k in S]) >= 1 * cov[i])
    u = model.addVar(0.0, 10000.0, 0.0, gp.GRB.CONTINUOUS)
    model.addConstr(u == len(c_loc) - sum([cov[i] for i in B]))

    g = [[model.addVar(0.0, 10000.0, 0.0, gp.GRB.CONTINUOUS) for k in S] for i in B]

    z = [[model.addVar(0.0, 10000.0, 0.0, gp.GRB.CONTINUOUS) for j in T] for k in S]

    b = [[model.addVar(0.0, 1.0, 0.0, gp.GRB.BINARY) for j in T] for k in S]

    for i in B:
        model.addConstr(sum([g[i][k] for k in S]) <= c_weight[i] + eps)
        for k in S:
            model.addConstr(g[i][k] <= c[k] * M)
            model.addConstr(g[i][k] <= s[k][i] * M)

    for k in S:
        model.addConstr(sum(b[k]) >= c[k])
        for j in T:
            model.addConstr(z[k][j] <= b[k][j] * M)
            model.addConstr(b[k][j] <= c[k])

    for j in T:
        model.addConstr(sum([z[k][j] for k in S]) >= t_weight[j] - u * ppc - eps)
        model.addConstr(sum([z[k][j] for k in S]) >= eps)

    for k in S:
        model.addConstr(sum([z[k][j] for j in T]) <= sum([g[i][k] for i in B]) + 10 * eps)

    r = [model.addVar(0.0, 10000.0, 0.0, gp.GRB.CONTINUOUS) for j in T]

    for k in S:
        for j in T:
            # r[j] >= d[k][j] if b[k][j] == 1
            model.addConstr(d[k][j] - r[j] <= M * (1 - b[k][j]))

    m = model.addVar(0.0, 10000.0, 0.0, gp.GRB.CONTINUOUS)
    for j in T:
        model.addConstr(m >= r[j])

    # model.addConstr(u == 0)

    w1 = 1
    w2 = 1
    w3 = 1

    model.setObjective(
        w1 * (sum(c) / len(c_loc)) + w2 * (sum(r) / (len(t_loc) * dist * 100)) + w3 * (u / len(c_loc)),
        gp.GRB.MINIMIZE,
    )
    # model.setObjective(w1 * (sum(c) / len(c_loc)) + w3 * (u / len(c_loc)))
    model.optimize()

    # for j in T:
    #     print(t_weight[j] - u.X * ppc)

    facilities = []
    for i in S:
        if c[i].X:
            facilities.append(centers[i])
    # sum_r = 0
    # for j in T:
    #     sum_r += r[j].X
    print(len(facilities), "/", len(c_loc))
    # print(sum_r / len(t_loc) / dist)
    print(u.X, "/", len(c_loc))

    ii = 0
    kk = []
    for k in S:
        kk.append(ii)
        if c[k].X:
            ii += 1

    groups = []
    for j in T:
        group = []
        for k in S:
            if b[k][j].X:
                group.append(kk[k])
        groups.append(group)

    # uncovered = []
    # for i in B:
    #     if u[i].X:
    #         uncovered.append(i)

    return facilities, groups, u.X
