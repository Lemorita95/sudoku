class Node():

    def __init__(self, i, j):
        """
        Create a new node with position
        """
        self.i = i
        self.j = j
        self.box = [(i // 3), (j // 3)]

    def __hash__(self):
        return hash((self.i, self.j))
    
    def __eq__(self, other):
        return (
            (self.i == other.i) and
            (self.j == other.j)
        )
    
    def __str__(self):
        return f"({self.i}, {self.j})"

    def __repr__(self):
        return f"Node({self.i}, {self.j})"

class Sudoku():

    def __init__(self, puzzle_file):

        # structure of sudoku
        self.height = 9
        self.width = 9
        self.numbers = [x for x in range(1, 10)]

        with open(puzzle_file) as file:
            contents = file.read()

            # Reshape the list into individual rows
            # file starts from above, Sudoku indexing from below
            rows = [contents[i:i+9] for i in range(0, len(contents), 9)][::-1]

            # values filled from puzzle.txt
            self.predefined = {}
            for row, row_value in enumerate(rows):
                for col, col_value in enumerate(row_value):
                    if col_value == '.':
                        continue
                    else:
                        self.predefined[Node(row, col)] = int(col_value)

        # nodes set
        self.nodes = set()
        for i in range(self.height):
            for j in range(self.width):

                self.nodes.add(Node(i, j))

    def neighbors(self, node):
        """"
        for a giving node, return all neighbors (box and cross)
        """
        return set(
            n for n in self.nodes
            if node != n and
            (
                (node.i == n.i or 
                node.j == n.j) or
                (node.box == n.box)
            )
        )