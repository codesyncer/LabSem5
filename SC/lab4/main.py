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


def val(np_data, np_class, x):
    k = 10
    knn = []
    for i in range(np_data.shape[0]):
        dist = distance(np_data[i], x)
        if len(knn) < k:
            heapq.heappush(knn, (-dist, i))
        elif dist < -knn[0][0]:
            heapq.heappushpop(knn, (-dist, i))
    print([knn])


def main():
    data = pd.read_csv('SPECT.csv')
    np_data, np_class, n_class = pre_pro(data, 'Class')
    train_data, train_class = np_data[]
    test_data, test_class = np_data[]


if __name__ == '__main__':
    main()
