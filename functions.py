"""Definitions of the helper functions used in the Mastermind project."""

def is_odd(number):
    """Return True if number is odd, else False."""
    return number % 2 != 0


def remove_empty_elements(lst):
    """Remove all None in lst."""
    while None in lst:
        lst.remove(None)
