from sudoku import *

import time


class SudokuCreator():

    def __init__(self, sudoku):
        """"
        Create sudoku CSP
        """
        self.sudoku = sudoku

        self.assigned = self.sudoku.predefined

        self.domains = {}
        for node in self.sudoku.nodes:
            if node in self.assigned.keys():
                self.domains[node] = [self.assigned[node]]
            # otherwise, fill with possibilities
            else:
                self.domains[node] = self.sudoku.numbers.copy()


    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        for k, v in assignment.items():
            print(f"{k}: {v}")

    def display_problem(self):
        """"
        display problem initial values
        backtrack at self.solve() changes self.assigned
        so call this function after and before solf.solve() returns initial and final state
        """
        for j in reversed(range(self.sudoku.height)):
            for i in range(self.sudoku.width):
                try:
                    print(self.assigned[Node(i, j)], end='')
                except KeyError:
                    print(" ", end='')

                # right block separator
                if i in [2, 5]:
                    print(" | ", end='')
            print()

            # bottom block separator
            if j in [6, 3]:
                print("--- + --- + ---")

    def solve(self):
        """
        Enforce arc consistency and solve CSP
        No node consistency since domain already in correct range
        """
        self.ac3()
        return self.backtrack(self.assigned)
    
    def revise(self, x, y):
        """"
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """

        # initialize revised as false
        revised = False

        # for each value in x's domain set
        for vx in self.domains[x].copy():
            # If no value in y's domain satisfies the constraint between x and y, remove vx
            if not any(vx != vy for vy in self.domains[y]):
                self.domains[x].remove(vx)
                revised = True
        
        return revised
    
    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # initialize queue, only existing arcs
        if arcs is None:
            queue = set()
            for node in self.sudoku.nodes:
                for neighbor in self.sudoku.neighbors(node):
                    queue.add((node, neighbor))
        else:
            queue = set(arcs)

        # while queue not empty
        while queue:

            # dequeue random element in queue
            X, Y = queue.pop()

            # if arc consistency of X regarding Y makes revision
            if self.revise(X, Y):
                # if no domain left, cannot solve
                if len(self.domains[X]) == 0:
                    return False
                
                # since X domains changed, add its neighbors on queue
                for Z in self.sudoku.neighbors(X):
                    if Z != Y:
                        queue.add((Z, X))
            
        return True
    
    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """

        # each variable assigned at assignment
        assigned = [k for k in assignment.keys()]

        for variable in self.sudoku.nodes:
            if variable not in assigned:
                return False
            
        return True
    
    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        assigned = [k for k in assignment.keys()]

        # arc constrait within assignment --> same value on neighbors
        for k, v in assignment.items():

            # neighbors
            neighbors = self.sudoku.neighbors(k)

            # intersection neighbors and assined
            intersect = set(neighbors).intersection(assigned)

            # for each intersection
            for x in intersect:
                # if same number assigned for neighbors
                if v == assignment[x]:
                    return False
        
        # if reaches this point, it is consistent
        return True

    def order_domain_values(self, node, assignment):
        """
        Return the domain values for `var` ordered by the least constraining value heuristic.
        """
        return sorted(self.domains[node], key=lambda val: self.num_constraints(node, val, assignment))

    def num_constraints(self, node, val, assignment):
        """
        Return the number of constraints a value imposes on other variables.
        """
        count = 0
        for neighbor in self.sudoku.neighbors(node):
            if neighbor not in assignment and val in self.domains[neighbor]:
                count += 1
        return count
    
    def select_unassigned_node(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """

        unassigned = [node for node in self.sudoku.nodes if node not in assignment]
        return min(unassigned, key=lambda node: (len(self.domains[node]), -len(self.sudoku.neighbors(node))))

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """       

        # if assignment is complete, returns it
        if self.assignment_complete(assignment):
            return assignment
        
        # select unassigned node
        node = self.select_unassigned_node(assignment)

        # for each alue in its domain
        for value in self.order_domain_values(node, assignment):
            # include var to assignment
            assignment[node] = value
            
            # check for consistency
            if self.consistent(assignment):

                # create a copy of the domains to restore later if needed
                local_copy = self.domains.copy()

                # ensure arc consistency of neighbor regarding no assignment
                if self.ac3([(node, neighbor) for neighbor in self.sudoku.neighbors(node)]):

                    # call recursively to solve the rest of variables
                    result = self.backtrack(assignment)

                    # if backtrack does not return failure
                    if result is not None:
                        return result
                    
                # restore the domains to their previous state
                self.domains = local_copy

            # delete var assignment and try again
            del assignment[node]

        # unable to complete assignment
        return None


def main():

    # Generate Sudoku
    sudoku = Sudoku('puzzle.txt')
    creator = SudokuCreator(sudoku)

    # display problem before solution
    creator.display_problem()
    print()

    # solve problem
    assignment = creator.solve()

    if assignment is None:
        print("No solution.")
    else:
        # display problem after solution
        creator.display_problem()


if __name__ == "__main__":
    start_time = time.time()
    print()
    main()
    print()
    print("--- %s seconds ---" % (time.time() - start_time))
    print()