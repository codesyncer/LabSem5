import pandas as pd
import numpy as np
import random


def generate(length, n):
    return np.random.randint(0, 2, (n, length))


def select(chromes, fitness_func):
    n = chromes.shape[0]
    fitness = np.apply_along_axis(fitness_func, 0, chromes)
    fitness_sum = np.sum(fitness)
    cumulative = np.cumsum(fitness / fitness_sum)
    chromes[:] = np.array([chromes[np.searchsorted(cumulative, (random.random(),), side='left')[0]] for _ in range(n)])


def crossover(chromes, rate):
    n = chromes.shape[0]
    length = chromes[0].shape[0]
    n_crossover = int(len(chromes) * rate / 100)
    index = random.sample(range(n), n_crossover)
    new_chromes = chromes.copy()
    for i in range(n_crossover):
        point = random.randint(0, length - 1)
        new_chromes[index[i - 1]] = np.concatenate((chromes[index[i - 1]][:point], chromes[index[i]][point:]))
    chromes[:] = new_chromes


def mutate(chromes, rate):
    n = chromes.shape[0]
    length = chromes[0].shape[0]
    n_mutate = int(n * length * rate / 100)
    for i in random.sample(range(n * length), n_mutate):
        chromes[i // length][i % length] = 1 - chromes[i // length][i % length]


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
    y_predicted = np.zeros(n_rows)
    for i in range(n_rows):
        prob0, prob1 = prob_class[0], prob_class[1]
        for j in range(n_feat):
            prob0 *= prob_tab[0][j][np_data[i][j]]
            prob1 *= prob_tab[1][j][np_data[i][j]]
        y_predicted[i] = int(prob1 > prob0)
    return y_predicted


def cross_val_k(np_data, np_class, k, callback):
    errs = ([], [], [], [], [])
    random.seed(5)
    j = [0] + random.sample(range(np_data.shape[0]), k - 1) + [np_data.shape[0]]
    for i in range(k):
        train_data = np.concatenate((np_data[:j[i]], np_data[j[i + 1]:]))
        train_class = np.concatenate((np_class[:j[i]], np_class[j[i + 1]:]))
        test_data = np.concatenate((np_data[j[i]:], np_data[:j[i + 1]]))
        test_class = np.concatenate((np_class[j[i]:], np_class[:j[i + 1]]))
        run_err = callback(train_data, train_class, test_data, test_class)
        if run_err[0] == -1:
            print('Ignore run')
            continue
        for m in range(len(errs)):
            errs[m].append(run_err[m])
    return errs


def ninety_ten(np_data, np_class, k, callback):
    errs = ([], [], [], [], [])
    n = np_data.shape[0]
    train_data, train_class = np_data[:int(.9 * n)], np_class[:int(.9 * n)]
    test_data, test_class = np_data[int(.9 * n):], np_class[int(.9 * n):]
    run_err = callback(train_data, train_class, test_data, test_class)
    if run_err[0] == -1:
        print('Ignore run')
    for m in range(len(errs)):
        errs[m].append(run_err[m])
    return errs


def get_err(y, y_predicted):
    return 100 * np.sum(y == y_predicted) / y.shape[0], 0, 0, 0, 0
    # acc, t0, f0, t1, f1 = 0, 0, 0, 0, 0
    # for yi, yi_predicted in zip(y, y_predicted):
    #     t0 += int(yi == yi_predicted == 0)
    #     t1 += int(yi == yi_predicted == 1)
    #     f0 += int(yi != yi_predicted == 0)
    #     f1 += int(yi != yi_predicted == 1)
    #     acc += int(yi == yi_predicted)
    # a_acc = 0 if y.shape[0] == 0 else 100 * acc / y.shape[0]
    # p0 = 0 if t0 + f0 == 0 else 100 * t0 / (t0 + f0)
    # r0 = 0 if t0 + f1 == 0 else 100 * t0 / (t0 + f1)
    # p1 = 0 if t1 + f1 == 0 else 100 * t1 / (t1 + f1)
    # r1 = 0 if t1 + f0 == 0 else 100 * t1 / (t1 + f0)
    # return a_acc, p0, r0, p1, r1


def main():
    data = pd.read_csv('SPECT.csv')
    np_data, np_class, n_class = pre_pro(data, 'Class')

    def nb_fitness(chrome):
        good_data = np.delete(np_data, np.where(chrome == 0), 1)

        def cb_main(train_data, train_class, test_data, test_class):
            prob_tab, prob_class = train(train_data, train_class, n_class)
            y_predicted = test(test_data, prob_tab, prob_class)
            return get_err(test_class, y_predicted)

        # err = cross_val_k(good_data, np_class, 10, cb_main)
        err = ninety_ten(good_data, np_class, 10, cb_main)
        return sum(err[0]) / len(err[0])

    chromosomes = generate(np_data.shape[1], 30)
    for _ in range(100):
        select(chromosomes, nb_fitness)
        crossover(chromosomes, 25)
        mutate(chromosomes, 10)
        print(sum([nb_fitness(chrome) for chrome in chromosomes]) / len(chromosomes))


if __name__ == '__main__':
    main()
