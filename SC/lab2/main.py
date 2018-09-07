import numpy as np
import pandas as pd
import random


def pre_pro(data, class_feat):
    class_count = -1
    class_map = {}
    class_col = []
    for i in range(data[class_feat].size):
        j = class_map.get(data[class_feat][i], -1)
        if j == -1:
            class_count += 1
            j = class_map[data[class_feat][i]] = class_count
        class_col.append(j)
    class_index = list(data).index(class_feat)
    data[class_feat] = class_col
    np_data_class = data.values
    np.random.seed(1)
    np.random.shuffle(np_data_class)
    return np.delete(np_data_class, class_index, axis=1), np_data_class[:, class_index], class_count + 1


def sigmod_v(x):
    return 1 / (1 + np.exp(-x))


def train(np_data, np_class, l_rate):
    n_x, n_h, n_y = np_data.shape[1], 5, 1
    w1, b1 = np.full((n_x, n_h), 1 / (n_x * n_h)), np.full((1, n_h), 1 / (n_h + n_y))
    w2, b2 = np.full((n_h, n_y), 1 / (n_h * n_y)), np.full((1, n_y), 1 / (n_h + n_y))
    n_iter, max_n_iter, thres = 0, 500, 0.5
    while n_iter < max_n_iter:
        for i in range(np_data.shape[0]):
            y1 = sigmod_v(np_data[i].reshape((1, n_x)))
            # y1 = np_data[i].reshape((1, n_x))
            y2 = sigmod_v(np.matmul(y1, w1) + b1)
            y3 = sigmod_v(np.matmul(y2, w2) + b2)
            op = 1 if y3[0][0] > thres else 0

            t = np.array([np_class[i]])
            err3 = y3 * (1 - y3) * (t - op)
            err2 = y2 * (1 - y2) * np.matmul(err3, w2.T)

            w2 += l_rate * np.matmul(y2.T, err3)
            b2 += l_rate * err3
            w1 += l_rate * np.matmul(y1.T, err2)
            b1 += l_rate * err2
        n_iter += 1
    return w1, b1, w2, b2


def test(np_data, params):
    n_x, n_h, n_y = np_data.shape[1], 5, 1
    w1, b1, w2, b2 = params
    y_pred = np.zeros((np_data.shape[0],))
    thres = 0.5
    for i in range(np_data.shape[0]):
        y1 = sigmod_v(np_data[i].reshape((1, n_x)))
        y2 = sigmod_v(np.matmul(y1, w1) + b1)
        y3 = sigmod_v(np.matmul(y2, w2) + b2)
        y_pred[i] = 1 if y3[0][0] > thres else 0
    return y_pred


def cross_val_k(np_data, np_class, k, callback):
    random.seed(5)
    j = [0] + random.sample(range(np_data.shape[0]), k - 1) + [np_data.shape[0]]
    for i in range(k):
        train_data = np.concatenate((np_data[:j[i]], np_data[j[i + 1]:]))
        train_class = np.concatenate((np_class[:j[i]], np_class[j[i + 1]:]))
        test_data = np.concatenate((np_data[j[i]:], np_data[:j[i + 1]]))
        test_class = np.concatenate((np_class[j[i]:], np_class[:j[i + 1]]))
        callback(train_data, train_class, test_data, test_class)


def error_desc(y, y_pred):
    t0, f0, t1, f1 = 0, 0, 0, 0
    for yi, yi_pred in zip(y, y_pred):
        t0 += int(yi == yi_pred == 0)
        t1 += int(yi == yi_pred == 1)
        f0 += int(yi != yi_pred == 0)
        f1 += int(yi != yi_pred == 1)
    try:
        print('P+: %f R+: %f P-: %f R-: %f' % (t0 / (t0 + f0), t0 / (t0 + f1), t1 / (t1 + f1), t1 / (t1 + f0)))
    except ZeroDivisionError:
        print('Ignore')


def main():
    data = pd.read_csv('IRIS.csv')

    np_data, np_class, _ = pre_pro(data, 'class')

    def cb_main(train_data, train_class, test_data, test_class):
        params = train(train_data, train_class, 0.2)
        y_pred = test(test_data, params)
        error_desc(test_class, y_pred)

    cross_val_k(np_data, np_class, 10, cb_main)


main()
