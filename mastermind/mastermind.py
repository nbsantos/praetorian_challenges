from collections import defaultdict
from heapq import *
from itertools import permutations, product
from typing import Tuple

# Guess is a list of variable int tuples.
Guess = Tuple[int, ...]
Score = Tuple[int, int]


class Mastermind:
    S = []
    possible_guesses = []
    scoreset_counts = {}

    def __init__(self, weapons, gladiators):
        self.weapons = weapons
        self.gladiators = gladiators
        self.S = set(permutations(range(1, weapons + 1), gladiators))
        self.possible_guesses = self.S.copy()
        self.scoreset_counts = {
            s: defaultdict(int) for s in product(range(gladiators + 1), repeat=2)}

    def next_guess(self):
        guess = self.possible_guesses.pop()
        self.S.remove(guess)

        return guess

    def prune(self, guess: Guess, resp: Guess):
        '''Remove from S any code that would not give the same
        response if it (the guess) were the code.'''

        self.S = [s for s in self.S if Mastermind.score(s, guess) == resp]

    def minmax(self):
        for pg in self.possible_guesses:
            for s in self.S:
                self.scoreset_counts[Mastermind.score(pg, s)][pg] += 1

    @staticmethod
    def score(guess: Guess, code: Guess) -> Score:
        '''Helper function to generate a score similar to
        the game implementation.'''

        w = b = 0
        for i, n in enumerate(guess):
            if n in code:
                w += 1
            if n == code[i]:
                b += 1
        return w, b


if __name__ == '__main__':
    code = (2, 5, 1, 0)
    weapons = 6
    gladiators = 4

    m = Mastermind(weapons, gladiators)

    guess = m.next_guess()

    m.prune(guess, (2, 1))

    m.minmax()

    print('done')
