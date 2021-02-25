import os
import pytest
from stupid_ai.markov_chain import MarkovChain

@pytest.fixture
def markov_chain():
  m = MarkovChain()
  m.set_file(os.path.join('data', 'male.txt'))
  m.train()
  return m

def test_p_values(markov_chain):
  assert markov_chain.P[0][0] == 0.004246284501061571
  assert markov_chain.P[0][1] == 0.008492569002123142
  assert markov_chain.P[0][2] == 0.12101910828025478
  assert markov_chain.P[0][3] == 0.016985138004246284

def test_h_values(markov_chain):
  assert markov_chain.H[0][0] == 2
  assert markov_chain.H[0][1] == 4
  assert markov_chain.H[0][2] == 57
  assert markov_chain.H[0][3] == 8

def test_h_total_values(markov_chain):
  assert markov_chain.h_totals[0] == 471
  assert markov_chain.h_totals[1] == 29
  assert markov_chain.h_totals[2] == 153
  