from board import Board
from rules import valid_move, completed_boxes


class DotsAndBoxes:
    def __init__(self):
        self.board = Board()
        self.current = 0
        self.scores = [0, 0]

        # Stores information about the previous valid move
        self.history = []

    def undo_last_move(self):
        """Undo the most recent valid move."""
        if not self.history:
            print("Nothing to undo.")
            return

        last = self.history.pop()

        # Remove the line from the board
        self.board.remove_line(
            last["orientation"],
            last["row"],
            last["col"]
        )

        # Restore score and player turn
        self.scores = last["scores"].copy()
        self.current = last["current"]

        print("Last move undone.")

    def run(self):
        print("Dots and Boxes")
        print("Enter moves as H row col or V row col.")
        print("Rows and columns start at 0.")
        print("Example: H 0 1")
        print("Enter UNDO to undo the previous valid move.")

        while not self.board.is_complete():
            self.board.display(self.scores, self.current)

            raw = input(
                f"Player {self.current + 1}, move: "
            ).strip().upper()

            # New UNDO feature
            if raw == "UNDO":
                self.undo_last_move()
                continue

            parts = raw.split()

            if len(parts) != 3:
                print("Invalid format.")
                continue

            
            orientation, row_text, col_text = parts

            try:
                row = int(row_text)
                col = int(col_text)
            except ValueError:
                print("Row and column must be valid integers.")
                continue

            if not valid_move(
                self.board,
                orientation,
                row,
                col
            ):
                print("Invalid or already-used move.")
                continue

            # Save the state BEFORE making the move
            self.history.append({
                "orientation": orientation,
                "row": row,
                "col": col,
                "scores": self.scores.copy(),
                "current": self.current
            })

            before = set(self.board.completed)

            self.board.add_line(
                orientation,
                row,
                col
            )

            newly_completed = completed_boxes(
                self.board,
                before
            )

            if newly_completed:
                self.scores[self.current] += newly_completed

                print(
                    f"Player {self.current + 1} completed "
                    f"{newly_completed} box(es) and plays again."
                )
            else:
                self.current = 1 - self.current

        self.board.display(
            self.scores,
            self.current
        )

        print("Game over!")

        if self.scores[0] == self.scores[1]:
            print("The game is a draw.")
        else:
            winner = (
                1
                if self.scores[0] > self.scores[1]
                else 2
            )
            print(f"Player {winner} wins!")