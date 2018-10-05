import pandas as pd
import numpy as np
import random


def upper(arr, x):
    low, high = 0, len(arr) - 1
    mid = (low + high) // 2
    while low < high:
        if arr[mid] < x:
            low = mid + 1
        elif arr[mid] > x:
            high = mid
        else:
            break
        mid = (low + high) // 2
    return mid


def generate(length, n):
    return [[random.randint(0, 1) for _ in range(length)] for _ in range(n)]


def select(chromes, fitness):
    fitness_vec = [fitness(chrome) for chrome in chromes]
    fitness_sum = sum(fitness_vec)
    prob_vec = [fit / fitness_sum for fit in fitness_vec]
    cumulative = [0] * len(chromes)
    for i in range(len(chromes)):
        cumulative[i] = prob_vec[i] + cumulative[i - 1]
    chromes[:] = [chromes[upper(cumulative, random.random())] for _ in range(len(chromes))]


def crossover(chromes, rate):
    n = int(len(chromes) * rate / 100)
    m_chromes = random.sample(range(len(chromes[0])), n)
    new_chromes = []
    for i in range(-1, len(m_chromes) - 1):
        point = random.randint(0, len(chromes[0]) - 1)
        new_chromes.append(chromes[m_chromes[i]][:point] + chromes[m_chromes[i + 1]][point:])
    for i in range(-1, len(m_chromes) - 1):
        chromes[m_chromes[i]] = new_chromes[i + 1]


def mutate(chromes, rate):
    n = int(len(chromes) * len(chromes[0]) * rate / 100)
    for i in random.sample(range(len(chromes) * len(chromes[0])), n):
        chromes[i // len(chromes)][i % len(chromes[0])] = 1 - chromes[i // len(chromes)][i % len(chromes[0])]


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
        freq_class[i] /= n_rows
    return prob_tab, freq_class


def test(np_data, prob_tab, prob_class):
    n_rows, n_feat = np_data.shape
    y_pred = np.zeros((n_rows))
    for i in range(n_rows):
        prob0, prob1 = prob_class[0], prob_class[1]
        for j in range(n_feat):
            prob0 *= prob_tab[0][j][np_data[i][j]]
            prob1 *= prob_tab[1][j][np_data[i][j]]
        y_pred[i] = int(prob1 > prob0)
    return y_pred


def cross_val_k(np_data, np_class, k, callback):
    random.seed(5)
    j = [0] + random.sample(range(np_data.shape[0]), k - 1) + [np_data.shape[0]]
    j = [0] + [np_data.shape[0]*.9] + [np_data.shape[0]]
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
        # t0 += int(yi == yi_pred == 0)
        # t1 += int(yi == yi_pred == 1)
        # f0 += int(yi != yi_pred == 0)
        # f1 += int(yi != yi_pred == 1)
        acc += int(yi == yi_pred)
    try:
        acc /= y.shape[0]
        macc.append(100 * acc)
        # mp0.append(100 * t0 / (t0 + f0))
        # mr0.append(100 * t0 / (t0 + f1))
        # mp1.append(100 * t1 / (t1 + f1))
        # mr1.append(100 * t1 / (t1 + f0))
    except ZeroDivisionError:
        print('Ignore')


def main():
    data = pd.read_csv('SPECT.csv')
    np_data, np_class, n_class = pre_pro(data, 'Class')

    def nb_fitness(chrome):
        good_data = np_data.copy()
        delete_cols = []
        for i in range(len(chrome)):
            if chrome[i] == 0:
                delete_cols.append(i)
        good_data = np.delete(good_data, delete_cols, 1)
        err_params = ([], [], [], [], [])

        def cb_main(train_data, train_class, test_data, test_class):
            global mp0, mr0, mp1, mr1
            prob_tab, prob_class = train(train_data, train_class, n_class)
            y_pred = test(test_data, prob_tab, prob_class)
            error_desc(test_class, y_pred, err_params)

        cross_val_k(good_data, np_class, 10, cb_main)

        return sum(err_params[0]) / len(err_params[0])

    chromosomes = generate(np_data.shape[1], 30)
    for _ in range(100):
        select(chromosomes, nb_fitness)
        crossover(chromosomes, 25)
        mutate(chromosomes, 10)
        print(sum([nb_fitness(chrome) for chrome in chromosomes]) / len(chromosomes))


if __name__ == '__main__':
    main()
