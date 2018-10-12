import random
import pandas as pd
import numpy as np
import heapq


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


def distance(x1, x2):
    return np.sum((x1 - x2) ** 2) ** .5


def train():
    pass


def val(np_data, np_class, n_class, x):
    k = 11
    knn = []
    votes = [0] * n_class
    for i in range(np_data.shape[0]):
        dist = distance(np_data[i], x)
        if len(knn) < k:
            heapq.heappush(knn, (-dist, i))
        elif dist < -knn[0][0]:
            heapq.heappushpop(knn, (-dist, i))
    highest_class = 0
    for i in range(len(knn)):
        curr_class = int(np_class[knn[i][1]])
        votes[curr_class] += 1
        if votes[highest_class] < votes[curr_class]:
            highest_class = curr_class
    return highest_class


def test(train_data, train_class, test_data, n_class):
    n_rows, n_feat = test_data.shape
    y_pred = np.zeros((n_rows))
    for i in range(test_data.shape[0]):
        y_pred[i] = val(train_data, train_class, n_class, test_data[i])
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


def error_desc(y, y_pred, err_params):
    macc, mp0, mr0, mp1, mr1 = err_params
    t0, f0, t1, f1, acc = 0, 0, 0, 0, 0
    for yi, yi_pred in zip(y, y_pred):
        t0 += int(yi == yi_pred == 0)
        t1 += int(yi == yi_pred == 1)
        f0 += int(yi != yi_pred == 0)
        f1 += int(yi != yi_pred == 1)
        acc += int(yi == yi_pred)
    try:
        acc /= y.shape[0]
        print('Acc: %f P+: %f R+: %f P-: %f R-: %f' % (
            100 * acc, 100 * t0 / (t0 + f0), 100 * t0 / (t0 + f1), 100 * t1 / (t1 + f1), 100 * t1 / (t1 + f0)))
        macc.append(100 * acc)
        mp0.append(100 * t0 / (t0 + f0))
        mr0.append(100 * t0 / (t0 + f1))
        mp1.append(100 * t1 / (t1 + f1))
        mr1.append(100 * t1 / (t1 + f0))
    except ZeroDivisionError:
        print('Ignore')


def main():
    data = pd.read_csv('SPECT.csv')
    np_data, np_class, n_class = pre_pro(data, 'Class')
    err_params = ([], [], [], [], [])

    def cb_main(train_data, train_class, test_data, test_class):
        global mp0, mr0, mp1, mr1
        y_pred = test(train_data, train_class, test_data, n_class)
        error_desc(test_class, y_pred, err_params)

    cross_val_k(np_data, np_class, 10, cb_main)
    print('MEAN Acc: %f P+: %f R+: %f P-: %f R-: %f' % tuple([sum(param) / len(param) for param in err_params]))


if __name__ == '__main__':
    main()
