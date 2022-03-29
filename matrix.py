import numpy as np
from sklearn import manifold
import DTW
import random
import os
import copy


def cal_DTW_matrix(df):

    CAR_NUM = df['CAR_NUM']
    Trajectory = df['Trajectory']
    Time_list = df['Time_list']

    length = len(CAR_NUM)
    ranindex = random.sample(range(0, length), 5000)  # 5000 samples
    ranindex.sort()
    sample_CAR_NUM = CAR_NUM[ranindex]  # sample car plates
    sample_Trajectory = Trajectory[ranindex]  # sample car trajectories
    sample_Time = Time_list[ranindex]  # sample car time series

    # calculate DTW matrix
    length = len(sample_CAR_NUM)
    dis_DTW = np.zeros((length, length))  # DTW matrix of trajectories
    time_DTW = np.zeros((length, length))  # DTW matrix of time series
    for i in range(length):
        for j in range(i, length):
            temp_dis_DTW = DTW.dynamic_timewarp(sample_Trajectory[i], sample_Trajectory[j], DTW.get_distance)
            temp_time_DTW = DTW.dynamic_timewarp(sample_Time[i], sample_Time[j], DTW.get_dis_of_timeseries)
            dis_DTW[i][j] = temp_dis_DTW
            time_DTW[i][j] = temp_time_DTW
    temp_t = dis_DTW.transpose()
    dis_DTW = dis_DTW + temp_t
    temp_t = time_DTW.transpose()
    time_DTW = time_DTW + temp_t
    for i in range(length):
        dis_DTW[i][i] = dis_DTW[i][i] / 2
        time_DTW[i][i] = time_DTW[i][i] / 2

    # processing of dist_DTW
    dis_DTW_copy = copy.deepcopy(dis_DTW)
    median_row = np.median(dis_DTW_copy, axis=1)  # get the row median
    for index in range(len(median_row)):
        dis_DTW_copy[index][dis_DTW_copy[index] >= median_row[index]] = median_row[index]
    dis_DTW_copy = (dis_DTW_copy + dis_DTW_copy.T) / 2
    dis_DTW_copy = dis_DTW_copy / np.max(dis_DTW_copy)

    # processing of time_DTW
    time_DTW_copy = copy.deepcopy(time_DTW)
    median_row = np.median(time_DTW_copy, axis=1)
    for index in range(len(median_row)):
        time_DTW_copy[index][time_DTW_copy[index] >= median_row[index]] = median_row[index]
    time_DTW_copy = (time_DTW_copy + time_DTW_copy.T) / 2
    time_DTW_copy = time_DTW_copy / np.max(time_DTW_copy)

    # weighted dist-time mixed matrix
    alpha = 0.5
    WMM = (alpha * dis_DTW_copy + (1 - alpha) * time_DTW_copy)

    return sample_CAR_NUM, sample_Trajectory, sample_Time, dis_DTW_copy, time_DTW_copy, WMM


def cal_MDS_matrix(dis_DTW, time_DTW, WMM):

    mds = manifold.MDS(n_components=2, metric=True, n_init=4, max_iter=500, verbose=0,
                       eps=0.001, n_jobs=1, random_state=None, dissimilarity='precomputed')

    dis_DTW_tran = mds.fit_transform(dis_DTW)
    time_DTW_tran = mds.fit_transform(time_DTW)
    WMM_tran = mds.fit_transform(WMM)

    return dis_DTW_tran, time_DTW_tran, WMM_tran


if __name__ == "__main__":
    path = r'./output/peak_data'
    file_list = os.listdir(path)
    for file in file_list:
        print(f'---reading：{file}---')
        df = np.load(os.path.join(path, file))
        file_name = os.path.splitext(file)[0]

        sample_CAR_NUM, sample_Trajectory, sample_Time, dis_DTW, time_DTW, WMM = cal_DTW_matrix(df)
        np.savez(f'./output/DTW/{file_name}.npz', sample_CAR_NUM=sample_CAR_NUM, sample_Trajectory=sample_Trajectory,
                 sample_Time=sample_Time, dis_DTW=dis_DTW, time_DTW=time_DTW, WMM=WMM)

        # dimension reduction of DTW matrix for visualizing (if needed)
        """
        dis_DTW_tran, time_DTW_tran, WMM_tran = cal_MDS_matrix(dis_DTW, time_DTW, WMM)
        np.savez(f'./output/MDS/{file_name}.npz', sample_CAR_NUM=sample_CAR_NUM, sample_Trajectory=sample_Trajectory,
                 sample_Time=sample_Time, dis_DTW_tran=dis_DTW_tran, time_DTW_tran=time_DTW_tran, WMM_tran=WMM_tran)
        """