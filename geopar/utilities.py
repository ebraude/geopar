from fractions import Fraction
from decimal import Decimal

GREEK_LETTERS = 'αβγδεηθλπρστμφω'  # For names of variables

def to_fraction(a_value):
    """
    Intent: returns a Fraction equivalent of a_value

    PRE: is_instance(a_value, (int, float))
    """

    return Fraction(Decimal(str(a_value)))


def find_str_occurrences(a_str, a_substr):
    """finds all occurrences of a_substr in a_str and
    returns their indices"""

    result = list()
    index = 0
    while index < len(a_str):
        index = a_str.find(a_substr, index)
        if index == -1:
            break
        result.append(index)
        index += len(a_substr)
    return result
