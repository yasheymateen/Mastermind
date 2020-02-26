"""Code of the graphical user interface used in the Mastermind project."""

import gtk
import pygtk
import random

from player import Player
from computer_player import ComputerPlayer

pygtk.require('2.0')

IMG_DIR = 'img/'

class PegButton(gtk.Button):
    def __init__(self, current_colours):
        super(PegButton, self).__init__()
        self.current_colours = current_colours

        self.set_size_request(48, 48)

        self.colour_image = gtk.Image()
        self.add(self.colour_image)

        self.colour = ''


    def __change_colour(self):
        colour_image = IMG_DIR + self.colour + '.png'
        self.colour_image.clear()
        self.colour_image.set_from_file(colour_image)


    def set_colour(self, colour):
        self.colour = colour
        self.__change_colour()


class MastermindGUI(object):
    def __init__(self):
        self.pause = 2
        self.save_dir = "saves/"

        self.colour_codes = ['r', 'g', 'b', 'c', 'm', 'y', 'o', 'p']
        self.feedback_keys = {'correct': 'k', 'partially_correct': 'w'}

        self.current_colours = []

        self.games = 2
        self.length = 4
        self.colours = 6
        self.turns = 12

        self.guesses = {}
        self.feedback = {}

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("Mastermind")
        self.window.connect('delete_event', self.quit)

        self.board = self.__create_board()

        self.vbox = gtk.VBox()
        self.vbox.pack_start(self.__create_menu())
        self.vbox.pack_start(self.board)

        self.window.add(self.vbox)

        self.window.show_all()


    def __create_menu(self):
        play_menu = gtk.Menu()

        play_menu_item = gtk.MenuItem("Play")
        play_menu_item.set_submenu(play_menu)

        single_player_menu_item = gtk.MenuItem("Single-player (PvC)")
        multiplayer_menu_item = gtk.MenuItem("Multiplayer (PvP)")
        duel_menu_item = gtk.MenuItem("Duel (CvC)")
        options_menu_item = gtk.MenuItem("Options")
        exit_menu_item = gtk.MenuItem("Exit")

        single_player_menu_item.connect('activate', self.play, Player(), ComputerPlayer())
        multiplayer_menu_item.connect('activate', self.play, Player(), Player())
        duel_menu_item.connect('activate', self.play, ComputerPlayer(), ComputerPlayer())
        options_menu_item.connect('activate', self.options_dialog)
        exit_menu_item.connect('activate', self.quit, self)

        # Unfinished
        single_player_menu_item.set_sensitive(False)
        duel_menu_item.set_sensitive(False)

        play_menu.append(single_player_menu_item)
        play_menu.append(multiplayer_menu_item)
        play_menu.append(duel_menu_item)
        play_menu.append(gtk.SeparatorMenuItem())
        play_menu.append(options_menu_item)
        play_menu.append(gtk.SeparatorMenuItem())
        play_menu.append(exit_menu_item)


        actions_menu = gtk.Menu()

        actions_menu_item = gtk.MenuItem("Actions")
        actions_menu_item.set_submenu(actions_menu)

        load_menu_item = gtk.MenuItem("Load")
        load_menu_item.connect('activate', self.file_dialog, "Load your game", 'load')

        load_menu_item.set_sensitive(False)  # Unfinished

        actions_menu.append(load_menu_item)


        menu_bar = gtk.MenuBar()

        menu_bar.append(play_menu_item)
        menu_bar.append(actions_menu_item)

        return menu_bar


    def __create_board(self):
        guesses_board = gtk.Table(self.turns, self.length, False)
        feedback_board = gtk.Table(self.turns, self.length, False)

        for row in range(self.turns):
            self.guesses[str(row)] = []
            for column in range(self.length):
                button = PegButton(self.current_colours)
                self.guesses[str(row)].append(button)
                guesses_board.attach(button, column, column + 1, row, row + 1)

        for row in range(self.turns):
            self.feedback[str(row)] = []
            for column in range(self.length):
                button = PegButton(self.current_colours)
                self.feedback[str(row)].append(button)
                feedback_board.attach(button, column, column + 1, row, row + 1)

        board = gtk.HBox(spacing=16)
        board.pack_start(guesses_board)
        board.pack_end(feedback_board)

        return board


    def __update_board(self, feedback):
        for i in range(len(feedback)):
            self.feedback[str(self.current_turn)][i].set_colour(feedback[i])


    def file_dialog(self, widget, title, operation_name):

        def save(filename):
            pass


        def load(filename):
            pass


        operations = {'save': save, 'load': load}

        file_dialog = gtk.FileSelection(title)
        file_dialog.set_filename(self.save_dir)

        file_dialog.ok_button.connect('clicked', operations[operation_name], file_dialog.get_filename())
        file_dialog.cancel_button.connect_object('clicked', gtk.Widget.destroy, file_dialog)

        file_dialog.run()


    def options_dialog(self, widget):

        def set_options(widget):
            self.games = games_options_entry_field.get_value_as_int()
            self.length = pegs_options_entry_field.get_value_as_int()
            self.colours = colours_options_entry_field.get_value_as_int()

            self.vbox.remove(self.board)
            self.board = self.__create_board()
            self.board.show_all()
            self.vbox.pack_start(self.board)

            options_dialog.destroy()


        options_dialog = gtk.Dialog("Options", None, gtk.DIALOG_MODAL \
                | gtk.DIALOG_DESTROY_WITH_PARENT | gtk.DIALOG_NO_SEPARATOR)

        games_options_entry_text = gtk.Label("Number of games: ")
        games_options_entry_field = gtk.SpinButton(gtk.Adjustment(2, 2, 100, 2, 2))

        pegs_options_entry_text = gtk.Label("Number of pegs: ")
        pegs_options_entry_field = gtk.SpinButton(gtk.Adjustment(4, 3, 8, 1, 1))

        colours_options_entry_text = gtk.Label("Number of colours: ")
        colours_options_entry_field = gtk.SpinButton(gtk.Adjustment(6, 3, 8, 1, 1))

        games_options_entry = gtk.HBox()
        games_options_entry.pack_start(games_options_entry_text)
        games_options_entry.pack_start(games_options_entry_field)

        pegs_options_entry = gtk.HBox()
        pegs_options_entry.pack_start(pegs_options_entry_text)
        pegs_options_entry.pack_start(pegs_options_entry_field)

        colours_options_entry = gtk.HBox()
        colours_options_entry.pack_start(colours_options_entry_text)
        colours_options_entry.pack_start(colours_options_entry_field)

        ok_button = gtk.Button("OK")
        cancel_button = gtk.Button("Cancel")

        ok_button.connect('clicked', set_options)
        cancel_button.connect_object('clicked', gtk.Widget.destroy, options_dialog)

        options_dialog.vbox.pack_start(games_options_entry)
        options_dialog.vbox.pack_start(pegs_options_entry)
        options_dialog.vbox.pack_start(colours_options_entry)

        options_dialog.action_area.pack_end(ok_button)
        options_dialog.action_area.pack_end(cancel_button)

        options_dialog.show_all()


    def name_entry_dialog(self, player, player_number):

        def set_name(widget):
            player.name = player_entry_field.get_text().lower().capitalize()
            name_entry_dialog.destroy()


        name_entry_dialog = gtk.Dialog("Enter your name", None, gtk.DIALOG_MODAL \
                | gtk.DIALOG_DESTROY_WITH_PARENT | gtk.DIALOG_NO_SEPARATOR)

        player_entry_text = gtk.Label("Player %s, what is your name? " % player_number)
        player_entry_field = gtk.Entry()

        player_entry = gtk.HBox()
        player_entry.pack_start(player_entry_text)
        player_entry.pack_start(player_entry_field)

        ok_button = gtk.Button("OK")
        ok_button.connect('clicked', set_name)
        
        name_entry_dialog.vbox.pack_start(player_entry)
        name_entry_dialog.action_area.pack_end(ok_button)

        name_entry_dialog.show_all()
        name_entry_dialog.run()


    def secret_pattern_dialog(self, codemaker):

        def set_secret_pattern(widget):
            secret_pattern = secret_pattern_field.get_text()[:self.length].lower()

            if len(secret_pattern) < self.length:
                secret_pattern_field.set_text('')
                return

            for colour in secret_pattern:
                if colour not in self.current_colours:
                    secret_pattern_field.set_text('')
                    return

            codemaker.secret_pattern = secret_pattern
            secret_pattern_dialog.destroy()


        secret_pattern_dialog = gtk.Dialog("Choose a secret pattern", None, \
                gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT \
                | gtk.DIALOG_NO_SEPARATOR)

        secret_pattern_text = gtk.Label("%s, choose a secret pattern: " % codemaker.name)
        secret_pattern_field = gtk.Entry()

        secret_pattern_entry = gtk.HBox()
        secret_pattern_entry.pack_start(secret_pattern_text)
        secret_pattern_entry.pack_start(secret_pattern_field)

        ok_button = gtk.Button("OK")
        ok_button.connect('clicked', set_secret_pattern)

        secret_pattern_dialog.vbox.pack_start(secret_pattern_entry)
        secret_pattern_dialog.action_area.pack_end(ok_button)

        secret_pattern_dialog.show_all()
        secret_pattern_dialog.run()


    def guess_dialog(self, codebreaker):

        def set_guess(widget):
            guess = guess_field.get_text()[:self.length].lower()
            
            if len(guess) < self.length:
                guess_field.set_text('')
                return

            for colour in guess:
                if colour not in self.current_colours:
                    guess_field.set_text('')
                    return

            codebreaker.guess = guess

            for i in range(self.length):
                self.guesses[str(self.current_turn)][i].set_colour(codebreaker.guess[i])

            guess_dialog.destroy()


        guess_dialog = gtk.Dialog("Make a guess", None, gtk.DIALOG_MODAL \
                | gtk.DIALOG_DESTROY_WITH_PARENT | gtk.DIALOG_NO_SEPARATOR)

        guess_text = gtk.Label("%s, make a guess: " % codebreaker.name)
        guess_field = gtk.Entry()

        guess_entry = gtk.HBox()
        guess_entry.pack_start(guess_text)
        guess_entry.pack_start(guess_field)

        save_button = gtk.Button("Save")
        save_button.connect('clicked', self.file_dialog, "Save your game", 'save')

        save_button.set_sensitive(False)  # Unfinished

        ok_button = gtk.Button("OK")
        ok_button.connect('clicked', set_guess)

        guess_dialog.vbox.pack_start(guess_entry)
        guess_dialog.action_area.pack_start(save_button)
        guess_dialog.action_area.pack_end(ok_button)

        guess_dialog.show_all()
        guess_dialog.run()


    def show_secret_pattern_dialog(self, secret_pattern):
        secret_pattern = ''.join(secret_pattern)

        secret_pattern_dialog = gtk.Dialog("Secret pattern", None, \
                gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT \
                | gtk.DIALOG_NO_SEPARATOR)

        secret_pattern_text = gtk.Label("The secret pattern is %s." % secret_pattern)

        ok_button = gtk.Button("OK")
        ok_button.connect_object('clicked', gtk.Widget.destroy, secret_pattern_dialog)

        secret_pattern_dialog.vbox.pack_start(secret_pattern_text)
        secret_pattern_dialog.action_area.pack_end(ok_button)

        secret_pattern_dialog.show_all()
        secret_pattern_dialog.run()


    def decide_roles(self, player1, player2):
        players = [player1, player2]
        random.shuffle(players)

        codemaker = players.pop()
        codebreaker = players.pop()

        return codemaker, codebreaker


    def allocate_colours(self):
        return self.colour_codes[:self.colours]


    def give_game_feedback(self, codemaker, codebreaker):
        if codemaker.is_correct(codebreaker.guess):
            text = "Correct, %s!\n" % codebreaker.name
        else:
            text = "Fail, %s. Fail.\n" % codebreaker.name

        game_feedback_dialog = gtk.Dialog("Game feedback", None, \
                gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT \
                | gtk.DIALOG_NO_SEPARATOR)

        game_feedback_text = gtk.Label(text)

        ok_button = gtk.Button("OK")
        ok_button.connect_object('clicked', gtk.Widget.destroy, game_feedback_dialog)

        game_feedback_dialog.vbox.pack_start(game_feedback_text)
        game_feedback_dialog.action_area.pack_end(ok_button)

        game_feedback_dialog.show_all()
        game_feedback_dialog.run()


    def declare_winner(self, player1, player2):
        if player1.score > player2.score:
            winner = player1
        elif player2.score > player1.score:
            winner = player2
        else:
            winner = None

        if winner:
            text = "%s wins! Good job!" % winner.name
        else:
            text = "It's a tie! Good job!"

        winner_dialog = gtk.Dialog("Winner", None, gtk.DIALOG_MODAL \
                | gtk.DIALOG_DESTROY_WITH_PARENT | gtk.DIALOG_NO_SEPARATOR)

        winner_text = gtk.Label(text)

        ok_button = gtk.Button("OK")
        ok_button.connect_object('clicked', gtk.Widget.destroy, winner_dialog)

        winner_dialog.vbox.pack_start(winner_text)
        winner_dialog.action_area.pack_end(ok_button)

        winner_dialog.show_all()
        winner_dialog.run()


    def is_last_turn(self):
        return self.current_turn == self.turns - 1


    def is_last_game(self):
        return self.current_game == self.games - 1


    def play(self, widget, player1, player2):
        self.current_colours = self.allocate_colours()
        self.current_game = 0

        self.name_entry_dialog(player1, "1")
        self.name_entry_dialog(player2, "2")

        codemaker, codebreaker = self.decide_roles(player1, player2)

        codemaker.remember_rules(self.length, self.current_colours)
        codebreaker.remember_rules(self.length, self.current_colours)

        for game in range(self.current_game, self.games):
            self.current_game = game
            self.current_turn = 0

            self.vbox.remove(self.board)
            self.board = self.__create_board()
            self.board.show_all()
            self.vbox.pack_end(self.board)

            self.secret_pattern_dialog(codemaker)

            for turn in range(self.current_turn, self.turns):
                self.current_turn = turn

                self.guess_dialog(codebreaker)

                if codemaker.is_correct(codebreaker.guess):
                    codemaker.prepare_feedback(codebreaker.guess, self.feedback_keys)
                    self.__update_board(codemaker.feedback)
                    print "Breaking"
                    break

                else:
                    codemaker.prepare_feedback(codebreaker.guess, self.feedback_keys)
                    codebreaker.analyse_feedback(codemaker.feedback)

                    codemaker.gain_point()
                    if self.is_last_turn():
                        codemaker.gain_point()

                    self.__update_board(codemaker.feedback)

            self.show_secret_pattern_dialog(codemaker.secret_pattern)
            self.give_game_feedback(codemaker, codebreaker)

            if self.is_last_game():
                self.declare_winner(codemaker, codebreaker)
            else:
                codemaker, codebreaker = codebreaker, codemaker


    def quit(self, widget, data):
        gtk.main_quit()
        return False


    def main(self):
        gtk.main()
