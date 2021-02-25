import os
import matplotlib.pyplot as plt
from stupid_ai.markov_chain import MarkovChain



m = MarkovChain()
m.set_file(os.path.join('data', 'male.txt'))
m.train()
print(list(map(lambda x: m.generate(x, method='max_likelihood'), m.alphabet[:-1])))

m.set_file(os.path.join('data', 'female.txt'))
m.train()
print(list(map(lambda x: m.generate(x, method='max_likelihood'), m.alphabet[:-1])))

plt.matshow(m.P)
plt.colorbar()
plt.show()
