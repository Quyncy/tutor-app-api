from django.test import SimpleTestCase

from app import calc

class CalcTests(SimpleTestCase):
    def test_add_num(self):
        res = calc.add(5, 6)

        self.assertEqual(res, 11)

    def test_substract_num(self):
        res = calc.substract(10, 5)

        self.assertEqual(res, 5)