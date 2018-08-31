import pandas as pd
import numpy as np


def spm(data, class_feat, learning_rate=0.5, fire_threshold=0):
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
    np.random.shuffle(np_data)
    test_data, train_data = np_data[:int(.9 * n_rows)], np_data[int(.9 * n_rows):]
    err, err_threshold, n_iter = 0, 0, 0
    w = [1 / n_feat] * n_feat
    while True and n_iter < 1000:
        n_iter += 1
        err = 0
        for i in range(test_data.shape[0]):
            w_sum = 0
            for j in range(n_feat):
                w_sum += w[j] * (1 if class_index == j else test_data[i][j])
            y = 1 if w_sum > fire_threshold else 0
            z = test_data[i][class_index]
            for j in range(n_feat):
                w[j] += learning_rate * (z - y) * (1 if class_index == j else test_data[i][j])
            err += abs(z - y)
        if err <= err_threshold:
            break
    print('Number of iterations: %d' % n_iter)
    test_err = 0
    for i in range(train_data.shape[0]):
        y = 0
        for j in range(n_feat):
            y += w[j] * (1 if class_index == j else test_data[i][j])
        y = 1 if y > fire_threshold else 0
        z = test_data[i][class_index]
        test_err += abs(z - y)
    print('Error: %d' % test_err)


def main():
    data = pd.read_csv('IRIS.csv')
    spm(data, 'class', 0.5, 0.6)

    data = pd.read_csv('SPECT.csv')
    spm(data, 'Class', 0.9, 0.6)


if __name__ == '__main__':
    main()
