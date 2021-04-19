from collections import defaultdict
from heapq import heappop, heappush
from itertools import permutations
from typing import Tuple
from requests import session

import argparse
import sys

# Guess is a list of variable int tuples.
Guess = Tuple[int, ...]
Score = Tuple[int, int]


class Mastermind:
    '''Implementation of Knuth's algorithm to play the Mastermind game.
    
    The original algorithm is supposed to solve the game in five moves or less.
    Since the challenge uses a modified version of the game, and I'm not nearly
    as smart as Knuth, I don't know how optimized this is :)'''
    
    def __init__(self, gladiators: int, guesses: int, rounds: int, weapons: int):
        self._gladiators = gladiators
        self._guesses = guesses
        self._rounds = rounds
        self._weapons = weapons
        self._S = self._generate_codes()
        self._possible_guesses = self._S.copy()
        self._scoreset_counts = []  # priority queue

    def prune(self, guess: Guess, score: Score):
        '''Remove from S any code that would not give the same
        response if it (the guess) were the code.'''

        self._S = [s for s in self._S if Mastermind.score(s, guess) == score]

    def next_guess(self) -> Guess:
        self._update_scoreset_counts()
        
        _, _, guess = heappop(self._scoreset_counts)
        
        # remove guess from lists
        try:
            self._S.remove(guess)
        except ValueError:
            pass
        finally:
            self._possible_guesses.remove(guess)
        
        
        return guess
                
    def _generate_codes(self):
        '''Generate all possible code permutations.'''
        return set(permutations(range(self._weapons), self._gladiators))  # permutations instead of product
    
    def _update_scoreset_counts(self):
        '''Helper function to generate a list with how many possibilities in
        S would be eliminated for each possible colored/white peg score.
        
        e.g.: [(25, (1, 2, 3, 4)), (15, (2, 1, 4, 3)), ...]
        '''
        
        self._scoreset_counts.clear()  # reset counts
         
        for pg in self._possible_guesses:
            scores = defaultdict(int)
            for s in self._S:
                scores[Mastermind.score(pg, s)] += 1
            # -(pg in self._S) prioritizes items in S
            heappush(self._scoreset_counts, (max(scores.values()), -(pg in self._S),pg))

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
    parser = argparse.ArgumentParser(description='Play Praetorian Mastermind challenge.')
    parser.add_argument('-e', '--email', default='nbsantos@gmail.com', help='email address')
    parser.add_argument('-l', '--level', type=int, default=1, help='which game level to play')
    parser.add_argument('-s', '--hash', action='store_true', help='print the challenge hash')
    parser.add_argument('-r', '--reset', action='store_true', help='reset the game')
    args = parser.parse_args()
    
    base = 'https://mastermind.praetorian.com'
    auth = base + '/api-auth-token/'
    level = base + f'/level/{args.level}/'
    hash_ = base + '/hash/'
    reset = base + '/reset/'
    
    # auth
    s = session()
    r = s.post(auth, json={'email': args.email})
    r.raise_for_status()
    s.headers = r.json()
    
    if args.hash:
        r = s.get(hash_)
        hash_ = r.json().get('hash', 'Hash not available')
        print(hash_)
    elif args.reset:
        r = s.post(reset)
        msg = r.json().get('message', 'Unable to reset session')
        print(msg)
    else:
        r = s.get(level)
        j = r.json()
        if error := j.get('error'):
            print(error)
            sys.exit(0)        
        
        gladiators = j['numGladiators']
        guesses = j['numGuesses']
        rounds = j['numRounds']
        weapons = j['numWeapons']
        
        m = Mastermind(gladiators, guesses, rounds, weapons)

        while True:
            guess = m.next_guess()
            r = s.post(level, json={'guess': list(guess)})
            print(r.json())
            error = r.json().get('error', '')
            if error := r.json().get('error'):
                print(error)
                sys.exit(0)
            if msg := r.json().get('message', ''):
                print(msg)
                break
            score = tuple(r.json().get('response', []))
            m.prune(guess, score)
