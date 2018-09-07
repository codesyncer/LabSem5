import pandas as pd
import numpy as np


def spm(data, class_feat, learning_rate=0.2, fire_threshold=0):
    n_rows, n_feat = data.shape
    class_index = list(data).index(class_feat)
    class_count = -1
    class_map = {}
    class_col = []
    for i in range(data[class_feat].size):
        j = class_map.get(data[class_feat][i], -1)
        if j == -1:
            class_count += 1
            j = class_map[data[class_feat][i]] = class_count
        class_col.append(j)
    data[class_feat] = class_col
    np_data = data.values
    np.random.seed(3)
    np.random.shuffle(np_data)
    train_data, test_data = np_data[:int(.9 * n_rows)], np_data[int(.9 * n_rows):]
    err_threshold, n_iter = 0, 0
    err = err_threshold + 1
    w = [1 / n_feat] * n_feat
    while err > err_threshold and n_iter < 1000:
        err = 0
        for i in range(train_data.shape[0]):
            w_sum = 0
            for j in range(n_feat):
                w_sum += w[j] * (1 if class_index == j else train_data[i][j])
            y = int(w_sum > fire_threshold)
            z = train_data[i][class_index]
            for j in range(n_feat):
                w[j] += learning_rate * (z - y) * (1 if class_index == j else train_data[i][j])
            err += abs(z - y)
        n_iter += 1
    print('TRAIN: #Iterations: %d, Accuracy %f' % (n_iter, (1 - err / train_data.shape[0]) * 100))
    err = 0
    for i in range(test_data.shape[0]):
        y = 0
        for j in range(n_feat):
            y += w[j] * (1 if class_index == j else test_data[i][j])
        y = int(y > fire_threshold)
        z = test_data[i][class_index]
        err += abs(z - y)
    print('TEST: Accuracy %f' % ((1 - err / test_data.shape[0]) * 100))


def main():
    data = pd.read_csv('IRIS.csv')
    spm(data, 'class')

    data = pd.read_csv('SPECT.csv')
    spm(data, 'Class')


if __name__ == '__main__':
    main()
