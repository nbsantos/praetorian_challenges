from itertools import permutations
import json
import requests


def _score(guess, code):
    s = [0, 0]
    for i, w in enumerate(guess):
        if w in code:
            s[0] += 1
        if w == code[i]:
            s[1] += 1
    return s


def prune(guess, S, resp):
    '''Remove from S any code that would not give the same response if it (the guess) were the code.'''
    new_S = list()
    for s in S:
        if _score(s, guess) == resp:
            new_S.append(s)
    return new_S


if __name__ == '__main__':
    email = 'nbsantos@gmail.com'

    r = requests.post(
        'https://mastermind.praetorian.com/api-auth-token/', data={'email': email})

    headers = r.json()  # > {'Auth-Token': 'AUTH_TOKEN'}
    headers['Content-Type'] = "application/json"

    # Interacting with the game
    r = requests.get(
        'https://mastermind.praetorian.com/level/1/', headers=headers)
    # > {'numGladiators': 4, 'numGuesses': 8, 'numRounds': 1, 'numWeapons': 6}
    level = r.json()

    S = list(map(list, permutations(
        range(1, level['numWeapons'] + 1), level['numGladiators'])))

    for _ in range(level['numGuesses']):
        guess = S[0]

        r = requests.post('https://mastermind.praetorian.com/level/1/',
                          data=json.dumps({'guess': guess}), headers=headers)
        resp = r.json()  # > {'response': [2, 1]}

        if resp['response'] == [4, 4]:
            break

        S = prune(guess, S, resp["response"])
