import unittest
from geopar.tf_elaborations_class import TF_Elaborations
from geopar.triangulated_figure_class import TriangulatedFigure
from geopar.triangle_class import Triangle
from geopar.angle_class import Angle
from geopar.tf_validator import TF_Validator

__author__ = 'satbek'

# URL1:
# https://docs.google.com/presentation/d/1nddxo9JPaoxz-Colod8qd6Yuj_k7LXhBfO3JlVSYXrE/edit?usp=sharing

# URL2:
# https://docs.google.com/presentation/d/1nddxo9JPaoxz-Colod8qd6Yuj_k7LXhBfO3JlVSYXrE/edit#slide=id.g13a06c4058_0_84

# URL3:
# https://docs.google.com/presentation/d/1nddxo9JPaoxz-Colod8qd6Yuj_k7LXhBfO3JlVSYXrE/edit#slide=id.g13a06c4058_0_179


class TestTFPreprocessor(unittest.TestCase):

    def setUp(self):
        self.preprocessor = TF_Elaborations()
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

        # TriangulatedFigure tf2 consists of seven Triangles tt1-tt7
        # Appearance: URL2 at the top
        self.tt1 = Triangle([1, 5, 4], [Angle([-1, -1, 60]), Angle([0, 1, 60]), Angle([1, 0, 60])])
        self.tt2 = Triangle([1, 3, 5], [Angle([-1, -1, 60]), Angle([0, 1, 0]), Angle([1, 0, 120])])
        self.tt3 = Triangle([5, 3, 6], [Angle([-1, -1, 120]), Angle([0, 1, 0]), Angle([1, 0, 60])])
        self.tt4 = Triangle([6, 3, 2], [Angle([-1, -1, 180]), Angle([0, 1, 0]), Angle([1, 0, 0])])
        self.tt5 = Triangle([4, 6, 2], [Angle([-1, -1, 120]), Angle([0, 1, 60]), Angle([1, 0, 0])])
        self.tt6 = Triangle([1, 4, 2], [Angle([-1, -1, 60]), Angle([0, 1, 120]), Angle([1, 0, 0])])
        self.tt7 = Triangle([4, 5, 6], [Angle([0, 0, 60]), Angle([0, 0, 60]), Angle([0, 0, 60])])
        self.tf2 = TriangulatedFigure([self.tt1, self.tt2, self.tt3, self.tt4, self.tt5, self.tt6, self.tt7])

        # TriangulatedFigure tf3 consists of seven Triangles ttt1-ttt7
        # Appearance: URL3 at the top
        self.ttt1 = Triangle([2, 6, 5], [Angle([0,1,0]), Angle.from_str('x'), Angle.from_str('x')])
        self.ttt2 = Triangle([2, 3, 6], [Angle([0,1,0]), Angle([-1,-1,60]), Angle.from_str('x')])
        self.ttt3 = Triangle([6, 3, 4], [Angle.from_str('x'), Angle([-1,-1,60]), Angle.from_str('x')])
        self.ttt4 = Triangle([4, 3, 1], [Angle.from_str('x'), Angle([-1,-1,60]), Angle([1,0,0])])
        self.ttt5 = Triangle([5, 4, 1], [Angle.from_str('x'), Angle.from_str('x'), Angle([1, 0, 0])])
        self.ttt6 = Triangle([2, 5, 1], [Angle([0,1,0]), Angle.from_str('x'), Angle([1,0,0])])
        self.ttt7 = Triangle([6, 4, 5], [Angle([0, 0, 60]), Angle([0, 0, 60]), Angle([0, 0, 60])])
        self.tf3 = TriangulatedFigure([self.ttt1, self.ttt2, self.ttt3, self.ttt4, self.ttt5, self.ttt6, self.ttt7])

    def test_theorem_2(self):
        validator = TF_Validator()
        if validator.check_180_rule(self.tf2):
            print('180 ok')
        if validator.check_360_rule(self.tf2):
            print('360 ok')
        if validator.check_pairing(self.tf2):
            print('pairing ok')

        preprocessor = TF_Elaborations()
        print('original:')
        print(self.tf2)
        self.tf2.set_angle_by_angle_points(6, 4, 5, Angle.from_str('x'))
        self.tf2.set_angle_by_angle_points(3, 5, 1, Angle.from_str('x'))
        self.tf2.set_angle_by_angle_points(2, 6, 3, Angle.from_str('x'))
        print('edited:')
        print(self.tf2)
        preprocessor.apply_360_rule_to(self.tf2)
        print('corrected:')
        print(self.tf2)

        self.assertTrue(True)

    def test_theorem_3(self):
        preprocessor = TF_Elaborations()
        print('original:')
        print(self.tf3)
        preprocessor.apply_pairing_to(self.tf3)
        print('after pairing:')
        print(self.tf3)
        pass
