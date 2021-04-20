from itertools import permutations
from typing import Tuple
from requests import session

import argparse
import logging
import sys

logging.basicConfig(level=logging.DEBUG)

# Guess is a list of variable int tuples.
Guess = Tuple[int, ...]
Score = Tuple[int, int]


class Mastermind:
    '''Implementation of Swaszek strategy to play the Mastermind game.'''

    def __init__(self, gladiators: int, weapons: int):
        self._gladiators = gladiators
        self._weapons = weapons
        self._S = None

    def prune(self, guess: Guess, score: Score):
        '''Remove from S any code that would not give the same
        response if it (the guess) were the code.'''

        self._S = (s for s in self._S if Mastermind.score(s, guess) == score)

    def next_guess(self) -> Guess:
        return next(self._S)

    def reset(self):
        '''Regenerate possible guesses.'''
        self._S = permutations(range(self._weapons), self._gladiators)

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
    parser = argparse.ArgumentParser(
        description='Play Praetorian Mastermind challenge.')
    parser.add_argument(
        '-e', '--email', default='nbsantos@gmail.com', help='email address')
    parser.add_argument('-l', '--level', type=int,
                        default=1, help='which game level to play')
    parser.add_argument('-s', '--hash', action='store_true',
                        help='print the challenge hash')
    parser.add_argument(
        '-r', '--reset', action='store_true', help='reset the game')
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
    j = r.json()
    logging.debug(j)
    s.headers = j

    if args.hash:
        r = s.get(hash_)
        j = r.json()
        logging.debug(j)
        hash_ = j.get('hash', 'Hash not available')
        print(hash_)
    elif args.reset:
        r = s.post(reset)
        j = r.json()
        logging.debug(j)
        msg = j.get('message', 'Unable to reset session')
        logging.error(msg)
    else:
        r = s.get(level)
        j = r.json()
        logging.debug(j)
        if error := j.get('error'):
            logging.error(error)
            sys.exit(0)

        gladiators = j['numGladiators']
        guesses = j['numGuesses']
        rounds = j['numRounds']
        weapons = j['numWeapons']

        logging.info('Round 1... Fight!!!')

        m = Mastermind(gladiators, weapons)
        m.reset()

        while True:
            guess = m.next_guess()
            r = s.post(level, json={'guess': list(guess)})
            j = r.json()
            logging.debug(j)
            if error := j.get('error'):
                logging.error(error)
                sys.exit(0)
            if left := j.get('roundsLeft'):  # next round
                logging.info(f'Round {rounds - left + 1}... Fight!!!')
                m.reset()  # reset class
                continue
            if msg := j.get('message'):  # next level
                logging.info(msg)
                break
            score = tuple(j.get('response', []))
            m.prune(guess, score)
