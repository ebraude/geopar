from geopar.triangulated_figure_class import TriangulatedFigure
from geopar.triangle_class import Triangle
from geopar.tf_validator import TF_Validator
from geopar.tf_elaborations_class import TF_Elaborations
from geopar.angle_class import Angle
from fractions import Fraction
from itertools import islice
from geopar.utilities import find_str_occurrences

"""
note: check input for correctness
note: show where input is wrong
"""


__author__ = 'satbek'  # edited by Eric Braude

greek_names = ['alpha', 'beta', 'gamma', 'delta', 'epsilon']
greek_symbols = ['α', 'β', 'γ', 'δ', 'ε']
latin_symbols = ['a', 'b', 'c', 'd', 'e']


class Parser(object):
    """
    """

    def __init__(self, path_to_file):
        self.__path_to_file = path_to_file
        self.__num_lines = -1
        self.__num_vars = -1
        self.__configuration = ''

    def read_first_configuration(self):
        """
        reads first __configuration from input __path_to_file
        with a bunch of configurations
        """

        file = open('../inputs/' + self.__path_to_file, encoding='utf-8')
        settings = file.readline()
        self.__num_lines, self.__num_vars = map(int, settings.split())
        self.__configuration = list(islice(file, self.__num_lines))

        return self.__process_configuration()

    def __process_configuration(self):
        """
        processes all lines in a __configuration
        and returns a triangulated figure
        """

        figure = TriangulatedFigure()
        for line in self.__configuration:
            figure.add(self.__process_triangle(line))

        return figure

    def __process_triangle(self, a_triangle):
        """
        processes a_triangle in a __configuration
        and returns a triangle

        1, 2, 3; \alpha + \beta - 90, \alpha + \beta - 90, \alpha + \beta - 90
        """

        # splitting points and angles
        points, angles = a_triangle.split(';')

        # processing angles
        angles = angles.split(',')

        for i in range(len(angles)):
            angles[i] = angles[i].strip()

            if angles[i] == 'x':
                pass  # do nothing
            elif angles[i][0] != '-':
                angles[i] = '+' + angles[i]

        processed_angles = list()
        for i in range(len(angles)):
            processed_angles.append(self.__process_angle(angles[i]))

        # processing points
        points = list(map(int, points.split(',')))

        return Triangle(points, processed_angles)

    def __process_angle(self, an_angle):
        """
        processes an_angle

        +\alpha + \beta - 90
        """

        # processing unknown angle
        if an_angle == 'x':
            return Angle([])

        # signs_at contains indices of + and -
        signs_at = find_str_occurrences(an_angle, '+')
        signs_at.extend(find_str_occurrences(an_angle, '-'))
        signs_at = sorted(signs_at)

        # stops_at
        stops_at = signs_at.copy()
        stops_at.append(len(an_angle))

        # contains signs in order
        # ['-', '+', '+', '-', '-', '+'] for -a+b+c-d-e+1
        signs = list()

        # contains terms in order
        # ['a', 'b', 'c', 'd', 'e', '1'] for -a+b+c-d-e+1
        terms = list()

        for i in range(len(stops_at) - 1):
            signs.append(an_angle[signs_at[i]])
            terms.append(an_angle[ (stops_at[i] + 1) : stops_at[i + 1 ]].strip())

        # print('an angle is {}'.format(an_angle))

        coefs = list()
        term_inds = list()

        for i in range(len(terms)):
            c, t = self.__process_term(terms[i])
            coefs.append(c)
            term_inds.append(t)
            # print('\t sign = {}, term = {} ==> coef: {}, term: {}'.format(signs[i], terms[i], c, t))

        angle_coefs = [Fraction(0)] * self.__num_vars
        for i in range(len(term_inds)):
            angle_coefs[term_inds[i]] += Fraction(signs[i] + coefs[i])

        return Angle(angle_coefs)

    def __process_term(self, a_term):
        """process

        ['\alpha', '\beta', '\gamma', '\delta', '\epsilon']
        ['α', 'β', 'γ', 'δ', 'ε']
        ['a', 'b', 'g', 'd', 'e']

        together with a_term's coefficient

        POST: (coef, term) pair returned
        where coef is str and term is int
        """
        if '\\' in a_term:
            # \alpha style

            # forcing 1 as a coefficient
            if a_term.startswith('\\'):
                a_term = '1' + a_term

            coef, term = a_term.split('\\')

            # making sure that a_term is legal
            if term not in greek_names:
                raise Exception('wrong input: ' + term)

            # converting a_term to its integer alternative
            # 0 for alpha, 1 for beta, etc
            term = greek_names.index(term)

            # confirming that user does not provide too many variables
            if term >= self.__num_vars:
                raise Exception('Too many variables provided!')

            # print('\t\t', a_term, coef, term)

            return coef, term
        else:
            # α and a style
            # a, α, 2a, 10a, 2, 10, 100/3, 10.5, 100/3a, 10.5a

            # forcing 1 as a coefficient
            if len(a_term) == 1 and a_term.isalpha():
                a_term = '1' + a_term

            if a_term[-1].isalpha():
                coef, term = a_term[:-1], a_term[-1]

                # making sure that a_term is legal
                if term not in greek_symbols + latin_symbols:
                    raise Exception('wrong input:', term)

                # converting a_term to its integer alternative
                # 0 for alpha, 1 for beta, etc
                if term in greek_symbols:
                    term = greek_symbols.index(term)
                elif term in latin_symbols:
                    term = latin_symbols.index(term)

                # confirming that user does not provide too many variables
                if term >= self.__num_vars:
                    raise Exception('Too many variables provided!')
            else:
                coef, term = a_term, self.__num_vars - 1

            # print('\t\t a_term = {}, coef = {}, term = {}'.format(a_term, coef, term))

            return coef, term


