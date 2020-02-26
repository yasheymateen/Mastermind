"""Definition of the ComputerPlayer class used in the Mastermind project.

Inherits from the Player class.

"""

import random
import sys
import time

from player import Player
from solving_algorithm import generate_solutions

class ComputerPlayer(Player):

    """Mastermind ComputerPlayer class."""

    def __init__(self):
        super(ComputerPlayer, self).__init__()  # Invoke parent __init__()

        self.pause = 0.1
        self.names = ['Chell', 'GLaDOS', 'Curiosity Core', 'Turret',
                'Companion Cube', 'Wheatley', 'Cave Johnson', 'Caroline',
                'Cake']


    def __type(self, message):
        """Simulate typing on terminal."""
        sys.stdout.write(' ')
        sys.stdout.flush()
        time.sleep(self.pause * 5)
        for character in message:
            sys.stdout.write(character)
            sys.stdout.flush()
            time.sleep(self.pause)
        time.sleep(self.pause * 5)
        print


    def ready_for_game(self):
        """Reset for next game."""
        self.solutions = []
        self.colours_tried = 0
        self.solving_phase = '1'


    def ask_for_name(self, message=''):
        """Set player name."""
        self.name = random.choice(self.names)  # Choose name randomly

        if message:
            print message.rstrip(),
        self.__type(self.name)


    def choose_secret_pattern(self, message=''):
        """Set secret pattern."""
        self.secret_pattern = []

        for colour in range(self.pattern_length):  # Choose pattern randomly
            self.secret_pattern.append(random.choice(self.pattern_colours))

        if message:
            print message.rstrip(),
        self.__type("?" * self.pattern_length)  # Hide secret pattern


    def make_guess(self, message='', allow_save=False):
        """Set guess."""
        self.guess = []

        # Try each colour to determine secret pattern colours
        if self.solving_phase == '1':
            colour = list(self.pattern_colours).pop(self.colours_tried)
            for peg in range(self.pattern_length):
                self.guess.append(colour)

        # Make initial guess with found colours
        elif self.solving_phase == '2':
            for colour in self.solutions:
                self.guess.append(colour)

        # Choose guess from solutions
        elif self.solving_phase == '3':
            solution = self.solutions.pop()
            for colour in solution:
                self.guess.append(colour)

        if message:
            print message.rstrip(),
        self.__type(''.join(self.guess))


    def analyse_feedback(self, feedback):
        """Analyse given feedback to improve guesses."""
        # Check colour feedback
        if self.solving_phase == '1':
            colour = self.guess[0]
            for key in feedback:               # Has feedback
                self.solutions.append(colour)  # Add that many to solution
            self.colours_tried += 1

            # Add remaining colour to solution if can be determined
            if self.colours_tried == len(self.pattern_colours) - 1:
                colour = list(self.pattern_colours).pop(self.colours_tried)
                for peg in range(self.pattern_length - len(self.solutions)):
                    self.solutions.append(colour)

            # Determined all colours
            if len(self.solutions) == self.pattern_length:
                self.solving_phase = '2'

        # Generate initial solutions
        elif self.solving_phase == '2':
            self.solutions = generate_solutions(self.guess, feedback)
            self.solving_phase = '3'

        # Refine solutions
        elif self.solving_phase == '3':
            new_solutions = generate_solutions(self.guess, feedback)

            # Get recurring solutions

            current_solutions = set(map(tuple, self.solutions))
            new_solutions = set(map(tuple, new_solutions))

            solutions = current_solutions & new_solutions  # Set intersection
            solutions = map(list, list(solutions))

            self.solutions = solutions
