import pandas as pd
import numpy as np
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
    np.random.shuffle(np_data_class)
    return np.delete(np_data_class, class_index, axis=1), np_data_class[:, class_index], class_count + 1


def train(np_data, np_class, n_class):
    n_rows, n_feat = np_data.shape
    prob_tab = np.zeros([n_class, n_feat, 2])
    freq_class = np.zeros([n_class])
    for i in range(n_rows):
        freq_class[np_class[i]] += 1
        for j in range(n_feat):
            prob_tab[np_class[i]][j][np_data[i][j]] += 1
    for i in range(n_class):
        prob_tab[i] /= freq_class[i]
    return prob_tab


def test(np_data, prob_tab):
    n_rows, n_feat = np_data.shape
    y_pred = np.zeros((n_rows))
    for i in range(n_rows):
        prob0, prob1 = 1, 1
        for j in range(n_feat):
            prob0 *= prob_tab[0][j][np_data[i][j]]
            prob1 *= prob_tab[1][j][np_data[i][j]]
        y_pred[i] = 1 if prob1 > prob0 else 0
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
        return t0 / (t0 + f0), t0 / (t0 + f1), t1 / (t1 + f1), t1 / (t1 + f0)
    except ZeroDivisionError:
        print('Fail')
        return 0, 0, 0, 0


mp0, mr0, mp1, mr1 = 0, 0, 0, 0


def main():
    data = pd.read_csv('SPECT.csv')
    np_data, np_class, n_class = pre_pro(data, 'Class')

    def cb_main(train_data, train_class, test_data, test_class):
        global mp0, mr0, mp1, mr1
        prob_tab = train(train_data, train_class, n_class)
        y_pred = test(test_data, prob_tab)
        p0, r0, p1, r1 = error_desc(test_class, y_pred)
        print('P+: %f R+: %f P-: %f R-: %f' % (p0, r0, p1, r1))
        mp0, mr0, mp1, mr1 = mp0 + p0, mr0 + r0, mp1 + p1, mr1 + r1

    k = 10
    cross_val_k(np_data, np_class, k, cb_main)
    print('Mean P+: %f R+: %f P-: %f R-: %f' % (100 * mp0 / k, 100 * mr0 / k, 100 * mp1 / k, 100 * mr1 / k))


if __name__ == '__main__':
    main()
