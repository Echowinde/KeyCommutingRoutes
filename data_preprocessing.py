import numpy as np
import pandas as pd
import os
import datetime


def data_processing(data):
    data.dropna(inplace=True)

    # data in morning and evening peak  06:30-10:30/15:30-21:30
    data['CAP_DATE'] = pd.to_datetime(data['CAP_DATE'], format='%Y/%m/%d %H:%M:%S').dt.time
    morning = data[(data['CAP_DATE'] >= datetime.time(6, 30, 0)) & (data['CAP_DATE'] <= datetime.time(10, 30, 0))]
    night = data[(data['CAP_DATE'] >= datetime.time(15, 30, 0)) & (data['CAP_DATE'] <= datetime.time(21, 30, 0))]

    # remove car plates that were detected less than 3
    counts = morning['CAR_NUM'].value_counts().to_frame().reset_index()
    counts.columns = ['CAR_NUM', 'counts']
    morning = morning.merge(counts, on='CAR_NUM')
    morning = morning[morning['counts'] >= 3]
    morning.drop('counts', axis=1, inplace=True)
    morning.sort_values(by=['CAR_NUM', 'CAP_DATE'], inplace=True)
    
    counts = night['CAR_NUM'].value_counts().to_frame().reset_index()
    counts.columns = ['CAR_NUM', 'counts']
    night = night.merge(counts, on='CAR_NUM')
    night = night[night['counts'] >= 3]
    night.drop('counts', axis=1, inplace=True)
    night.sort_values(by=['CAR_NUM', 'CAP_DATE'], inplace=True)

    del data
    return morning, night


def generate_trip_chain(df):
    car_num = []
    trajectory = []
    time_list = []
    date, loc = [], []
    for i in df.itertuples():
        if not car_num:
            car_num.append(i[1])
        if car_num[-1] != i[1]:
            car_num.append(i[1])
            trajectory.append(loc)
            time_list.append(date)
            date, loc = [], []
        date.append(str(i[2]))
        lng, lat = float(i[3].split(',')[0]), float(i[3].split(',')[1])
        loc.append((lng, lat))
    trajectory.append(loc)
    time_list.append(date)
    return car_num, trajectory, time_list


if __name__ == '__main__':
    path = r'./raw_data'
    file_list = os.listdir(path)
    for file in file_list:
        print(f'---reading：{file}---')
        df = pd.read_csv(os.path.join(path, file), encoding='gbk', engine='python')
        df_morning, df_night = data_processing(df)
        morning_a, morning_b, morning_c = generate_trip_chain(df_morning)
        night_a, night_b, night_c = generate_trip_chain(df_night)
        file_name = os.path.splitext(file)[0]
        np.savez(f'./output/peak_data/{file_name}_morning', CAR_NUM=morning_a, Trajectory=morning_b, Time_list=morning_c)
        np.savez(f'./output/peak_data/{file_name}_night', CAR_NUM=night_a, Trajectory=night_b, Time_list=night_c)
        print(f'---{file} done---')
