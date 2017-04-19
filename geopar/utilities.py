from fractions import Fraction
from decimal import Decimal

GREEK_LETTERS = 'αβγδεηθλπρστμφω'  # For names of variables

def to_fraction(a_value):
    """
    Intent: returns a Fraction equivalent of a_value

    PRE: is_instance(a_value, (int, float))
    """

    return Fraction(Decimal(str(a_value)))
