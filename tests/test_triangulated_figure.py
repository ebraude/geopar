import unittest
from geopar.triangle_class import Triangle
from geopar.triangulated_figure_class import TriangulatedFigure
from geopar.angle_class import Angle

__author__ = 'ebraude'

# URL1: https://docs.google.com/presentation/d/1nddxo9JPaoxz-Colod8qd6Yuj_k7LXhBfO3JlVSYXrE/edit?usp=sharing


class TestTriangulatedFigure(unittest.TestCase):

    def setUp(self):
        self.tf_empty = TriangulatedFigure()

        # TriangulatedFigure tf1 consists of seven Triangles t1-t7
        # Appearance: URL1 at the top
        self.t1 = Triangle([1, 2, 5], [20, 10, 150])
        self.t2 = Triangle([5, 2, 6], [80, 10, 90])
        self.t3 = Triangle([6, 2, 3], [140, 10, 30])
        self.t4 = Triangle([4, 6, 3], [80, 70, 30])
        self.t5 = Triangle([1, 4, 3], [20, 130, 30])
        self.t6 = Triangle([1, 5, 4], [20, 70, 90])
        self.t7 = Triangle([4, 5, 6], [60, 60, 60])
        self.tf1 = TriangulatedFigure()
        self.tf1.add(self.t1)
        self.tf1.add(self.t2)
        self.tf1.add(self.t3)
        self.tf1.add(self.t4)
        self.tf1.add(self.t5)
        self.tf1.add(self.t6)
        self.tf1.add(self.t7)

        # TriangulatedFigure tf2 consists of seven Triangles t1-t7
        # Appearance: URL1 at the top
        # tf2 is different from tf1 only in a way it is described
        self.t11 = Triangle([2, 5, 1], [10, 150, 20])
        self.t22 = Triangle([6, 5, 2], [90, 80, 10])
        self.t33 = Triangle([6, 2, 3], [140, 10, 30])
        self.t44 = Triangle([6, 3, 4], [70, 30, 80])
        self.t55 = Triangle([3, 1, 4], [30, 20, 130])
        self.t66 = Triangle([5, 4, 1], [70, 90, 20])
        self.t77 = Triangle([6, 4, 5], [60, 60, 60])
        self.tf11 = TriangulatedFigure()
        self.tf11.add(self.t22)
        self.tf11.add(self.t55)
        self.tf11.add(self.t77)
        self.tf11.add(self.t11)
        self.tf11.add(self.t66)
        self.tf11.add(self.t33)
        self.tf11.add(self.t44)

    def test_constructor(self):

        t1 = Triangle([1, 2, 5], [20, 10, 150])
        t2 = Triangle([5, 2, 6], [80, 10, 90])
        t3 = Triangle([6, 2, 3], [140, 10, 30])
        t4 = Triangle([4, 6, 3], [80, 70, 30])
        t5 = Triangle([1, 4, 3], [20, 130, 30])
        t6 = Triangle([1, 5, 4], [20, 70, 90])
        t7 = Triangle([4, 5, 6], [60, 60, 60])
        tf1 = TriangulatedFigure([t1, t2, t3, t4, t5, t6, t7])
        print(tf1)

    def test_set_angle(self):
        a = Angle([100])
        self.tf1.set_angle_by_angle_points(3, 6, 2, 100)
        check = False
        for t in self.tf1.get_triangles():
            if t.has_all_points([3, 2, 6]):
                if t.angle_of_point(6) == 100:
                    check = True
        self.assertTrue(check)

    def test_get_angle_by_points(self):
        self.assertEqual(self.tf1.get_angle_by_angle_points(2, 5, 1), 150)
        self.assertEqual(self.tf1.get_angle_by_angle_points(5, 1, 2), 20)
        self.assertEqual(self.tf1.get_angle_by_angle_points(1, 2, 5), 10)

    def test_get_state(self):
        print(self.tf1.get_id())
        print(self.tf11.get_id())
        self.assertTrue(True)

    def test_get_points(self):

        print('test_get_points()')
        self.assertEqual(7, len(self.tf1.get_triangles()))  # 7 triangles
        self.assertEqual(6, len(self.tf1.get_points()))  # 6 points

    def test_triangles_with_vertex(self):

        print('test_triangles_with_point()')
        self.assertEqual(7, len(self.tf1.get_triangles()))  # 7 triangles

        # how can we check the order of triangles?

        triangles_ = self.tf1.triangles_with_point(4)
        self.assertEqual(4, len(triangles_))  # 4 triangles around point 4

    def test_is_empty(self):
        self.assertTrue(self.tf_empty.is_empty())
        self.assertFalse(self.tf1.is_empty())

    def test_number_of_unknown_angles_at(self):
        self.assertEqual(self.tf1.number_of_unknown_angles_at(4), 0)
        self.assertEqual(self.tf1.number_of_unknown_angles_at(5), 0)
        self.assertEqual(self.tf1.number_of_unknown_angles_at(6), 0)
        self.tf1.set_angle_by_angle_points(6, 4, 5, Angle.from_str('x'))
        self.assertEqual(self.tf1.number_of_unknown_angles_at(4), 1)
        self.tf1.set_angle_by_angle_points(3, 4, 6, Angle.from_str('x'))
        self.assertEqual(self.tf1.number_of_unknown_angles_at(4), 2)

    def test_sum_of_known_angles_at(self):
        self.assertEqual(self.tf1.sum_of_known_angles_at(4), 360)
        self.assertEqual(self.tf1.sum_of_known_angles_at(1), 60)
        self.tf1.set_angle_by_angle_points(1, 4, 3, Angle.from_str('x'))
        self.assertEqual(self.tf1.sum_of_known_angles_at(4), 230)
        self.tf1.set_angle_by_angle_points(3, 1, 4, Angle.from_str('x'))
        self.assertEqual(self.tf1.sum_of_known_angles_at(1), 40)

    def test_angle_points_of_unknown_angles_at(self):
        ang_pts = self.tf1.angle_points_of_unknown_angles_at(4)
        ang_pts2 = self.tf1.angle_points_of_unknown_angles_at(5)
        self.assertEqual(len(ang_pts), 0)
        self.assertEqual(len(ang_pts2), 0)

        self.tf1.set_angle_by_angle_points(6, 4, 5, Angle.from_str('x'))
        self.tf1.set_angle_by_angle_points(4, 5, 6, Angle.from_str('x'))
        self.tf1.set_angle_by_angle_points(6, 5, 2, Angle.from_str('x'))
        ang_pts = self.tf1.angle_points_of_unknown_angles_at(4)
        ang_pts2 = self.tf1.angle_points_of_unknown_angles_at(5)
        self.assertEqual(len(ang_pts), 1)
        self.assertEqual(len(ang_pts2), 2)
        self.assertTrue([6, 4, 5] in ang_pts)
        self.assertTrue([4, 5, 6] in ang_pts2)
        self.assertTrue([6, 5, 2] in ang_pts2)

    def test_complete_unknown_angle_at(self):
        self.tf1.set_angle_by_angle_points(1, 4, 3, Angle.from_str('x'))
        self.tf1.complete_unknown_angle_at(4)
        self.assertEqual(self.tf1.get_angle_by_angle_points(1, 4, 3), 130)
