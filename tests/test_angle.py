import unittest
from geopar.angle_class import Angle
from geopar.utilities import GREEK_LETTERS
from fractions import Fraction

__author__ = 'satbek'


class TestAngle(unittest.TestCase):
    def setUp(self):
        self.a_constant = Angle([90])
        self.a_constant_neg = Angle([-90])

        self.a_two1 = Angle([1, 45])
        self.a_two2 = Angle([0, 45])
        self.a_two3 = Angle([2, -45])
        self.a_two4 = Angle([0, -45])

        self.angle1 = Angle([1, 2, 3, 4, 5, 60])
        self.angle2 = Angle([2, 3, 4, 5, 6, 70])
        self.angle12 = Angle([3, 5, 7, 9, 11, 130])
        self.angle3 = Angle([2, 4, 6, 8, 100])
        self.angle4 = Angle([2, 4, 6, 8, 100])
        self.angle5 = Angle([0, 0, 0, 0, 0, 90])

    def test_init(self):
        # Force conversion of int, float coefficients to Fraction
        angle = Angle([1, 2, Fraction(3), 4.0, Fraction(1, 3)])
        for coef in angle.get_coefficients():
            self.assertTrue(isinstance(coef, Fraction))

    def test_add(self):
        # Angle + Angle
        self.assertEqual(Angle([10]) + Angle([20]), Angle([30]))
        self.assertEqual(Angle([1, 10]) + Angle([0, -20]), Angle([1, -10]))
        self.assertEqual(Angle([100, 101, 102, 103]) + Angle([10, 11, 12, 13]), Angle([110, 112, 114, 116]))

        # Angle + int
        self.assertEqual(Angle([1, 10]) + 90, Angle([1, 100]))
        self.assertEqual(Angle([1, 2, 3, 4, -10]) + 90, Angle([1, 2, 3, 4, 80]))

        # Angle + float
        self.assertEqual(Angle([1, 10]) + 1.5, Angle([1, 11.5]))
        self.assertEqual(Angle([-1, 0, -10]) + 1.5, Angle([-1, 0, -8.5]))

    def test_radd(self):
        # int + Angle
        self.assertEqual(90 + Angle([1, 10]), Angle([1, 100]))
        self.assertEqual(90 + Angle([1, 2, 3, 4, -10]), Angle([1, 2, 3, 4, 80]))

        # float + Angle
        self.assertEqual(1.5 + Angle([1, 10]), Angle([1, 11.5]))
        self.assertEqual(1.5 + Angle([-1, 0, -10]), Angle([-1, 0, -8.5]))

    def test_sub(self):
        # Angle - Angle
        self.assertEqual(Angle([10]) - Angle([20]), Angle([-10]))
        self.assertEqual(Angle([1, 10]) - Angle([-3, -20]), Angle([4, 30]))
        self.assertEqual(Angle([110, 112, 114, 116]) - Angle([10, 11, 12, 13]), Angle([100, 101, 102, 103]))

        # Angle - int
        self.assertEqual(Angle([1, 10]) - 90, Angle([1, -80]))
        self.assertEqual(Angle([1, 2, 3, 4, -10]) - 90, Angle([1, 2, 3, 4, -100]))

        # Angle - float
        self.assertEqual(Angle([1, 10]) - 1.5, Angle([1, 8.5]))
        self.assertEqual(Angle([-1, 0, -10]) - 1.5, Angle([-1, 0, -11.5]))

    def test_rsub(self):
        # int - Angle
        self.assertEqual(90 - Angle([1, 10]), Angle([-1, 80]))
        self.assertEqual(90 - Angle([1, 2, 3, 4, -10]), Angle([-1, -2, -3, -4, 100]))

        # float - Angle
        self.assertEqual(1.5 - Angle([1, 10]), Angle([-1, -8.5]))
        self.assertEqual(1.5 - Angle([-1, 0, -10]), Angle([1, 0, 11.5]))

    def test_truediv(self):
        a = Angle([120])
        b = Angle([1, 2, 3, 30])

        # Angle / int
        self.assertEqual(a / .5, Angle([240]))
        self.assertEqual(b / 2, Angle([.5, 1, 1.5, 15]))
        self.assertEqual(b / 1, b)

        # Angle / float
        self.assertEqual(b / .5, Angle([2, 4, 6, 60]))
        self.assertEqual(b / 2.0, Angle([.5, 1, 1.5, 15]))
        self.assertEqual(b / 1.0, b)

    def test_mul(self):
        b = Angle([1, 2, 3, 30])

        # Angle * int
        self.assertEqual(b * 2, Angle([2, 4, 6, 60]))
        self.assertEqual(b * 1, b)

        # Angle * float
        self.assertEqual(b * .5, Angle([.5, 1, 1.5, 15]))
        self.assertEqual(b * 2.0, Angle([2, 4, 6, 60]))
        self.assertEqual(b * 1.0, b)

    def test_rmul(self):
        a = Angle([])
        b = Angle([1, 2, 3, 30])

        # Angle * int
        self.assertEqual(2 * b, Angle([2, 4, 6, 60]))
        self.assertEqual(1 * b, b)
        # Angle * float
        self.assertEqual(.5 * b, Angle([.5, 1, 1.5, 15]))
        self.assertEqual(2.0 * b, Angle([2, 4, 6, 60]))
        self.assertEqual(1.0 * b, b)

    def test_eq(self):
        b = Angle([1, 2, 3, 30])
        c = Angle([90])

        # Angle == Angle
        self.assertTrue(b == Angle([1, 2, 3, 30]))
        self.assertTrue(b == b)
        # int == Angle
        self.assertTrue(90 == c)
        # Angle == int
        self.assertTrue(c == 90)
        # float == Angle
        self.assertTrue(90.0 == c)
        # Angle == float
        self.assertTrue(c == 90.0)

    def test_ne(self):
        a = Angle([])
        b = Angle([1, 2, 3, 30])
        c = Angle([90])

        # Angle != Angle
        self.assertTrue(b != Angle([2, 2, 3, 30]))
        self.assertFalse(b != b)
        # int != Angle
        self.assertTrue(100 != c)
        # Angle != int
        self.assertFalse(c != 90)
        # float != Angle
        self.assertTrue(90.1 != c)
        # Angle != float
        self.assertFalse(c != 90.0)

    def test_str(self):
        print(self.a_constant)
        print(self.a_constant_neg)
        print(self.a_two1)
        print(self.a_two2)
        print(self.a_two3)
        print(self.a_two4)

    def test_from_str(self):
        a_str = '-1 2/4 -3/5 40.00 -599 6/1'
        a = Angle.from_str(a_str)
