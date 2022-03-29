from math import cos, asin, sqrt


def get_distance(point1, point2):
    """
    haversine formula
    :param point1:
    :param point2:
    :return:
    """
    # some constants
    EARTH_REDIUS = 6378.137
    P = 0.017453292519943295  # PI/180

    lng1 = point1[0]
    lat1 = point1[1]
    lng2 = point2[0]
    lat2 = point2[1]
    a = 0.5 - cos((lat2 - lat1) * P)/2 + cos(lat1 * P) * cos(lat2 * P) * (1 - cos((lng2 - lng1) * P)) / 2
    s = 2 * EARTH_REDIUS * asin(sqrt(a))  # unit:km
    return s


def get_dis_of_timeseries(Time1 , Time2):
    """
    calculate the distance between two timestamps
    :param Time1:
    :param Time2:
    :return:
    """
    time12sec = int(Time1[0:2]) * 3600 + int(Time1[3:5]) * 60 + int(Time1[6:8])
    time22sec = int(Time2[0:2]) * 3600 + int(Time2[3:5]) * 60 + int(Time2[6:8])
    dis = abs(time12sec - time22sec)
    return dis


def calc_dist(x, y):
    """
    the distance between two node in the time series
    :param x:
    :param y:
    :return:
    """
    # if the node is a list
    if type(x) == 'list':
        length = len(x)
        s = 0
        for i in range(length):
            s = s + (x[i]-y[i])*(x[i]-y[i])
        return sqrt(s)
    else:  # the node is just a number
        return abs(x-y)


def dynamic_timewarp(seq_a, seq_b, d):
    """
    DP return the distance
    :param seq_a:
    :param seq_b:
    :param d: distance calculate function
    :return:
    """

    # if seq_a or seq_b is None, then return the DTW result is 0
    if seq_a is None or seq_b is None:
        return float("inf")

    # create the cost matrix
    numRows, numCols = len(seq_a), len(seq_b)
    if numRows == 0 or numCols == 0:
        return 0
    cost = [[0 for _ in range(numCols)] for _ in range(numRows)]   # 距离矩阵

    # record father
    fa = [[(0, 0) for _ in range(numCols)] for _ in range(numRows)]   # cost矩阵每个元素的父节点

    # initialize the first row and column
    cost[0][0] = 2 * d(seq_a[0], seq_b[0])
    for i in range(1, numRows):
        cost[i][0] = cost[i - 1][0] + d(seq_a[i], seq_b[0])  # initialize col 0
        fa[i][0] = (i-1, 0)   # save father node

    for j in range(1, numCols):
        cost[0][j] = cost[0][j - 1] + d(seq_a[0], seq_b[j])   # initialize row 0
        fa[0][j] = (0, j-1)   # save father node

    # initialize the sigma w, which is length of the path, note that length of diagonal path is 2
    Sumw = 0

    # fill in the rest of the matrix
    for i in range(1, numRows):
        for j in range(1, numCols):
            # choices = cost[i - 1][j], cost[i][j - 1], cost[i - 1][j - 1]
            # cost[i][j] = min(choices) + d(seq_a[i], seq_b[j])
            if cost[i-1][j] < cost[i][j-1]:
                # cost[i-1][j] is the lowest of former path
                if cost[i-1][j] + d(seq_a[i], seq_b[j]) < cost[i-1][j-1] + 2 * d(seq_a[i], seq_b[j]):
                    cost[i][j] = cost[i-1][j] + d(seq_a[i], seq_b[j])
                    fa[i][j] = (i-1, j)
                # cost[i-1][j-1] is the lowest of former path
                else:
                    cost[i][j] = cost[i - 1][j-1] + 2 * d(seq_a[i], seq_b[j])
                    fa[i][j] = (i-1, j-1)
            else:
                # cost[i][j-1] is the lowest of former path
                if cost[i][j-1] + d(seq_a[i], seq_b[j]) < cost[i-1][j-1] + 2 * d(seq_a[i], seq_b[j]):
                    cost[i][j] = cost[i][j-1] + d(seq_a[i], seq_b[j])
                    fa[i][j] = (i, j-1)
                # cost[i-1][j-1] is the lowest of former path
                else:
                    cost[i][j] = cost[i - 1][j - 1] + 2 * d(seq_a[i], seq_b[j])
                    fa[i][j] = (i-1, j-1)

    # show the cost matrix
    """
    print("cost matrix:")
    for row in cost:
        for entry in row:
            print ("%.2f " % entry, end="")
        print("\n")
    """

    path = []
    i = numRows - 1
    j = numCols - 1
    path.append((i, j))  # add the last node
    while i != 0 or j != 0:
        tempi = i
        tempj = j
        i, j = fa[i][j]
        path.append((i, j))
        if (tempi == i + 1) & (tempj == j + 1):
            Sumw = Sumw + 2
        else:
            Sumw += 1

    # show the path
    """
    print("path:")
    for cord in path[::-1]:
        print(cord, ' ', end="")
        print("\n")
    """

    return cost[-1][-1] / Sumw   # the DTW distance of the two sequences


def test():

    # test - distance of two paths
    # Situation 1: two paths are the same
    seq_a = [(120.1, 30.2), (120.2, 30.4), (120.4, 30.1), (120.6, 30.0)]
    seq_b = [(120.1, 30.2), (120.2, 30.4), (120.4, 30.1)]
    dist = dynamic_timewarp(seq_a, seq_b, get_distance)
    print(dist)

    # Situation 2: two paths are the same, but one misses some point
    seq_a = [(120.1, 30.2), (120.4, 30.5), (121.7, 30.8)]
    seq_b = [(120.1, 30.2), (120.3, 30.4), (120.5, 30.6), (121.7, 30.8)]
    dist = dynamic_timewarp(seq_a, seq_b, get_distance)
    print(dist)

    # Situation 3: one path is None
    seq_a = [(120.1, 30.2), (120.2, 30.4), (120.4, 30.1), (120.6, 30.0)]
    seq_b = None
    dist = dynamic_timewarp(seq_a, seq_b, get_distance)
    print(dist)

    # test - distance of two time series
    seq_a = ['08:07:17', '09:22:30', '14:08:12', '14:12:45']
    seq_b = ['08:07:17', '09:22:30', '14:08:12']
    dist = dynamic_timewarp(seq_a, seq_b, get_dis_of_timeseries)
    print(dist)


if __name__ == "__main__":
    test()
