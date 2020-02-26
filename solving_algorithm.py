"""Implementation of the solving algorithm used in the Mastermind project."""

from functions import remove_empty_elements

def generate_solutions(guess, feedback):
    """Generate solutions for given feedback of guess."""

    def add_solution(colour, index, length):
        """Return solution of given length with colour at index.

        >>> add_solution('b', 1, 4)
        ['', 'b', '', '']

        """
        solution = []
        for i in range(index):
            solution.append('')
        solution.append(colour)
        for i in range(length - (index + 1)):
            solution.append('')
        return solution


    def add_empty_solution(length):
        """Return empty solutions of given length.

        >>> add_empty_solution(4)
        [['', '', '', ''], ['', '', '', ''], ['', '', '', ''], ['', '', '', '']]

        """
        solutions = []
        for i in range(length):
            solutions.append([])
            for j in range(length):
                solutions[i].append('')
        return solutions


    def add_correct_solution(guess):
        """Return solutions for feedback 'black' of given guess.

        >>> add_correct_solution(['r', 'g', 'b', 'y'])
        [['r', '', '', ''], ['', 'g', '', ''], ['', '', 'b', ''], ['', '', '', 'y']]

        """
        guess_length = len(guess)
        solutions = []
        for i in range(guess_length):
            solutions.append(add_solution(guess[i], i, guess_length))
        return solutions


    def add_partially_correct_solution(guess):
        """Return solutions for feedback 'white' of given guess.

        >>> add_partially_correct_solution(['r', 'g', 'b', 'y'])
        [['', 'r', '', ''], ['', '', 'r', ''], ['', '', '', 'r'],
         ['g', '', '', ''], ['', '', 'g', ''], ['', '', '', 'g'],
         ['b', '', '', ''], ['', 'b', '', ''], ['', '', '', 'b'],
         ['y', '', '', ''], ['', 'y', '', ''], ['', '', 'y', '']]

        """
        guess_length = len(guess)
        solutions = []
        for i in range(guess_length):
            for j in range(guess_length):
                if guess[i] == guess[j]:        # Current peg position
                    continue
                solutions.append(add_solution(guess[i], j, guess_length))
        solutions = set(map(tuple, solutions))  # Remove duplicate solutions
        solutions = map(list, list(solutions))
        return solutions


    def merge_solutions(new_solutions, cumulative_solutions):
        """Merge solutions in new_solutions with those in cumulative_solutions
        whenever possible.

        To clarify,
            ['r', '', '', ''] can be merged with ['', 'g', 'b', 'y']
            ['r', '', '', ''] cannot be merged with ['c', 'g', 'b', '']

        """
        solutions = []
        for new_solution in new_solutions:
            for cumulative_solution in cumulative_solutions:
                solution_length = len(new_solution)
                for i in range(solution_length):
                    # Merge if possible
                    if new_solution[i] != '' and cumulative_solution[i] == '':
                        solution = list(cumulative_solution)
                        solution[i] = new_solution[i]
                        solutions.append(solution)
                        break
        solutions = set(map(tuple, solutions))  # Remove duplicate solutions
        solutions = map(list, list(solutions))
        return solutions


    def remove_invalid_solutions(guess, solutions):
        """Remove invalid solutions.

        Solutions are invalid if the solution and guess do not have equal numbers of each colour.

        """
        sorted_guess = sorted(guess)
        for i, solution in enumerate(solutions):
            if sorted(solution) != sorted_guess:
                solutions[i] = None  # Mark for removal
        remove_empty_elements(solutions)
        return solutions


    generate_solution = {
            'b': add_correct_solution,
            'w': add_partially_correct_solution
            }
    solutions = add_empty_solution(len(guess))  # Start with empty solutions
    for key in feedback:  # Generate and merge solutions for each feedback key
        solutions = merge_solutions(generate_solution[key](guess), solutions)
    solutions = remove_invalid_solutions(guess, solutions)
    return solutions
