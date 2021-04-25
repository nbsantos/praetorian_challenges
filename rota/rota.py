from __future__ import annotations
from typing import List
from enum import Enum
from board import Player, Board, Move


class RotaPlayer(Player, Enum):
    P = "p"
    C = "c"
    E = "-" # stand-in for empty

    @property
    def opposite(self) -> RotaPlayer:
        if self == RotaPlayer.P:
            return RotaPlayer.C
        elif self == RotaPlayer.C:
            return RotaPlayer.P
        else:
            return RotaPlayer.E

    def __str__(self) -> str:
        return self.value


class RotaBoard(Board):
    def __init__(self, position: List[RotaPlayer] = [RotaPlayer.E] * 9, turn: RotaPlayer = RotaPlayer.P) -> None:
        self.position: List[RotaPlayer] = position
        self._turn: RotaPlayer = turn

    @property
    def turn(self) -> Player:
        return self._turn

    def move(self, location: Move) -> Board:
        temp_position: List[RotaPlayer] = self.position.copy()
        temp_position[location] = self._turn
        return RotaBoard(temp_position, self._turn.opposite)

    @property
    def legal_moves(self, setup: bool = False) -> List[Move]:
        empty = [Move(l) for l in range(len(self.position)) if self.position[l] == RotaPlayer.E]
        if setup:
            return empty
        else:
            return []

    @property
    def is_win(self) -> bool:
        # three row, three column, and then two diagonal checks
        return self.position[0] == self.position[4] and self.position[0] == self.position[8] and self.position[0] != RotaPlayer.E or \
               self.position[1] == self.position[4] and self.position[1] == self.position[7] and self.position[1] != RotaPlayer.E or \
               self.position[2] == self.position[4] and self.position[2] == self.position[6] and self.position[2] != RotaPlayer.E

    def evaluate(self, player: Player) -> float:
        if self.is_win and self.turn == player:
            return -1
        elif self.is_win and self.turn != player:
            return 1
        else:
            return 0

    def __repr__(self) -> str:
        return f"""
        {self.position[0]}|{self.position[1]}|{self.position[2]}
        -----
        {self.position[3]}|{self.position[4]}|{self.position[5]}
        -----
        {self.position[6]}|{self.position[7]}|{self.position[8]}
        """
