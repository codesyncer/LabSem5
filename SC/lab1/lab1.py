import pandas as pd
import numpy as np


def spm(data, class_feat):
    n_rows, n_feat = data.shape
    w = [1 / n_feat] * n_feat
    class_index = list(data).index(class_feat)
    class_count = 0
    class_map = {}
    class_col = []
    for i in range(data[class_feat].size):
        j = class_map.get(data[class_feat][i], -1)
        if j == -1:
            class_count +=
            class_map[data[class_feat][i]] = class_count
            j =
        class_col.append(j)


def main():
    data = pd.read_csv('IRIS.csv')
    spm(data, 'class')


if __name__ == '__main__':
    main()
