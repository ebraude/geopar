import unittest
from geopar.tf_validator import TF_Validator
from geopar.triangulated_figure_class import TriangulatedFigure
from geopar.triangle_class import Triangle

__author__ = 'satbek'

# URL1:
# https://docs.google.com/presentation/d/1nddxo9JPaoxz-Colod8qd6Yuj_k7LXhBfO3JlVSYXrE/edit?usp=sharing

# URL 2:
# https://docs.google.com/presentation/d/1nddxo9JPaoxz-Colod8qd6Yuj_k7LXhBfO3JlVSYXrE/edit#slide=id.g13a65b87db_0_0


class TestTFValidator(unittest.TestCase):

    def setUp(self):
        self.validator = TF_Validator()
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

        # TriangulatedFigure tf_simple consists of 1 triangle t_simple
        # Appearance: URL2 at the top
        self.t_simple = Triangle([1,2,3],[50,70,60])
        self.tf_simple = TriangulatedFigure([self.t_simple])

    def test_rule_180(self):
        self.assertTrue(self.validator.check_180_rule(self.tf1))

    def test_rule_360(self):
        self.assertTrue(self.validator.check_360_rule(self.tf1))

    def test_rule_pairing(self):
        self.assertTrue(self.validator.check_pairing(self.tf1))

        with self.assertRaises(Exception):
            self.validator.check_180_rule(self.tf_empty)
