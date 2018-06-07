from python_linq import From
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
            From(1)

        From("a")
        From([1,2,3])

        self.assertTrue(True)

    def test_to_list(self):
        self.assertListEqual(
            self.simple,
            From(self.simple).to_list()
        )

    def test_simple_combination(self):
        obj = From(self.simple)
        self.assertTrue(3 in obj)
        self.assertTrue(2 in obj)

    def test_simple_select(self):
        expected = [2,3,4]

        obj = From(self.objects)
        
        result = obj.select(lambda x: x["value"]).to_list()

        self.assertEqual(result, expected)

    def test_shaping_select(self):
        expected = self.objects

        obj = From(self.simple)
        
        def shaper(x):
            return {"value": x}

        result = obj.select(shaper).to_list()

        self.assertListEqual(expected, result)

    def test_where(self):
        expected = [2, 4]
        obj = From(self.simple)

        result = obj.where(lambda x: x % 2 == 0).to_list()

        self.assertListEqual(expected, result)

    def test_select_many(self):
        expected = [1, 2, 3, 4]
        obj = From([[1, 2], [3, 4]])

        result = obj.select_many().to_list()

        self.assertListEqual(expected, result)

    def test_first(self):
        expected = 2
        result = From(self.simple).first()
        self.assertEqual(expected, result)

        expected = 3
        result = From(self.simple).first(lambda x: x % 2 != 0)
        self.assertEqual(expected, result)

        with self.assertRaises(NoSuchElementError):
            From(self.simple).first(lambda x: x > 5)

    def test_first_or_none(self):
        expected = 2
        result = From(self.simple).first()
        self.assertEqual(expected, result)

        expected = 3
        result = From(self.simple).first(lambda x: x % 2 != 0)
        self.assertEqual(expected, result)

        self.assertIsNone(From(self.simple).first_or_none(lambda x: x > 5))

    def test_distinct(self):
        expected = [1,2,3,4]
        subject = [1,1,1,1,1,1,1,1,2,3,3,3,3,3,4]

        result = From(subject).distinct().to_list()

        self.assertListEqual(expected, result)

        subject = [
            {
                "value": 1
            },
            {
                "value": 1
            },
            {
                "value": 1
            },
            {
                "value": 2
            },
            {
                "value": 2
            },
            {
                "value": 3
            }
        ]
        expected = [1, 2, 3]

        result = From(subject).distinct(lambda x: x["value"]).select(lambda x: x["value"]).to_list()

        self.assertListEqual(expected,result)

    def test_group_join(self):
        expected = [
            {
                "a": 1,
                "b": 4
            },
            {
                "a": 4,
                "b": 9
            },
            {
                "a": 9,
                "b": 16
            }
        ]
        subjA = [1, 2, 3]
        subjB = [1, 2, 3]

        result = From(subjA).group_join(
            subjB,
            lambda x: x,
            lambda x: x,
            lambda inner, outer: {"a": inner * inner, "b": (outer + 1) * (outer + 1)}
        ).to_list()

        self.assertListEqual(expected, result)

        