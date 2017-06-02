from collections import Counter

__author__ = 'satbek'  # Edited by Eric Braude


class TF_Validator(object):
    #  Validation rules on Triangulated Figures

    @staticmethod
    def run_all_rules(a_tf):
        return TF_Validator.check_180_rule(a_tf) and TF_Validator.check_360_rule(a_tf) \
               and TF_Validator.check_pairing(a_tf)

    @staticmethod
    def check_180_rule(a_tf):
        """
        Precondition: a_tf is an instance of TriangulatedFigure containing at least one triangle
        Postcondition: Whether the angles of every triangle in a_tf sum to 180
        """
        if a_tf.is_empty():
            raise Exception('A triangulated figure is empty! See precondition in TFValidator.rule_180().')
        for triangle_ in a_tf.get_triangles():
            if sum(triangle_.get_angles()) != 180:
                return False
        return True

    @staticmethod
    def check_360_rule(a_tf):
        """
        Precondition: a_tf is an instance of TriangulatedFigure containing at least one triangle
        Postcondition: Whether the angles at every interior point of a_tf sum to 360
        """
        # Check precondition
        if a_tf.is_empty():
            raise Exception\
                ('A triangulated figure is empty! See precondition in TFValidator.run_360_rule.')

        # --interior_points pertains to a_tf
        interior_points = a_tf.get_interior_points()

        # --Postcondition
        for point in interior_points:
            triangles = a_tf.triangles_at(point)
            sum_angles = 0
            for triangle in triangles:
                sum_angles += triangle.angle_of_point(point)
            if sum_angles != 360:
                return False
        return True

    @staticmethod
    def check_pairing(a_tf):
        """
        Precondition: a_tf is an instance of TriangulatedFigure containing at least one triangle

        Postcondition: Whether the "before" angles = the "after" angles for every interior point
        """
        # Check precondition
        if a_tf.is_empty():
            raise Exception('a_tf is empty! See precondition PRE')

        following, preceding = [], []
        for point in a_tf.get_interior_points():
            for triangle in a_tf.triangles_at(point):
                following.append(triangle.angle_of_point(triangle.point_following(point)))
                preceding.append(triangle.angle_of_point(triangle.point_preceding(point)))

            if set(following) != set(preceding):
                return False

        return True
