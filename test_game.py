import unittest

from board import Board
from rules import valid_move, completed_boxes


class TestDotsAndBoxes(unittest.TestCase):

    def test_valid_horizontal_move(self):
        board = Board()

        self.assertTrue(valid_move(board, "H", 0, 0))

        board.add_line("H", 0, 0)

        self.assertTrue(board.horizontal[0][0])


    def test_valid_vertical_move(self):
        board = Board()

        self.assertTrue(valid_move(board, "V", 0, 0))

        board.add_line("V", 0, 0)

        self.assertTrue(board.vertical[0][0])


    def test_repeated_move_is_invalid(self):
        board = Board()

        board.add_line("H", 0, 0)

        self.assertFalse(valid_move(board, "H", 0, 0))


    def test_box_completion(self):
        board = Board()

        # Create three sides of the top-left box
        board.add_line("H", 0, 0)
        board.add_line("H", 1, 0)
        board.add_line("V", 0, 0)

        before = set(board.completed)

        # Fourth side completes the box
        board.add_line("V", 0, 1)

        newly_completed = completed_boxes(board, before)

        self.assertEqual(newly_completed, 1)
        self.assertIn((0, 0), board.completed)


    def test_end_of_game(self):
        board = Board()

        # Fill every horizontal line
        for row in range(board.rows + 1):
            for col in range(board.cols):
                board.add_line("H", row, col)

        # Fill every vertical line
        for row in range(board.rows):
            for col in range(board.cols + 1):
                board.add_line("V", row, col)

        self.assertTrue(board.is_complete())


if __name__ == "__main__":
    unittest.main()