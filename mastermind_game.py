"""Implementation of the game mechanics, logic and text interface of the Mastermind project."""

import os
import pickle
import random
import sys
import time

from player import Player
from computer_player import ComputerPlayer
from board import Board
from functions import is_odd

class MastermindGame(object):

    """MastermindGame class."""

    def __init__(self):
        self.pause = 2
        self.width = 80

        self.min = 3
        self.max = 8

        self.save_dir = 'saves'

        self.modes = ['s', 'm', 'd', 'l', 'i', 'o', 'q']
        self.settings = {'g': 'games', 'p': 'length', 'c': 'colours', 'b': None}

        self.colour_codes = ['r', 'g', 'b', 'c', 'm', 'y', 'o', 'p']
        self.feedback_keys = {'correct': 'b', 'partially_correct': 'w'}

        self.colour_names = {'r': 'red', 'g': 'green', 'b': 'blue', 'c': 'cyan', 'm': 'magenta', 'y': 'yellow', 'o': 'orange', 'p': 'purple'}
        self.feedback_names = {'b': 'black', 'w': 'white'} 

        self.games = 2
        self.length = 4
        self.colours = 6
        self.turns = 12

        self.guesses = {}
        self.feedback = {}


    def __clear(self):
        """Clear screen."""
        os.system('clear')


    def __pause(self, pause):
        """Pause game."""
        time.sleep(pause)


    def main(self):
        """Main game loop."""
        while True:
            mode = self.menu()
            if mode == 's':
                self.play(player1=Player(), player2=ComputerPlayer())
            elif mode == 'm':
                self.play(player1=Player(), player2=Player())
            elif mode == 'd':
                self.play(player1=ComputerPlayer(), player2=ComputerPlayer())
            elif mode == 'l':
                self.load_game()
            elif mode == 'i':
                self.instructions()
            elif mode == 'o':
                self.options()
            elif mode == 'q':
                self.quit()


    def menu(self):
        """Menu screen."""
        while True:
            self.__clear()

            print "Mastermind"
            print "-" * self.width
            print "[S] Single-player (PvC)"
            print "[M] Multiplayer (PvP)"
            print "[D] Duel (CvC)"
            print "[L] Load"
            print "[I] Instructions"
            print "[O] Options"
            print "[Q] Quit"
            print "-" * self.width
            print

            mode = None
            while mode not in self.modes:  # Prompt for mode
                try:
                    mode = raw_input("> ")[0].lower()
                except IndexError:
                    mode = None
                except EOFError:
                    print
            return mode


    def instructions(self):
        """Instructions screen."""
        self.__clear()

        print "Mastermind : Instructions"
        print "-" * self.width
        print "Mastermind is played by two players: the codemaker and the codebreaker."
        print "It is played in a pre-agreed number of games consisting of 12 turns each."
        print
        print "The codemaker forms a secret pattern which the codebreaker must deduce within a game."
        print "The secret pattern consists of 3-8 pegs, allowing duplicates, each of which can be of 3-8 colours."
        print "The available colours are: red, green, blue, cyan, magenta, yellow, orange and purple."
        print
        print "The codemaker provides feedback on the codebreaker's guesses by:"
        print "    - placing a black key code for each code which has the correct colour and position"
        print "    - placing a white key code for each code which has the correct colour but wrong position"
        print
        print "The codemaker gains a point for each guess made by the codebreaker."
        print "The codemaker gains an extra point if the codebreaker fails to solve the pattern."
        print "The players then take turns playing as the codemaker and codebreaker."
        print
        print "The player with the most points wins."
        print
        print "Colours can be specified by entering the first character of each colour."
        print "    Example > Guess: rgby"
        print
        print "For a given game played with n pegs, if more than n colours is entered, only the first n are taken as the guess."
        print "-" * self.width
        print

        sys.stdout.flush()
        os.system('read -rs -n 1')  # Exit on key press


    def options(self):
        """Options screen."""
        while True:
            self.__clear()

            print "Mastermind : Options"
            print "-" * self.width
            print "[G] Number of games   (must be even, default=2) : %d" % self.games
            print "[P] Number of pegs    (3-8, default=4)          : %d" % self.length
            print "[C] Number of colours (3-8, default=6)          : %d" % self.colours
            print "[B] Back"
            print "-" * self.width
            print

            setting = None
            settings = self.settings.keys()
            while setting not in settings:  # Prompt for setting
                try:
                    setting = raw_input("> ")[0].lower()
                except IndexError:
                    setting = None
                except EOFError:
                    print

            if setting == 'b':  # Back
                break

            while True:
                try:
                    # Prompt for setting value
                    value = int(raw_input(">> Enter a new value for %s: " % setting.upper()))
                    # Invalid value
                    if setting == 'g' and is_odd(value):
                        raise 'ParityError'
                    elif (setting == 'p' or setting == 'c') and (value < self.min or value > self.max):
                        raise 'RangeError'
                except EOFError:
                    print 
                except (ValueError, 'ParityError', 'RangeError'):
                    pass
                else:
                    break

            setattr(self, self.settings[setting], value)  # Set value of setting

    
    def quit(self):
        """Quit game."""
        self.__clear()
        print "Thank you for playing!"
        sys.exit()


    def save_game(self, codemaker, codebreaker):
        """Save game screen."""
        confirm = None
        while confirm != 'y' and confirm != 'n':  # Confirm saving
            try:
                confirm = raw_input("\n\nWould you like to save your game (Y/n)? ")[0].lower()
            except EOFError:
                print
            except IndexError:
                pass
        if confirm == 'n':
            print
            return

        if not os.path.isdir(self.save_dir):  # Make save directory if none exists
            os.mkdir(self.save_dir)

        # Get saved games
        saved_games = os.listdir(self.save_dir)
        saved_names = list(saved_games)
        if saved_games:
            for i, saved_name in enumerate(saved_names):
                saved_names[i] = saved_name.rstrip('.sav')
            print "Saved games found:  %s" % '  '.join(saved_names)
 
        save_name = None
        while not save_name:
            try:
                # Prompt for save name
                save_name = raw_input("Enter a name for your save: ").lower()
                if save_name == '':  # Cancel
                    print
                    return
            except EOFError:
                print

        if save_name in saved_names:  # If save exists
            confirm = None
            while confirm != 'y' and confirm != 'n':  # Confirm overwriting
                try:
                    confirm = raw_input("%s already exists. Would you like to overwrite (y/N)? " % save_name)[0].lower()
                except EOFError:
                    print
                except IndexError:
                    pass
            if confirm == 'n':
                print
                return

        # Save game
        save_name = os.path.join(self.save_dir, save_name + '.sav')
        self.save(save_name, codemaker, codebreaker)


    def load_game(self):
        """Load game screen."""
        self.__clear()

        print "Mastermind"
        print "-" * self.width
        print "Searching saved games directory...\n"

        # Get saved games
        saved_games = os.listdir(self.save_dir)
        if not saved_games:
            print "No saved games found. Aborting..."
            self.__pause(self.pause)
            return

        # Show saved games
        saved_names = list(saved_games)
        for i, saved_name in enumerate(saved_names):
            saved_names[i] = saved_name.rstrip('.sav')
        print "Saved games found:  %s\n" % '  '.join(saved_names)

        load_name = None
        while load_name not in saved_names:
            try:
                # Prompt for load name
                load_name = raw_input("Enter the name of the save you want to load: ").lower()
                if load_name == '':  # Cancel
                    return
            except EOFError:
                print

        # Load game
        load_name = os.path.join(self.save_dir, load_name + '.sav')
        codemaker, codebreaker = self.load(load_name)
        self.play(codemaker=codemaker, codebreaker=codebreaker, load_game=True)

    
    def save(self, save_name, codemaker, codebreaker):
        """Save game."""
        try:
            save_file = open(save_name, 'w')
        except IOError:
            print "Game cannot be saved. Aborting...\n"
            return

        try:
            pickle.dump(self.games, save_file)
            pickle.dump(self.length, save_file)
            pickle.dump(self.colours, save_file)
            pickle.dump(self.turns, save_file)

            pickle.dump(self.guesses, save_file)
            pickle.dump(self.feedback, save_file)
            pickle.dump(self.board, save_file)

            pickle.dump(self.current_colours, save_file)
            pickle.dump(self.current_game, save_file)
            pickle.dump(self.current_turn, save_file)

            pickle.dump(codemaker, save_file)
            pickle.dump(codebreaker, save_file)

        except pickle.PicklingError:
            print "Game cannot be saved. Aborting...\n"

        else:
            print "Game saved successfully.\n"

        save_file.close()


    def load(self, load_name):
        """Load game."""
        try:
            load_file = open(load_name, 'r')
        except IOError:
            print "Game cannot be loaded. Aborting..."
            self.__pause(self.pause)
            return

        try:
            self.games = pickle.load(load_file)
            self.length = pickle.load(load_file)
            self.colours = pickle.load(load_file)
            self.turns = pickle.load(load_file)
            
            self.guesses = pickle.load(load_file)
            self.feedback = pickle.load(load_file)
            self.board = pickle.load(load_file)

            self.current_colours = pickle.load(load_file)
            self.current_game = pickle.load(load_file)
            self.current_turn = pickle.load(load_file)

            codemaker = pickle.load(load_file)
            codebreaker = pickle.load(load_file)

        except pickle.UnpicklingError:
            print "Game cannot be loaded. Aborting..."
            self.__pause(self.pause)
            load_file.close()

        else:
            load_file.close()
            return codemaker, codebreaker


    def display_game_header(self, codemaker, codebreaker):
        """Display game header.

        The header shown in the secret pattern choice screen.

        """
        print "Mastermind : Play : Game (%d/%d)" % (self.current_game + 1, self.games)
        print "-" * self.width
        print "%s will be playing as the codemaker" % codemaker.name
        print "%s will be playing as the codebreaker" % codebreaker.name
        print
        print "Using %d pegs" % self.length
        print "Using %d colours:" % len(self.current_colours),
        for colour in self.current_colours:
            print self.colour_names[colour],
        print
        print "-" * self.width
        print


    def display_turn_header(self, codemaker, codebreaker, last_turn=False):
        """Display turn header.

        The header shown on each turn.

        """
        if last_turn:  # Hide turn number on last turn
            print "Mastermind : Play : Game (%d/%d)" % (self.current_game + 1, self.games)
        else:
            print "Mastermind : Play : Game (%d/%d) : Turn (%d/%d)" % (self.current_game + 1, self.games, self.current_turn + 1, self.turns)
        print "-" * self.width
        print "(Codemaker) %-15s : %-7d" % (codemaker.name, codemaker.score),
        print "(Codebreaker) %-15s : %-7d" % (codebreaker.name, codebreaker.score)
        print "Pegs : %-30d" % self.length,
        print "Colours: %-30s" % ''.join(self.current_colours)
        print
        print "Attention, humans: Press Ctrl-D during your turn to save."
        print "                   Press Ctrl-C anytime to quit."
        print "-" * self.width
        print 


    def name_players(self, player1, player2):
        """Player names input screen."""
        print "Mastermind : Play : Enter your names"
        print "-" * self.width

        player1.ask_for_name("Hi Player 1! What is your name? ")
        player2.ask_for_name("Hi Player 2! What is your name? ")

        while player1.name == player2.name:  # Do not allow same names
            print "\nWhoops! Sorry but you can't have the same name.\n"
            player1.ask_for_name("Change your name, Player 1: ")
            player2.ask_for_name("Change your name, Player 2: ")


    def decide_roles(self, player1, player2):
        """Decide roles randomly."""
        players = [player1, player2]
        random.shuffle(players)

        codemaker = players.pop()
        codebreaker = players.pop()

        return codemaker, codebreaker


    def allocate_colours(self):
        """Return colours for current game set.

        Based on number of colours setting.

        """
        return self.colour_codes[:self.colours]

    
    def record_turn(self, guess, feedback):
        """Record current guess and feedback."""
        self.guesses[str(self.current_game)].append(guess)
        self.feedback[str(self.current_game)].append(feedback)


    def give_game_feedback(self, codemaker, codebreaker):
        """Give codebreaker feedback for current game."""
        if codemaker.is_correct(codebreaker.guess):
            print "Correct, %s!\n" % codebreaker.name
        else:
            print "Fail, %s. Fail.\n" % codebreaker.name


    def declare_winner(self, player1, player2):
        """Declare winner of current game set, else tie."""
        if player1.score > player2.score:
            winner = player1
        elif player2.score > player1.score:
            winner = player2
        else:
            winner = None

        if winner:
            print "%s wins! Good job!" % winner.name
        else:
            print "It's a tie! Good job!"

    
    def is_last_turn(self):
        """Return True if last turn, else False."""
        return self.current_turn == self.turns - 1


    def is_last_game(self):
        """Return True if last game, else False."""
        return self.current_game == self.games - 1

    
    def play(self, player1=None, player2=None, codemaker=None, codebreaker=None, load_game=False):
        """Main game mechanics and logic loop."""
        if not load_game:  # Initialise new game set
            self.current_colours = self.allocate_colours()
            self.current_game = 0

            self.__clear()

            self.name_players(player1, player2)
            codemaker, codebreaker = self.decide_roles(player1, player2)

            # Remember current game set rules
            codemaker.remember_rules(self.length, self.current_colours)
            codebreaker.remember_rules(self.length, self.current_colours)

        for game in range(self.current_game, self.games):

            if not load_game:  # Initialise new game
                # Create new record entry
                self.guesses[str(game)] = []
                self.feedback[str(game)] = []

                self.current_game = game
                self.current_turn = 0

                # Initialise board
                self.board = Board(self.length, self.width, self.turns)

                # Prepare for next game
                codemaker.ready_for_game()
                codebreaker.ready_for_game()

                self.__clear()
                self.display_game_header(codemaker, codebreaker)

                print "%s, DON'T LOOK!" % codebreaker.name.upper()
                codemaker.choose_secret_pattern("%s, choose a secret pattern: " % codemaker.name)

            for turn in range(self.current_turn, self.turns):

                if load_game:
                    load_game = False  # Continue normally after loading

                self.current_turn = turn

                self.__clear()
                self.display_turn_header(codemaker, codebreaker)
                self.board.display()

                while True:  # Prompt for guess
                    try:
                        codebreaker.make_guess("%s, make a guess: " % codebreaker.name, allow_save=True)
                    except EOFError:  # Ctrl-D is pressed
                        self.save_game(codemaker, codebreaker)
                    else:
                        break

                if codemaker.is_correct(codebreaker.guess):  # Correct guess
                    codemaker.prepare_feedback(codebreaker.guess, self.feedback_keys)
                    self.record_turn(codebreaker.guess, codemaker.feedback)
                    self.board.update(turn, codebreaker.guess, codemaker.feedback)
                    break

                else:
                    codemaker.prepare_feedback(codebreaker.guess, self.feedback_keys)
                    print "%s's feedback is" % codemaker.name,
                    codemaker.show_feedback(self.feedback_names)
                    codebreaker.analyse_feedback(codemaker.feedback)

                    codemaker.gain_point()
                    if self.is_last_turn():
                        codemaker.gain_point()

                    self.record_turn(codebreaker.guess, codemaker.feedback)
                    self.board.update(turn, codebreaker.guess, codemaker.feedback)

                    self.__pause(self.pause)

            self.__clear()
            self.display_turn_header(codemaker, codebreaker, last_turn=True)
            self.board.display()

            print "%s's secret pattern is" % codemaker.name,
            codemaker.show_secret_pattern(self.colour_names)
            self.__pause(self.pause * 1.5)

            self.give_game_feedback(codemaker, codebreaker)
            self.__pause(self.pause)

            if self.is_last_game():
                self.declare_winner(codemaker, codebreaker)
                self.__pause(self.pause)
            else:
                codemaker, codebreaker = codebreaker, codemaker  # Swap roles
