from geopar.triangulated_figure_class import TriangulatedFigure
from geopar.triangle_class import Triangle
from geopar.angle_class import Angle
from geopar.tf_validator import TF_Validator
from geopar.tf_elaborations_class import TF_Elaborations

"""
Known Issue: Does not check the input for correctness
"""

__author__ = 'satbek'  # edited by Eric Braude


def parse_file(a_file):
    '''
    Returns return_figure = TriangulatedFigure with the specifications in a_file
    '''
    # --the_file represents a_file, opened for input
    the_file = open('../inputs/' + a_file)

    # --number_of_triangles assigned
    line = the_file.readline()
    line = line.split()
    number_of_triangles = int(line[0])

    # --return_figure = TriangulatedFigure with the specifications in a_file

    return_figure = TriangulatedFigure()
    for i in range(number_of_triangles):
        # line = ['point1, point2, point3', 'angle1, angle2, angle3']
        line = the_file.readline().split(';')

        # _points = [point1, point2, point3]
        _points = list(map(int, line[0].split(',')))

        # angles_str = ['angle1', 'angle2', 'angle3']
        angles_str = list(map(str.strip, line[1].split(',')))

        a1 = Angle.from_str(angles_str[0])
        a2 = Angle.from_str(angles_str[1])
        a3 = Angle.from_str(angles_str[2])

        _angles = [a1, a2, a3]
        return_figure.add(Triangle(_points, _angles))

    return return_figure


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
            print("Pre-process complete.")
            print("Here is your triangulated figure:")
            print(a_tf)
            print("1B. UNIQUE ALL-ANGLE CONSEQUENCE OF THE PREMISES.")
        else:
            print("Pre-process complete.")
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
triangulated_figure = parse_file('input.txt')

print('-------------------------')
print('Before pre-processing:')
print('-------------------------')
print("Here is your triangulated figure:")
print(triangulated_figure)

print('-------------------------')
print('Pre-process is running...')
print('-------------------------')

run(triangulated_figure)
