import json
import sklearn.cluster as skc
import copy
import numpy as np
import os


def get_eps(mat):
    """
    get the best eps
    :param mat:
    :return:
    """
    dist = copy.deepcopy(mat)
    dist = np.sort(dist)
    eps_array = dist.sum(axis=0)  # 对二维矩阵按列求和
    eps_array = eps_array / len(eps_array)
    return eps_array[1]


def get_MinPts(mat, eps):
    """
    get the best MinPts
    :param mat:
    :param eps:
    :return:
    """
    dist = copy.deepcopy(mat)
    length = len(dist[np.where(dist <= eps)])
    MinPts = length / len(dist)
    MinPts = round(MinPts)
    return MinPts


def get_cluster_data(mat):
    """
    use DBSCAN to find key routes
    :param mat:
    :return:
    """
    data = []
    sample_CAR_NUM = mat['sample_CAR_NUM']
    sample_Trajectory = mat['sample_Trajectory']
    WMM = mat['WMM']

    eps = get_eps(WMM)
    minpts = get_MinPts(WMM, eps)
    print("eps:{:.3f}, MinPts:{}".format(eps, minpts))

    # use WMM itself as matric
    db = skc.DBSCAN(eps=eps, min_samples=minpts, metric='precomputed').fit(WMM)  # DBSCAN object
    labels = db.labels_
    clusters = np.bincount(labels[labels > -1])  # remove noises

    cluster_id = np.argsort(clusters)[-5:]
    cluster_sample_num = np.sort(clusters)[-5:]
    # cluster and corresponding sample num
    print(dict(zip(cluster_id, cluster_sample_num)))

    for idx in cluster_id:
        cluster_car = sample_CAR_NUM[labels == idx]
        cluster_path = sample_Trajectory[labels == idx]
        cluster_data = {'date': file_name, 'cluster': int(idx), 'car_num': cluster_car, 'path': cluster_path}
        data.append(cluster_data)

    return data


if __name__ == "__main__":

    path = r'./output/DTW'
    file_list = os.listdir(path)
    output = dict()
    for file in file_list:
        print(f'---reading：{file}---')
        file_name = os.path.splitext(file)[0]
        matrix = np.load(os.path.join(path, file), allow_pickle=True)
        data = get_cluster_data(matrix)
        output[file_name] = data

    with open(r'./output/cluster_result.json', 'w') as f:
        f.write(json.dumps(output))
