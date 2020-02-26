"""Definition of the Player class used in the Mastermind project."""

from functions import remove_empty_elements

class Player(object):

    """Mastermind Player class."""

    def __init__(self):
        self.name = ''
        self.score = 0


    def __validate_input(self, message, allow_save=False):
        """Validate pattern input; return pattern on success, else None."""
        pattern = None
        while not pattern:
            if allow_save:  # Allow Ctrl-D saving
                pattern = raw_input(message)[:self.pattern_length].lower()
            else:
                try:
                    pattern = raw_input(message)[:self.pattern_length].lower()
                except EOFError:
                    print

        if len(pattern) < self.pattern_length:      # Too short
            return

        for colour in pattern:
            if colour not in self.pattern_colours:  # Invalid colour
                return

        return list(pattern)


    def remember_rules(self, pattern_length, pattern_colours):
        """Remember current game set rules."""
        self.pattern_length = pattern_length
        self.pattern_colours = pattern_colours

    
    def ready_for_game(self):
        pass


    def ask_for_name(self, message=''):
        """Set player name."""
        self.name = None
        while not self.name:
            try:
                self.name = raw_input(message).lower().capitalize()
            except EOFError:
                print


    def choose_secret_pattern(self, message=''):
        """Set secret pattern."""
        self.secret_pattern = None
        while not self.secret_pattern:
            self.secret_pattern = self.__validate_input(message)


    def make_guess(self, message='', allow_save=False):
        """Set guess."""
        self.guess = None
        while not self.guess:
            self.guess = self.__validate_input(message, allow_save)


    def is_correct(self, guess):
        """Return True if guess is correct, else False."""
        return guess == self.secret_pattern


    def prepare_feedback(self, guess, feedback_keys):
        """Prepare feedback for guess."""
        self.feedback = []

        guess = list(guess)                         # Cast from str
        secret_pattern = list(self.secret_pattern)  # Make a copy

        # Find correct pegs (feedback 'black')
        for i, colour in enumerate(guess):
            if colour == secret_pattern[i]:
                self.feedback.append(feedback_keys['correct'])
                guess[i] = secret_pattern[i] = None  # Done

        # Remove done pegs
        remove_empty_elements(guess)
        remove_empty_elements(secret_pattern)

        # Find partially correct pegs (feedback 'white')
        for i, colour in enumerate(guess):
            if colour in secret_pattern:
                self.feedback.append(feedback_keys['partially_correct'])
                secret_pattern[secret_pattern.index(colour)] = None  # Done


    def show_feedback(self, feedback_names):
        """Show feedback for current guess."""
        if self.feedback:
            feedback = []
            for key in self.feedback:
                feedback.append(feedback_names[key])  # Use feedback names
            print ' '.join(feedback)
        else:
            print 'none'


    def analyse_feedback(self, feedback):
        pass


    def show_secret_pattern(self, colour_names):
        """Show secret pattern."""
        secret_pattern = []
        for colour in self.secret_pattern:
            secret_pattern.append(colour_names[colour])  # Use colour names
        print ' '.join(secret_pattern)


    def gain_point(self):
        """Gain a point."""
        self.score += 1
