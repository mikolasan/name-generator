import random


class MarkovChain():

    n_letters = 33 + 1
    stop_symbol = '.'
    alphabet = list(map(lambda x: chr(x), range(
        ord('а'),
        ord('я') + 1))) + ['ё', stop_symbol]
    max_name_length = 10

    def __init__(self):
        random.seed()
        self.reset()

    def reset(self):
        self.H = [[0 for i in range(self.n_letters)] for j in range(self.n_letters)]
        self.h_totals = [0] * self.n_letters
        self.P = [[0 for i in range(self.n_letters)] for j in range(self.n_letters)]

    def letter_to_index(self, l):
        return self.alphabet.index(l)

    def set_file(self, filename):
        self.f = open(filename, encoding='utf-8')

    def train(self):
        name = self.f.readline().strip()
        while name != '':
            if len(name) > 1:
                for k in range(0, len(name)):
                    letter = name[k].lower()
                    if k == len(name) - 1:
                        next_letter = self.stop_symbol
                    else:
                        next_letter = name[k + 1].lower()
                    i = self.letter_to_index(letter)
                    j = self.letter_to_index(next_letter)
                    self.H[i][j] += 1
                    self.h_totals[i] += 1
            name = self.f.readline().strip()

        # print(h_totals)
        # print(H)

        for i in range(len(self.H)):
            H_i = self.H[i]
            # print(H_i)
            j_max = max(range(len(H_i)), key=H_i.__getitem__)
            # print(j_max, H_i[j_max])
            for j in range(len(self.H[i])):
                if self.h_totals[i] > 0:
                    self.P[i][j] = self.H[i][j] / self.h_totals[i]
        # print(P)

    def max_likelihood_next(self, letter):
        i = self.letter_to_index(letter)
        H_i = self.H[i]
        j_max = max(range(len(H_i)), key=H_i.__getitem__)
        return self.alphabet[j_max]


    def rand_likelihood_next(self, letter):
        i = self.letter_to_index(letter)
        H_i = self.H[i][:]
        highscores = sorted(range(len(H_i)), key=H_i.__getitem__, reverse=True)[:5]
        return self.alphabet[random.choice(highscores)]


    def next_by_probability(self, letter, random_number):
        i = self.letter_to_index(letter)
        P_i = self.P[i]
        j = 0
        U = P_i[j]
        while U < random_number and j < len(P_i) - 1:
            j += 1
            # print(U, random_number, j, len(H_i))
            U += P_i[j]
        return self.alphabet[j]


    def generate(self, first_letter, method='random'):
        new_name = first_letter
        while new_name[-1] != self.stop_symbol and len(new_name) < self.max_name_length:
            if method == 'random':
                r = random.random()
                new_name += self.next_by_probability(new_name[-1], r)
            elif method == 'max_likelihood':
                new_name += self.max_likelihood_next(new_name[-1])
            elif method == 'rand_likelihood':
                new_name += self.rand_likelihood_next(new_name[-1])
        return new_name


