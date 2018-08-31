import pandas as pd
import numpy as np

def pre_pro(data, class_feat):
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
    data = data.drop(class_feat, axis=1)
    return data.values, np.array(class_col), class_count+1

def nba(data, class_feat):
    np_data, np_class, n_class = pre_pro(data, class_feat)
    n_rows, n_feat = np_data.shape
    freq_tab = np.zeros([n_class, 2, n_feat])
    freq_class = np.zeros([n_class])
    for i in range(n_rows):
        freq_class[np_class[i]] += 1
        for j in range(n_feat):
            freq_tab[np_class[i]][np_data[i][j]][j] += 1
    for i in range(n_class):
        for j in range(n_feat):
            freq_tab[i][j] /= freq_class[i]
    print(freq_tab)



def main():
    data = pd.read_csv('SPECT.csv')
    nba(data, 'Class')


if __name__ == '__main__':
    main()