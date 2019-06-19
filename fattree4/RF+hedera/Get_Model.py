import pandas as pd
from sklearn.externals import joblib
import os
import sys
import numpy as np
import random
import operator
import math
from pandas import concat

model = joblib.load('model/KMeans_model.m')

dir_prefix = "D:/HaiWen/forecast_flow_size2/forecast_flow_size/flux/data/ml/"
random.seed(0)

thres = [100000]

thresNum = 2
feature_frac = list()
frac_num = 32

WINDOW_SIZE = 5

# TEST_NAME = 'PageRank'
TEST_NAME = 'KMeans'
# TEST_NAME = 'SGD'
# TEST_NAME = 'tensorFlow'
# TEST_NAME = 'web_server'

TARGET_COLUMN = 'flow_size'
TEST_PATH = 'D:/HaiWen/forecast_flow_size2/forecast_flow_size/flux/data/ml/' + TEST_NAME + '/test/'

def calculate_scaling(training_paths):
    scaling = {}
    #calculate scaling factors
    for f in training_paths:
        df = pd.read_csv(f, index_col=False)

        for column in df.columns:
            if column not in scaling:
                scaling[column] = 0.
            scaling[column] = max(scaling[column], float(df[column].max()))
    return scaling

def prepare_files(files, window_size, scaling, target_column='flow_size'):
    result = []
    time = []

    for f in files:
        df = pd.read_csv(f, index_col=False)
        time.append(df['time'])
        df = df.drop("index", axis=1)
        flow_size = df[target_column]
        df = df.apply((lambda x: resize(x, scaling)), axis=0)
        
        df[target_column] = flow_size
        #extend the window
        columns = list(df)
        final_df = df.copy()
        for sample_num in range(1, window_size):
            shifted = df.shift(sample_num)
            shifted.columns = map(lambda x: x+str(sample_num), shifted.columns)
            final_df = concat([shifted, final_df], axis=1)

        final_df = final_df.fillna(0)
        final_df = final_df.drop(target_column, axis=1)

        result.append((final_df, flow_size))

    return result, time

def make_io(data):
    inputs = None
    outputs = None
    for d in data:
        i_data = d[0].as_matrix()
        o_data = d[1].tolist()

        if inputs is None:
            inputs = i_data
            outputs = o_data
        else:
            inputs = np.append(inputs, i_data, axis=0)
            outputs = np.append(outputs, o_data)
    return (inputs, outputs)

def time_make_io(data):
    times = []
    for d in data:
        for a in d:
            times.append(a)
    return times

def get_label(x):
    global thres
    for i in range(len(thres)):
        if x <= thres[i]:
            return i
    return len(thres)

def resize(s,scaling):
    return s/scaling[s.name]

def get_df():
    test_files = [os.path.join(TEST_PATH, f) for f in os.listdir(TEST_PATH)]

    test_data_scaling = calculate_scaling(test_files)
    test_data, test_time = prepare_files(test_files, WINDOW_SIZE, test_data_scaling, TARGET_COLUMN)
    test_inputs, test_outputs = make_io(test_data)
    test_time = time_make_io(test_time)
    test_pred = model.predict(test_inputs)
    test_output = [get_label(float(i)) for i in test_outputs]
    test_pred_binary = [get_label(float(i)) for i in test_pred]
    
    src = [random.randint(1,8) for i in xrange(len(test_time))]
    dst = [random.randint(1,8) for i in xrange(len(test_time))]

    allTree_preds = np.stack([t.predict(test_inputs) for t in model.estimators_], axis = 0)
    # print(allTree_preds)
    err_down = np.percentile(allTree_preds, (100 - 95) / 2.0, axis = 0)
    err_up = np.percentile(allTree_preds, 100 - (100 - 95) / 2.0, axis = 0)
    all_mean = np.mean(allTree_preds, axis = 0)

    df = pd.DataFrame()
    df['time'] = test_time
    df['yhat'] = test_pred
    df['y'] = test_output
    df['y_size'] = test_outputs
    # df['down'] = err_down
    # df['up'] = err_up
    df['Confidence'] = 100 - (err_up - err_down) / df['yhat']
    df.reset_index(inplace = True)
    # df_sorted = df.iloc[np.argsort(df['Confidence'])[::1]]
    df.drop(['yhat'],axis=1,inplace=True)
    df['src'] = src
    df['dst'] = dst
    df = df[df['src'] != df['dst']]
    df_big = df[df['y'] == 1]
    # df_big = df_big[0:1000]
    df_small = df[df['y'] == 0]
    # df_small = df_small[0:1000]
    return df_big, df_small