def run(a_tf):
    '''
    Postconditions:
    1. (Completed before pairing): 180 and 360 rules produce no further angles on given a_tf
    2. (All known?): EITHER NOT a_tf.all_angles_are_known() AND this did not return
    OR AND UNIQUE ALL-ANGLE CONSEQUENCE OF THE PREMISES or INCONCLUSIVE  reported to user on console
    3. (Queried): State of a_tf on console AND user was queried to attempt pairing
    4. (No pairing): EITHER user replied "yes" AND user_input == 'y'
        OR user replied "no" AND "1A. INCONCLUSIVE" and a_tf are on the console AND this returned
    5. (Pairing): Pairing, 180 and 360 rules were performed until no new results AND result reported
    6. Validity of a_tf is on the console
    '''

    # --1. (Completed before pairing)

    old_a_tf_state, new_a_tf_state = 0, a_tf.get_id()  # before/after computing present state
    preprocessor = TF_Elaborations()
    while old_a_tf_state != new_a_tf_state:
        old_a_tf_state = a_tf.get_id()
        preprocessor.apply_180_rule_to(a_tf)
        preprocessor.apply_360_rule_to(a_tf)
        new_a_tf_state = a_tf.get_id()

    # --2. (All angles?)

    validator = TF_Validator()
    if a_tf.all_angles_are_known():
        # 180, 360, and pairing valid?
        if validator.run_all_rules(a_tf):
            print('-------------------------')
            print("Pre-process complete.")
            print('-------------------------')
            print("Here is your triangulated figure:")
            print(a_tf)
            print("1B. UNIQUE ALL-ANGLE CONSEQUENCE OF THE PREMISES.")
        else:
            print('-------------------------')
            print("Pre-process complete.")
            print('-------------------------')
            print('INCONCLUSIVE (1)')
        return

    # --3. (Queried)

    print('-------------------------')
    print('Before pairing:')
    print('-------------------------')
    print(a_tf)
    user_input = input('Do you want angle pairing to be applied? (y/n): ')
    print()

    # --4. (No)

    if user_input == 'n':
        print('-------------------------')
        print("Pre-process complete.")
        print('-------------------------')
        print('1A. INCONCLUSIVE')
        print("Here is your triangulated figure:")
        print(a_tf)
        return

    # --5. (Yes)

    # Apply pairing, 180, and 360 rules until no new angles deduced
    old_a_tf_state, new_a_tf_state = 0, a_tf.get_id()  # before/after computing present state
    preprocessor = TF_Elaborations()
    while old_a_tf_state != new_a_tf_state:
        old_a_tf_state = a_tf.get_id()
        preprocessor.apply_pairing_to(a_tf)
        preprocessor.apply_180_rule_to(a_tf)
        preprocessor.apply_360_rule_to(a_tf)
        new_a_tf_state = a_tf.get_id()

    # All angles known; 180, 360, and pairing valid?
    if a_tf.all_angles_are_known() and validator.run_all_rules(a_tf):
        print('-------------------------')
        print("Pre-process complete.")
        print('-------------------------')
        print("2. A CONSEQUENCE OF THE PREMISES.")
        print("Here is your triangulated figure:")
        print(a_tf)
    else:
        print('-------------------------')
        print("Pre-process complete.")
        print('-------------------------')
        print("INCONCLUSIVE (2)")
        print("Here is your triangulated figure:")
        print(a_tf)


# "Pre-processing" stage
p = Parser('input.txt')
triangulated_figure = p.read_first_configuration()

print('-------------------------')
print('Before pre-processing:')
print('-------------------------')
print("Here is your triangulated figure:")
print(triangulated_figure)

print('-------------------------')
print('Pre-process is running...')
print('-------------------------')

run(triangulated_figure)
