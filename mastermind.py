#!/usr/bin/env python

"""The Mastermind project."""

import signal
import sys

from mastermind_game import MastermindGame
from mastermind_gui import MastermindGUI
from signal_handler import quit_game

def main():
    """Main program loop."""
    signal.signal(signal.SIGINT, quit_game)  # Exit gracefully

    try:
        mode = sys.argv[1]
    except IndexError:
        mode = '-t'

    if mode == '-t':  # Text mode
        mastermind = MastermindGame()
        mastermind.main()
    elif mode == '-g':  # Graphical mode
        mastermind_gui = MastermindGUI()
        mastermind_gui.main()
    else:
        print "Usage: %s [-t|-g]" % sys.argv[0]


if __name__ == '__main__':
    main()
