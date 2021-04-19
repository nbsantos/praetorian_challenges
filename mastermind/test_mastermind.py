# test_mastermind.py

import pytest
from mastermind import Mastermind

def test_S_creation():
    m = Mastermind(weapons=6, gladiators=4)