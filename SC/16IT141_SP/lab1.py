import pandas as pd
import numpy as np

def spm(data, class_feat):
    n_rows, n_feat = data.shape
    w = [1 / n_feat] * n_feat
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
    err, threshold, n_iter, l, mid = 0, 0, 0, .2, -10
    while True:
        n_iter += 1
        err = 0
        for i in range(test_data.shape[0]):
            y = 0
            for j in range(n_feat):
                y += w[j] * (1 if class_index == j else test_data[i][j])
            y = 1 if y > mid else 0
            z = test_data[i][class_index]
            for j in range(n_feat):
                w[j] += l * (z - y) * (1 if class_index == j else test_data[i][j])
            err += z - y
        if abs(err) <= threshold:
            break
    print('Number of iterations: %d' % n_iter)
    err = 0
    for i in range(train_data.shape[0]):
        y = 0
        for j in range(n_feat):
            y += w[j] * (1 if class_index == j else test_data[i][j])
        y = 1 if y > mid else 0
        z = test_data[i][class_index]
        err += z - y
    print('Error: %d' % err)


def main():
    data = pd.read_csv('SPECT.csv')
    spm(data, 'Class')


if __name__ == '__main__':
    main()
