import unittest
from typing import List
from minimax import find_best_move
from rota import RotaBoard, RotaPlayer
from board import Move


class TTTMinimaxTestCase(unittest.TestCase):
    def test_easy_position(self):
        # win in 1 move
        to_win_easy_position: List[RotaPlayer] = [RotaPlayer.P, RotaPlayer.C, RotaPlayer.P,
                                                  RotaPlayer.E, RotaPlayer.E, RotaPlayer.C,
                                                  RotaPlayer.P, RotaPlayer.E, RotaPlayer.C]
        test_board1: RotaBoard = RotaBoard(to_win_easy_position, RotaPlayer.P)
        answer1: Move = find_best_move(test_board1)
        self.assertEqual(answer1, (0, 4))

    def test_block_position(self):
        # must block C's win
        to_block_position: List[RotaPlayer] = [RotaPlayer.P, RotaPlayer.E, RotaPlayer.C,
                                               RotaPlayer.E, RotaPlayer.C, RotaPlayer.E,
                                               RotaPlayer.E, RotaPlayer.P, RotaPlayer.E]
        test_board2: RotaBoard = RotaBoard(to_block_position, RotaPlayer.P)
        answer2: Move = find_best_move(test_board2)
        self.assertEqual(answer2, (-1, 6))

    #def test_hard_position(self):
        ## find the best move to win 2 moves
        #to_win_hard_position: List[RotaPlayer] = [RotaPlayer.P, RotaPlayer.E, RotaPlayer.E,
                                                  #RotaPlayer.E, RotaPlayer.E, RotaPlayer.C,
                                                  #RotaPlayer.C, RotaPlayer.P, RotaPlayer.E]
        #test_board3: RotaBoard = RotaBoard(to_win_hard_position, RotaPlayer.P)
        #answer3: Move = find_best_move(test_board3)
        #self.assertEqual(answer3, (0, 1))


if __name__ == '__main__':
    unittest.main()


