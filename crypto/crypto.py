import argparse
import codecs
import sys
import requests

# Global values
base = "http://crypto.praetorian.com/{}"
email = ""
auth_token = None

# Used for authentication


def token(email):
    global auth_token
    if not auth_token:
        url = base.format("api-token-auth/")
        resp = requests.post(url, data={"email": email})
        auth_token = {"Authorization": "JWT " + resp.json()['token']}
        resp.close()
    return auth_token

# Fetch the challenge and hint for level n


def fetch(n):
    url = base.format("challenge/{}/".format(n))
    resp = requests.get(url, headers=token(email))
    resp.close()
    if resp.status_code != 200:
        raise Exception(resp.json()['detail'])
    return resp.json()

# Submit a guess for level n


def solve(n, guess):
    url = base.format("challenge/{}/".format(n))
    data = {"guess": guess}
    resp = requests.post(url, headers=token(email), data=data)
    resp.close()
    if resp.status_code != 200:
        raise Exception(resp.json()['detail'])
    return resp.json()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Praetorian crypto challenge.")
    parser.add_argument("-e", "--email", default="nbsantos@gmail.com",
                        help="email address")
    parser.add_argument("-l", "--level", type=int, default=0,
                        help="level to play")
    parser.add_argument("-s", "--show", action="store_true",
                        help="show cypher")
    parser.add_argument("-g", "--guess",
                        help="password guess")
    args = parser.parse_args()

    email = args.email
    level = args.level
    data = fetch(level)

    if args.show:
        print(data)
        sys.exit(0)

    hashes = {}
    guess = args.guess

    # Level 0 is a freebie and gives you the password
    guess = data['challenge']
    h = solve(level, guess)

    # If we obtained a hash add it to the dict
    if 'hash' in h:
        hashes[level] = h['hash']

    # Display all current hash
    for k, v in hashes.items():
        print("Level {}: {}".format(k, v))
