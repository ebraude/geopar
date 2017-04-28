from geopar.angle_class import Angle

__author__ = 'satbek'  # modified by Eric Braude


class Triangle:
    """
    Intent: Triangle with 3 angles and 3 vertices (also called 'points')
              points[0] *-----* points[1] angles[1]
                         \  /
                angles[2] * points[2]

    Class invariants:
    1. self.points consists of 3 distinct non-negative int instances
    2. self.points is in clockwise order geometrically
    3. self.angles[i] corresponds to self.points[i]  for i in [0, 2]
    """

    def __init__(self, three_points, three_angles):
        """
        PRE1: three_points consists of three distinct non-negative integers
        PRE2: three_angles consists of three Angle|int|float instances

        Postconditions:
        1. self.points|self.angles correspond to three_points|three_angles
        2. self.angles consists of Angle objects
        """

        # Convert int|float angles to Angle
        temp_3_angles = []
        for angle in three_angles:
            if isinstance(angle, (int, float)):
                temp_3_angles.append(Angle([angle]))
            if isinstance(angle, Angle):
                temp_3_angles.append(angle)

        self.points, self.angles = three_points, temp_3_angles

    def __hash__(self):
        # Returns hash of self based on contents of self.angles

        sorted_points = sorted(self.points)
        for_hash = str(sorted_points[0]) + str(hash(self.angle_of_point(sorted_points[0])))
        for_hash += str(sorted_points[1]) + str(hash(self.angle_of_point(sorted_points[1])))
        for_hash += str(sorted_points[2]) + str(hash(self.angle_of_point(sorted_points[2])))
        return hash(for_hash)

    def __str__(self):
        # Returns: string representation of self.

        return_string = 'TRIANGLE -> Vertices: {}, {}, {}; Angles: {}, {}, {}'.format(
            self.get_points()[0], self.get_points()[1], self.get_points()[2],
            self.get_angles()[0], self.get_angles()[1], self.get_angles()[2])
        return return_string

    def angle_of_point(self, a_point):
        # Precondition: a_point is in self.points
        # Returns: the element of self.angles corresponding to a_point

        if a_point not in self.points:
            raise Exception('There is no such point for this Triangle.')
        return self.angles[self.points.index(a_point)]

    def complete_unknown_angle(self):
        """
        Intent:Completes a triangle with one unknown angle.
        Precondition: self.number_of_known() = 2
        Postconditions:
        1. self.number_of_known() = 3
        2. The sum of self.angles = 180
        """

        # Ensuring precondition
        if self.number_of_known() != 2:
            raise Exception('Something went wrong.')

        sum_ = self.sum_of_known_angles()
        third = 180 - sum_

        for i in range(3):
            if not self.angles[i].is_known():
                self.angles[i] = third

    def get_angle_points_by_point(self, a_point):
        # Returns: the clockwise elts. of self.points for the angle at a_point

        index_of_a_point = self.index_of_point(a_point)
        shift = (index_of_a_point + 2) % 3
        points = self.points[shift:] + self.points[:shift]
        return points

    def get_angles(self):

        return self.angles

    def get_points(self):

        return self.points

    def has_all_points(self, three_points):
        # Returns: whether or not self.points is the same set as three_points

        return set(self.points) == set(three_points)

    def has_point(self, a_point):
        # Returns: whether or not a_point is in self.points

        return a_point in self.points

    def has_unknown_angle(self):
        # Returns: whether or not is_known() is True for any element of self.angles

        return self.number_of_known() != 3

    def index_of_point(self, a_point):
        """
        Precondition: a_point is in self.points
        Returns index of a_point in self.points
        """
        if a_point not in self.points:
            raise Exception('There is no such point for this Triangle.')
        return self.get_points().index(a_point)

    def number_of_known(self):
        # Returns: the number of angles in self satisfying is_known()

        count = 0
        for angle in self.angles:
            if angle.is_known():
                count += 1
        return count

    def point_following(self, a_point):
        # Precondition: a_point is in self.points
        # Returns: the element of self.points that follows a_point clockwise

        if a_point not in self.points:
            raise Exception('There is no such point for this Triangle.')
        index_of_a_point = self.points.index(a_point)
        return self.points[(index_of_a_point + 1) % 3]

    def point_preceding(self, a_point):
        # Precondition: a_point is in self.points
        # Returns: the element of self.points that precedes a_point clockwise

        if a_point not in self.points:
            raise Exception('There is no such point for this Triangle.')
        index_of_a_point = self.points.index(a_point)
        return self.points[(index_of_a_point - 1) % 3]

    def set_angle_by_index(self, an_index, an_angle):
        # Precondition: an_index is either 0, 1, or 2
        # Postcondition: self.angles[an_index] = an_angle

        if an_index not in [0, 1, 2]:
            raise Exception('Bad index.')
        self.angles[an_index] = an_angle

    def set_angle_by_point(self, a_point, an_angle):
        # Precondition: a_point is in self.points
        # Postcondition: an_angle is the element of self.angles corresponding to a_point
        # Example: set_angle_by_point(self, 44, 70) with self.points = [.., 44, ..]
        # results in self.angles = [.., 70, ..]

        if a_point not in self.points:
            raise Exception('There is no such point for this Triangle.')
        self.angles[self.index_of_point(a_point)] = an_angle

    def sum_of_known_angles(self):
        # Returns: sum of self.angles elements satisfying is_known()

        sum_ = 0
        for angle in self.angles:
            if angle.is_known():
                sum_ += angle
        return sum_
