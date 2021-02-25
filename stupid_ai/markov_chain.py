import random


def gen_alphabet():
    return list(map(lambda x: chr(x), range(
        ord('а'),
        ord('я') + 1))) + ['ё']


def max_element_index(array):
    return max(range(len(array)), key=array.__getitem__)


def take_highscores(array, n=1):
    a = array[:]
    highscores = sorted(range(len(a)), key=a.__getitem__, reverse=True)[:n]
    return highscores


class MarkovChain():

    stop_symbol = '.'
    alphabet = gen_alphabet() + [stop_symbol]
    n_letters = len(alphabet)

    def __init__(self):
        random.seed()
        self.reset()

    def reset(self):
        self.H = [[0 for i in range(self.n_letters)]
                  for j in range(self.n_letters)]
        self.h_totals = [0] * self.n_letters
        self.P = [[0 for i in range(self.n_letters)]
                  for j in range(self.n_letters)]

    def letter_to_index(self, l):
        return self.alphabet.index(l)

    @staticmethod
    def make_file_iterator(file):
        name = file.readline().strip()
        while name != '':
            if len(name) > 1:
                yield name
            name = file.readline().strip()

    def set_file(self, filename):
        self.file = open(filename, encoding='utf-8')
        self.file_iterator = self.make_file_iterator(self.file)

    def train(self):
        for name in self.file_iterator:
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

        # print(h_totals)
        # print(H)

        for i in range(len(self.H)):
            H_i = self.H[i]
            # print(H_i)
            j_max = max_element_index(H_i)
            # print(j_max, H_i[j_max])
            for j in range(len(H_i)):
                if self.h_totals[i] > 0:
                    self.P[i][j] = self.H[i][j] / self.h_totals[i]
        # print(P)

    def max_likelihood_next(self, letter):
        i = self.letter_to_index(letter)
        H_i = self.H[i]
        j_max = max_element_index(H_i)
        return self.alphabet[j_max]

    def rand_likelihood_next(self, letter):
        i = self.letter_to_index(letter)
        highscores = take_highscores(self.H[i], n=5)
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

    def generate(self, first_letter, method='random', max_name_length=10):
        new_name = first_letter
        while new_name[-1] != self.stop_symbol and len(new_name) < max_name_length:
            if method == 'random':
                r = random.random()
                new_name += self.next_by_probability(new_name[-1], r)
            elif method == 'max_likelihood':
                new_name += self.max_likelihood_next(new_name[-1])
            elif method == 'rand_likelihood':
                new_name += self.rand_likelihood_next(new_name[-1])
        return new_name
