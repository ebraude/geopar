from collections import Counter

__author__ = 'satbek'


class TFValidator(object):
    """
    Triangulated Figure Validator: a triangulated figure is valid when it passes
    all of the following three rules (see the paper):
    1 - Rule of 180 degrees
    2 - Rule of 360 degrees
    3 - Rule of pairing
    """

    @staticmethod
    def all_rules(a_tf):
        return TFValidator.rule_180(a_tf) and TFValidator.rule_360(a_tf) and TFValidator.rule_pairing(a_tf)

    @staticmethod
    def rule_180(a_tf):
        """
        INTENT
        Checks whether a rule of 180 degrees is valid in a triangulated figure.

        PRE
        a_tf is an instance of TriangulatedFigure class containing at least one triangle.

        POST
        True is returned if the angles of every triangle in a_tf sum up to 180, False otherwise.
        """

        if a_tf.is_empty():
            raise EmptyException('A triangulated figure is empty! See precondition in TFValidator.rule_180().')

        for triangle_ in a_tf.get_triangles():
            if sum(triangle_.get_angles()) != 180:
                return False
        return True

    @staticmethod
    def rule_360(a_tf):
        """
        Checks whether a rule of 360 degrees is valid in a triangulated figure.

        PRE
        a_tf is an instance of TriangulatedFigure class containing at least one triangle.

        POST
        True is returned if the angles around every interior point sum up to 360, False otherwise.
        """

        if a_tf.is_empty():
            raise EmptyException('A triangulated figure is empty! See precondition in TFValidator.rule_360().')

        '''
        # version 1
        def sum_of_angles_around_a_point_is_360(a_point):
            # Intent: returns True if the sum of angles around a_point equals 360, False otherwise
            triangles_ = a_tf.triangles_with_point(a_point)
            sum_angles_ = 0
            for triangle_ in triangles_:
                sum_angles_ += triangle_.angle_of_point(interior_point)
            return sum_angles_ == 360

        for interior_point in a_tf.get_interior_points():
            if not sum_of_angles_around_a_point_is_360(interior_point):
                return False

        return True
        '''

        '''
        # version 2
        # === 1 (Interior point): 'interior_point' is a point
        for interior_point in a_tf.get_interior_points():

            # === 2 (Summed up): 'sum_angle' contains the sum of angles around 'interior_point'
            triangles = a_tf.triangles_with_point(interior_point)
            sum_angles = 0
            for triangle in triangles:
                sum_angles += triangle.angle_of_point(interior_point)

            # === 3 (Sum checked): 'sum_angles' is not equal to 360
            if sum_angles != 360:
                return False

        # === 4 (Complement): 'sum_angles' is equal to 360
        return True
        '''

        # === 1 (Interior point): interior_point = points[i] for 0 <= i < len(points)
        # === 2 (Summed up): sum_angles = sum of angles around interior_point
        # === 3 (Sum checked): sum_angles != 360
        # === 4 (Complement): i == len(points)

        points = a_tf.get_interior_points()

        # a_tf has no interior points
        if not points:
            return True

        i = 0

        while i != len(points):

            # === 1 (Interior point)
            interior_point = points[i]
            i += 1

            # === 2 (Summed up)
            triangles = a_tf.triangles_with_point(interior_point)
            sum_angles = 0
            for triangle in triangles:
                sum_angles += triangle.angle_of_point(interior_point)

            # === 3 (Sum checked)
            if sum_angles != 360:
                return False

        # === 4 (Complement)
        return True

    @staticmethod
    def rule_pairing(a_tf):
        """
        Checks whether a rule of pairing is valid in a triangulated figure a_tf.

        PRE
        a_tf is an instance of TriangulatedFigure class containing at least one triangle.

        POST
        True is returned if the rule is valid, False otherwise.
        """

        ########################################################################
        if a_tf.is_empty():
            raise Exception('a_tf is empty! See precondition PRE')
            ########################################################################

        following, preceding = [], []
        for point in a_tf.get_interior_points():
            for tri in a_tf.triangles_with_point(point):
                following.append(tri.angle_of_point(tri.point_following(point)))
                preceding.append(tri.angle_of_point(tri.point_preceding(point)))

            if Counter(following) != Counter(preceding):
                return False

        return True

