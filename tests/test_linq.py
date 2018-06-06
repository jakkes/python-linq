from python_linq import Linq
from python_linq.linq_exceptions import *
import unittest

class TestBasicFunctions(unittest.TestCase):
    def setUp(self):
        self.simple = [2,3,4]
        self.objects = [
            {
                "value": 2
            },{
                "value": 3
            },{
                "value": 4
            }
        ]

    def test_wrapper(self):
        with self.assertRaises(ValueError):
            Linq(1)

        Linq("a")
        Linq([1,2,3])

        self.assertTrue(True)

    def test_to_list(self):
        self.assertListEqual(
            self.simple,
            Linq(self.simple).to_list()
        )

    def test_simple_combination(self):
        obj = Linq(self.simple)
        self.assertTrue(3 in obj)
        self.assertTrue(2 in obj)

    def test_simple_select(self):
        expected = [2,3,4]

        obj = Linq(self.objects)
        
        result = obj.select(lambda x: x["value"]).to_list()

        self.assertEqual(result, expected)

    def test_shaping_select(self):
        expected = self.objects

        obj = Linq(self.simple)
        
        def shaper(x):
            return {"value": x}

        result = obj.select(shaper).to_list()

        self.assertListEqual(expected, result)

    def test_where(self):
        expected = [2, 4]
        obj = Linq(self.simple)

        result = obj.where(lambda x: x % 2 == 0).to_list()

        self.assertListEqual(expected, result)

    def test_select_many(self):
        expected = [1, 2, 3, 4]
        obj = Linq([[1, 2], [3, 4]])

        result = obj.select_many().to_list()

        self.assertListEqual(expected, result)

    def test_first(self):
        expected = 2
        result = Linq(self.simple).first()
        self.assertEqual(expected, result)

        expected = 3
        result = Linq(self.simple).first(lambda x: x % 2 != 0)
        self.assertEqual(expected, result)

        with self.assertRaises(NoSuchElementError):
            Linq(self.simple).first(lambda x: x > 5)

    def test_first_or_none(self):
        expected = 2
        result = Linq(self.simple).first()
        self.assertEqual(expected, result)

        expected = 3
        result = Linq(self.simple).first(lambda x: x % 2 != 0)
        self.assertEqual(expected, result)

        self.assertIsNone(Linq(self.simple).first_or_none(lambda x: x > 5))