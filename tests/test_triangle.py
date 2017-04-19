import unittest
from geopar.triangle_class import Triangle
from geopar.angle_class import Angle

__author__ = 'satbek'


class TestTriangle(unittest.TestCase):
    def setUp(self):
        self.triangle0 = Triangle([1, 2, 3], [20, 30, 130])
        self.triangle1 = Triangle([2, 1, 77], [130, 20, 30])
        self.triangle2 = Triangle([1, 77, 88], [Angle([30, 40, 110]), Angle.from_str('x'), Angle([60, 60, 60])])

        self.aa = Angle.from_str('1/3 1/3 1/3 60')
        self.ab = Angle.from_str('-1/3 1/3 -1/3 45')
        self.ac = Angle.from_str('x')
        self.triangle3 = Triangle([1, 2, 3], [self.aa, self.ab, self.ac])

        self.aaa = Angle.from_str('1/3 1/3 1/3 60')
        self.aba = Angle.from_str('-1/3 1/3 -1/3 45')
        self.aca = Angle.from_str('x')
        self.triangle3a = Triangle([1, 2, 3], [self.aaa, self.aba, self.aca])

    def test_init(self):
        # force conversion of int, float angles to Angle
        triangle = Triangle([1, 2, 3], [10, 20.0, Angle([30])])
        for angle in triangle.angles:
            self.assertTrue(isinstance(angle, Angle))

    def test_str(self):
        print(self.triangle0)
        print(self.triangle1)
        print(self.triangle2)
        print(self.triangle3)

    def test_hash(self):
        self.assertEqual(hash(self.triangle0), hash(self.triangle0))  # a == a
        self.assertEqual(hash(self.triangle1), hash(self.triangle1))  # b == b
        self.assertNotEqual(hash(self.triangle0), hash(self.triangle1))  # a != b

        self.assertEqual(hash(self.triangle3), hash(self.triangle3))  # c == c
        self.assertEqual(hash(self.triangle3), hash(self.triangle3a))  # c == d

    def test_get_angles(self):
        self.assertTrue(20 in self.triangle0.get_angles())
        self.assertTrue(30 in self.triangle1.get_angles())
        self.assertTrue(Angle.from_str('30 40 110') in self.triangle2.get_angles())

    def test_get_points(self):
        self.assertEqual(self.triangle0.get_points(), [1, 2, 3])
        self.assertTrue(77 in self.triangle1.get_points())
        self.assertFalse(78 in self.triangle1.get_points())

    def test_angle_of_point(self):
        self.assertTrue(20 == self.triangle0.angle_of_point(1))
        self.assertTrue(30 == self.triangle1.angle_of_point(77))
        self.assertTrue(Angle([60,60,60]) == self.triangle2.angle_of_point(88))

        with self.assertRaises(Exception):
            self.triangle1.angle_of_point(4)

    def test_index_of_point(self):
        self.assertTrue(0 == self.triangle0.index_of_point(1))
        self.assertTrue(1 == self.triangle0.index_of_point(2))
        self.assertTrue(2 == self.triangle0.index_of_point(3))

        with self.assertRaises(Exception):
            self.triangle1.angle_of_point(4)

    def test_point_following(self):
        self.assertEqual(3, self.triangle0.point_following(2))
        self.assertEqual(1, self.triangle0.point_following(3))

        with self.assertRaises(Exception):
            self.triangle1.angle_of_point(4)

    def test_point_preceding(self):
        self.assertEqual(1, self.triangle1.point_preceding(77))

        with self.assertRaises(Exception):
            self.triangle1.angle_of_point(4)

    def test_count_known(self):
        self.assertEqual(3, self.triangle0.number_of_known())
        self.assertEqual(3, self.triangle1.number_of_known())
        self.assertEqual(2, self.triangle2.number_of_known())

    def test_has_point(self):
        self.assertTrue(self.triangle0.has_point(1))
        self.assertTrue(self.triangle0.has_point(3))
        self.assertFalse(self.triangle0.has_point(4))
        self.assertTrue(self.triangle1.has_point(77))

    def test_has_all_points(self):
        self.assertTrue(self.triangle0.has_all_points([1, 2, 3]))
        self.assertTrue(self.triangle1.has_all_points([1, 2, 77]))

    def test_has_unknown(self):
        self.assertFalse(self.triangle0.has_unknown_angle())
        self.assertTrue(self.triangle2.has_unknown_angle())

    def test_get_angle_points_by_point(self):
        self.assertEqual(self.triangle0.get_angle_points_by_point(1), [3, 1, 2])
        self.assertEqual(self.triangle0.get_angle_points_by_point(2), [1, 2, 3])
        self.assertEqual(self.triangle0.get_angle_points_by_point(3), [2, 3, 1])

    def test_set_angle_by_point(self):
        triangle = Triangle([1, 2, 3], [20, 30, 130])
        triangle.set_angle_by_point(1, 30)
        triangle.set_angle_by_point(2, 20)
        self.assertEqual(30, triangle.angle_of_point(1))
        self.assertEqual(20, triangle.angle_of_point(2))
        self.assertEqual(130, triangle.angle_of_point(3))

        with self.assertRaises(Exception):
            self.triangle1.angle_of_point(4)

    def test_set_angle_by_index(self):
        triangle = Triangle([1, 2, 3], [20, 30, 130])
        triangle.set_angle_by_index(0, 30)
        triangle.set_angle_by_index(1, 20)
        self.assertEqual(30, triangle.angle_of_point(1))
        self.assertEqual(20, triangle.angle_of_point(2))
        self.assertEqual(130, triangle.angle_of_point(3))

        with self.assertRaises(Exception):
            self.triangle1.set_angle_by_index(3)

    def test_sum_of_known_angles(self):
        self.assertEqual(self.triangle0.sum_of_known_angles(), Angle([180]))
        self.assertEqual(self.triangle2.sum_of_known_angles(), Angle([90, 100, 170]))

    def test_complete_unknown_angle(self):
        triangle = Triangle([1, 77, 88], [Angle([30, 40, 110]), Angle.from_str('x'), Angle([60, 60, 60])])
        triangle.complete_unknown_angle()
        self.assertEqual(Angle([-90, -100, 10]), triangle.angle_of_point(77))

        triangle = Triangle([1, 2, 3], [Angle.from_str('x'), 100, 10])
        triangle.complete_unknown_angle()
        self.assertEqual(70, triangle.angle_of_point(1))
