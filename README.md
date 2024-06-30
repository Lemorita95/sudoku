# sudoku
approaching sudoku as a constraint satisfaction problem (CSP) using backtrack algorithm to solve it using python.

## content
[requirements.txt](requirements.txt) - python libraries requirement

[sudoku.py](sudoku.py) - definition of game elements

[puzzle.txt](puzzle.txt) - initial state of sudoku board

[play.py](play.py) - game configuration and executable

## description
in sudoku.py file it is defined **two classes**:
1) **Node**. sudoku cell.
2) **Sudoku**. set all nodes in board. identify nodes present in puzzle.txt. method to identify node's neighbors.

in play.py:
- **SudokuCreator** class hold the game and backtrack solving algorithm.
- **main** function calls SudokuCreator methods to run the program.