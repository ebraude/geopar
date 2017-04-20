from decimal import Decimal
from fractions import Fraction
from operator import add, sub
import copy

from geopar.utilities import to_fraction, GREEK_LETTERS

__author__ = 'satbek'  # modified by Eric Braude starting 03/15/17


class Angle:
    """
    A (geometric) angle as linear combination of GREEK_LETTERS with Fraction coefficients.

    Class Invariants: (valid before all methods except __init__ and after all methods)
    1. self.coefficients contains n Fractions, where 0 <= n <= len(GREEK_LETTERS)
    2. n = 0 denotes nothing is known about self
    3. For n > 0, self denotes the following angle:
    self.coefficients[0]α + self.coefficients[1]β + ... + self.coefficients[n-1]
    """

    def __init__(self, some_coefficients):
        """
        Preconditions:
        1. len(some_coefficients) <= len(GREEK_LETTERS)
        2. isinstance(c, (Fraction, int, float)) for every c in some_coefficients

        """

        # (Converted): self.coefficients[i] is the Fraction equivalent of
        # some_coefficients[i] for all i in [0, len(some_coefficients))

        self.coefficients = []
        for coefficient in some_coefficients:
            if isinstance(coefficient, (int, float)):
                self.coefficients.append(to_fraction(coefficient))
            elif isinstance(coefficient, Fraction):
                self.coefficients.append(coefficient)

    def __add__(self, an_angle):
        """
        Intent: Implementation of "+" arithmetic operation for addition to self.
        Usage: Angle + Angle, Angle + int, Angle + float

        Preconditions:
        1. self.is_known()
        2. (an_angle matches):
        EITHER is_instance(an_angle, (int, float))
        OR is_instance(an_angle, Angle) AND an_angle.is_known()
            AND an_angle.get_dimension() = self.get_dimension()

        Postconditions:
        1. (Coefficients obtained):
        EITHER is_instance(an_angle, Angle)
            AND given_coefficients = an_angle.get_coefficients()
        OR is_instance(an_angle, (int, float))
            AND given_coefficients = [0, 0, ..., an_angle]

        2. (Coefficients added):
        returned_coefficients is a list of length self.get_dimension()
        AND for all i, returned_coefficients[i] = self.coefficients[i] + given_coefficients[i]

        3. (Sum returned): Angle with coefficients returned_coefficients is returned
        """

        # --(Coefficients Obtained)
        given_coefficients = []
        if isinstance(an_angle, Angle):
            given_coefficients = an_angle.get_coefficients()
        elif isinstance(an_angle, (int, float)):
            given_coefficients = \
                [Fraction(0)] * (self.get_dimension() - 1) + [to_fraction(an_angle)]

        # --(Coefficients added)
        returned_coefficients = list(map(add, self.coefficients, given_coefficients))

        # --(Sum returned)
        return Angle(returned_coefficients)

    def __eq__(self, an_angle):
        """
        Intent: Implementation of "==" test for equality
        Usage: Angle == Angle, Angle == int, Angle == float, int == Angle, float == Angle

        Preconditions:
        1. self.is_known()
        2. is_instance(an_angle, (Angle, int, float))
        3. EITHER !is_instance(an_angle, Angle)
           OR an_angle.is_known() AND self.get_dimension() = an_angle.get_dimension()

        Returns: whether or not self has the same values as an_angle
        """
        # --(Converted): as_angle is an Angle with the same value as an_angle

        as_angle = copy.deepcopy(an_angle)  # to avoid changing the parameter
        if isinstance(as_angle, (int, float)):
            as_angle = Angle([to_fraction(0)] * (self.get_dimension() - 1)
                             + [to_fraction(as_angle)])

        # --(Compared):
        # EITHER self.coefficients same as as_angle.coefficients AND True returned
        # OR False returned

        an_angle_coefficients = as_angle.get_coefficients()
        for i in range(len(self.coefficients)):
            if self.coefficients[i] != an_angle_coefficients[i]:
                return False

        return True

    def __hash__(self):
        """
        Returns: hash of sum of self.coefficients
        """
        result = ''
        for c in self.coefficients:
            result += str(c)
        return hash(result)

    def __mul__(self, a_number):
        """
        Intent: Implementation of "/" arithmetic operation for division of self.
        Usage: Angle / Angle, Angle / int, Angle / float

        Preconditions:
        1. self.is_known()
        2. (an_angle matches):
        EITHER is_instance(an_angle, (int, float))
        OR is_instance(an_angle, Angle) AND an_angle.is_known()
            AND an_angle.get_dimension() = self.get_dimension()
        3. a_number != 0

        Postconditions:
        1. (Coefficients multiplied):
        returned_coefficients is a list of length self.get_dimension()
        AND for all i, returned_coefficients[i] = self.coefficients[i] * given_coefficients[i]

        2. (Product returned): Angle with coefficients returned_coefficients is returned
        """

        result_coefs = list(map(lambda x: x * to_fraction(a_number), self.coefficients))
        return Angle(result_coefs)

    def __ne__(self, other):
        """
        Intent: Binary comparison operation '!='.
        Usage: Angle != Angle; Angle != int; int != Angle; Angle != float; float != Angle
        Preconditions: as for self.__eq__()
        """
        return not self.__eq__(other)

    def __radd__(self, an_angle):
        """
        Specifications as for __add__ except self is second term as in
        int + Angle or float + Angle
        """
        return self + an_angle

    def __repr__(self):
        return self.__str__()

    def __rmul__(self, a_number):
        """
        Specifications as for __mul__ except self is second term as in
        int * Angle or float * Angle
        """
        return self * a_number

    def __rsub__(self, an_angle):
        """
        Specifications as for __sub__ except self is second term as in
        int - Angle or float - Angle
        """
        # an_angle - self = an_angle + negated_self
        negated_self = Angle(list(map(lambda x: -x, self.coefficients)))
        return negated_self + an_angle

    def __str__(self):
        """
        Returns: EITHER 'x' --if self is unknown OR string version of
        self.coefficients[0]α + ...coefficients[1]β + ... + ...coefficients[n-1]
        """

        # If unknown
        if not self.is_known():
            return 'x'

        # First n-1 coefficients
        result = ''
        for i in range(len(self.coefficients) - 1):
            a = self.coefficients[i]
            if a > 0:
                result += (' + ' + str(a) if a != 1 else ' + ') + GREEK_LETTERS[i]
            elif a < 0:
                result += (' - ' + str(abs(a)) if abs(a) != 1 else ' - ') + GREEK_LETTERS[i]

        # Last coefficient
        a = self.coefficients[-1]
        if a > 0:
            result += ' + ' + str(a)
        elif a < 0:
            result += ' - ' + str(abs(a))

        # Restore sign before the first coefficient
        if result[1] == '-':
            result = '-' + result[3:]
        elif result[1] == '+':
            result = result[3:]

        return result

    def __sub__(self, an_angle):
        """
        Intent: Implementation of "-" arithmetic operation for addition to self.
        Usage: Angle - Angle, Angle - int, Angle - float

        Preconditions:
        1. self.is_known()
        2. (an_angle matches):
        EITHER is_instance(an_angle, (int, float))
        OR is_instance(an_angle, Angle) AND an_angle.is_known()
            AND an_angle.get_dimension() = self.get_dimension()

        Postconditions:
        1. (Coefficients obtained):
        EITHER is_instance(an_angle, Angle)
            AND given_coefficients = an_angle.get_coefficients()
        OR is_instance(an_angle, (int, float))
            AND given_coefficients = [0, 0, ..., an_angle]

        2. (Coefficients subtracted):
        returned_coefficients is a list of length self.get_dimension()
        AND for all i, returned_coefficients[i] = self.coefficients[i] - given_coefficients[i]

        3. (Sum returned): Angle with coefficients returned_coefficients is returned
        """

        # --(Coefficients Obtained)
        given_coefficients = []
        if isinstance(an_angle, Angle):
            given_coefficients = an_angle.get_coefficients()
        elif isinstance(an_angle, (int, float)):
            given_coefficients = \
                [Fraction(0)] * (self.get_dimension() - 1) + [to_fraction(an_angle)]

        # --(Coefficients added)
        returned_coefficients = list(map(sub, self.coefficients, given_coefficients))

        # --(Sum returned)
        return Angle(returned_coefficients)

    def __truediv__(self, a_number):
        """
        Intent: Implementation of "/" arithmetic operation for division of self.
        Usage: Angle / Angle, Angle / int, Angle / float

        Preconditions:
        1. self.is_known()
        2. (an_angle matches):
        EITHER is_instance(an_angle, (int, float))
        OR is_instance(an_angle, Angle) AND an_angle.is_known()
            AND an_angle.get_dimension() = self.get_dimension()
        3. a_number != 0

        Postconditions:
        1. (Coefficients divided):
        returned_coefficients is a list of length self.get_dimension()
        AND for all i, returned_coefficients[i] = self.coefficients[i] / given_coefficients[i]

        2. (Quotient returned): Angle with coefficients returned_coefficients is returned
        """
        returned_coefficients = \
            list(map(lambda x: x / to_fraction(a_number), self.coefficients))
        return Angle(returned_coefficients)

    def get_coefficients(self):
        return self.coefficients

    def get_dimension(self):
        # Example if self is aα + aβ + c, 3 is returned
        return len(self.coefficients)

    def is_known(self):
        return bool(self.get_coefficients())

    @classmethod
    def from_str(cls, a_string):
        """
        Intent: To instantiate an Angle from a string

        Precondition: a_string is in one of the forms:
            - 'x' for unknown
            - 'a b ... z' for aα + bβ + ... + z
                where a, b, ..., z are either
                    - integers (e.g., 1, 2, -90, -9, etc)
                    - float numbers (e.g., 1.2, 2.3, -90.0, -9.0, etc)
                    - fractions (e.g., 1/2, 3/5, -6/19, -9/2, etc)

        Returns: the corresponding Angle
        """

        if a_string == 'x':
            return Angle([])

        coefficients = a_string.split()  # coefficients separated by spaces
        fraction_coefficients = []
        for coefficient in coefficients:
            if '/' in coefficient:
                fraction_coefficients.append(Fraction(coefficient))
            else:
                fraction_coefficients.append(Fraction(Decimal(coefficient)))

        return Angle(fraction_coefficients)
