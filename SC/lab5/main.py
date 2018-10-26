import pandas as pd
import numpy as np


def generate(length, n):
    return np.random.randint(0, 2, (n, length))


def select(chromes, fitness_func):
    n = chromes.shape[0]
    fitness = np.apply_along_axis(fitness_func, 0, chromes)
    cumulative = np.cumsum(fitness / np.sum(fitness))
    return np.array([chromes[np.searchsorted(cumulative, (np.random.random(),), side='left')[0]] for _ in range(n)])


def crossover(chromes, rate):
    n = chromes.shape[0]
    length = chromes[0].shape[0]
    n_crossover = int(n * rate / 100)
    index = np.random.choice(range(n), n_crossover, False)
    new_chromes = chromes.copy()
    j = 0
    while j < n:
        np.random.shuffle(index)
        for i in range(n_crossover):
            point = np.random.randint(0, length)
            new_chromes[j] = np.concatenate((chromes[index[i - 1]][:point], chromes[index[i]][point:]))
            j += 1
            if j >= n:
                break
    return new_chromes


def mutate(chromes, rate):
    n = chromes.shape[0]
    length = chromes[0].shape[0]
    n_mutate = int(n * length * rate / 100)
    for i in np.random.choice(range(n * length), n_mutate, False):
        chromes[i // length][i % length] = 1 - chromes[i // length][i % length]
    return chromes


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


def split_call(np_data, np_class, train_split, callback):
    n = np_data.shape[0]
    mark = int(train_split * n)
    train_data, train_class = np_data[:mark], np_class[:mark]
    test_data, test_class = np_data[mark:], np_class[mark:]
    return callback(train_data, train_class, test_data, test_class)


def main1():
    np.random.seed(1)
    data = pd.read_csv('SPECT.csv')
    np_data, np_class, n_class = pre_pro(data, 'Class')

    def cb_main(train_data, train_class, test_data, test_class):
        prob_tab, prob_class = train(train_data, train_class, n_class)
        y_predicted = test(test_data, prob_tab, prob_class)
        return 100 * np.sum(test_class == y_predicted) / test_class.shape[0]

    print(split_call(np_data, np_class, .9, cb_main))


def main():
    np.random.seed(1)
    data = pd.read_csv('SPECT.csv')
    np_data, np_class, n_class = pre_pro(data, 'Class')

    def nb_fitness(chrome):
        good_data = np.delete(np_data, np.where(chrome == 0), 1)

        def cb_main(train_data, train_class, test_data, test_class):
            prob_tab, prob_class = train(train_data, train_class, n_class)
            y_predicted = test(test_data, prob_tab, prob_class)
            return 100 * np.sum(test_class == y_predicted) / test_class.shape[0]

        return split_call(good_data, np_class, .9, cb_main)

    chromosomes = generate(np_data.shape[1], 30)
    for i in range(100):
        chromosomes = select(chromosomes, nb_fitness)
        chromosomes = crossover(chromosomes, 25)
        chromosomes = mutate(chromosomes, 10)
        print('%3d: %d%%' % (i, sum([nb_fitness(chrome) for chrome in chromosomes]) / len(chromosomes)))
        # print(nb_fitness(chromosomes[0]))


if __name__ == '__main__':
    main()
