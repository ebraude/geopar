from collections import Counter

__author__ = 'satbek'  # edited by Eric Braude


class TF_Elaborations(object):
    """
    Functions that deduce or infer new facts from a given TriangulatedFigure

    The deductions are the 180-degree rule and the 360-degree rule;
    The inferral is the Pairing rule. For more on these refer to the paper by Braude and Abdyldayev
    """

    @staticmethod
    def apply_180_rule_to(a_tf):
        """
        Intent: Include unknown angles trianle-by-triangle in a_tf where possible
        Precondition: isinstance(a_tf, TriangulatedFigure)
        Postcondition: For every triangle t in a_tf.get_triangles(), at most one angle in t is known
        """
        for triangle in a_tf.get_triangles():
            if triangle.number_of_known() == 2:
                triangle.complete_unknown_angle()

    @staticmethod
    def apply_360_rule_to(a_tf):
        """
        Intent: Add unknown angles interior-point-by-point in a_tf where possible
        Precondition: isinstance(a_tf, TriangulatedFigure)
        Postcondition: At every interior point in a_tf, either all angles are known
        or at least two are not known
        """
        for point in a_tf.get_interior_points():
            a_tf.make_angles_known_at(point)

    @staticmethod
    def apply_pairing_at(a_tf, a_point):
        """
        Intent: Add unknown angles at a_point where possible

        Preconditions:
        1. isinstance(a_tf, TriangulatedFigure)
        2. a_point is an interior vertex of a_tf

        Postcondition: Either (1) all angles that a_point subtends in a_tf are known and they pair
        or (2) more than two are unknown or (3) exactly two are unknown but the rest do not pair
        """

        # --triangles_at_point defined

        triangles_at_point = a_tf.triangles_at(a_point)

        # --known_angles_following / ..._preceding = the known alternating angles subtended by a_point
        #   AND unknown_following_count / ..._preceding_... = the sum of above that are unknown
        #   AND known_angle_count is the count of the known angles subtended by a_point
        #   AND points_of_unknown_angles is the list of unknown angles as point triplets

        known_angles_following, known_angles_preceding = [], []
        unknown_following_count, unknown_preceding_count, known_angle_count = 0, 0, 0
        points_of_unknown_angles = []

        for t in triangles_at_point:

            point_following = t.point_following(a_point)
            point_preceding = t.point_preceding(a_point)
            angle_following = t.angle_of_point(point_following)
            angle_preceding = t.angle_of_point(point_preceding)

            if angle_following.is_known():
                known_angles_following.append(angle_following)
                known_angle_count += angle_following
            else:
                unknown_following_count += 1
                points_of_unknown_angles.append(t.get_angle_points_by_point(point_following))
            if angle_preceding.is_known():
                known_angles_preceding.append(angle_preceding)
                known_angle_count += angle_preceding
            else:
                unknown_preceding_count += 1
                points_of_unknown_angles.append(t.get_angle_points_by_point(point_preceding))

        # --Postcondition

        # Set the 2 unknown angles when case (2) applies only
        if unknown_following_count == 1 and unknown_following_count == 1 and \
                set(known_angles_following) == set(known_angles_preceding):
            angle_to_set = ((len(triangles_at_point) - 2) * 180 - known_angle_count) / 2
            a_tf.set_angle_by_angle_points(*points_of_unknown_angles[0], angle_to_set)
            a_tf.set_angle_by_angle_points(*points_of_unknown_angles[1], angle_to_set)

    @staticmethod
    def apply_pairing_to(a_tf):
        """
        Intent: Add unknown angles at every interior point of a_tf where possible
        Precondition: isinstance(a_tf, TriangulatedFigure)
        Postcondition:
        For every interior point in a_tf, the postconditions of apply_pairing_at() are true
        """
        for interior_point in a_tf.get_interior_points():
            TF_Elaborations.apply_pairing_at(a_tf, interior_point)
