import os
import random
import matplotlib.pyplot as plt

n_letters = 33 + 1
H = [[0 for i in range(n_letters)] for j in range(n_letters)]
h_totals = [0] * n_letters
P = [[0 for i in range(n_letters)] for j in range(n_letters)]

stop_symbol = '.'
alphabet = list(map(lambda x: chr(x), range(
    ord('а'),
    ord('я') + 1))) + ['ё', stop_symbol]
max_name_length = 10


def letter_to_index(l):
    return alphabet.index(l)


def train(filename):
    global H
    H = [[0 for i in range(n_letters)] for j in range(n_letters)]
    global h_totals
    h_totals = [0] * n_letters
    global P
    P = [[0 for i in range(n_letters)] for j in range(n_letters)]
    with open(filename, encoding='utf-8') as f:
        name = f.readline().strip()
        while name != '':
            if len(name) > 1:
                for k in range(0, len(name)):
                    letter = name[k].lower()
                    if k == len(name) - 1:
                        next_letter = stop_symbol
                    else:
                        next_letter = name[k + 1].lower()
                    i = letter_to_index(letter)
                    j = letter_to_index(next_letter)
                    H[i][j] += 1
                    h_totals[i] += 1
            name = f.readline().strip()

        # print(h_totals)
        # print(H)

        for i in range(len(H)):
            H_i = H[i]
            # print(H_i)
            j_max = max(range(len(H_i)), key=H_i.__getitem__)
            # print(j_max, H_i[j_max])
            for j in range(len(H[i])):
                if h_totals[i] > 0:
                    P[i][j] = H[i][j] / h_totals[i]
        # print(P)


def max_likelihood_next(letter):
    i = letter_to_index(letter)
    H_i = H[i]
    j_max = max(range(len(H_i)), key=H_i.__getitem__)
    return alphabet[j_max]


def rand_likelihood_next(letter):
    i = letter_to_index(letter)
    H_i = H[i][:]
    highscores = sorted(range(len(H_i)), key=H_i.__getitem__, reverse=True)[:5]
    return alphabet[random.choice(highscores)]


def next_by_probability(letter, random_number):
    i = letter_to_index(letter)
    P_i = P[i]
    j = 0
    U = P_i[j]
    while U < random_number and j < len(P_i) - 1:
        j += 1
        # print(U, random_number, j, len(H_i))
        U += P_i[j]
    return alphabet[j]


def generate(first_letter, method='random'):
    new_name = first_letter
    while new_name[-1] != stop_symbol and len(new_name) < max_name_length:
        if method == 'random':
            r = random.random()
            new_name += next_by_probability(new_name[-1], r)
        elif method == 'max_likelihood':
            new_name += max_likelihood_next(new_name[-1])
        elif method == 'rand_likelihood':
            new_name += rand_likelihood_next(new_name[-1])
    return new_name


random.seed()

train(os.path.join('data', 'male.txt'))
print(list(map(lambda x: generate(x, method='max_likelihood'), alphabet[:-1])))

train(os.path.join('data', 'female.txt'))
print(list(map(lambda x: generate(x, method='max_likelihood'), alphabet[:-1])))

plt.matshow(P)
plt.colorbar()
plt.show()
