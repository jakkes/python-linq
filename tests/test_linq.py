from python_linq import From
from python_linq.core import Grouping
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

    def test_all(self):
        self.assertFalse(From([1, 2, 3, 4, 5, 6]).all(lambda x: x == 4))

        self.assertTrue(From([1, 2, 3, 4, 5, 6]).all(lambda x: x < 7))

        subject = [
            {
                "id": 1,
                "value": 2
            },{
                "id": 2,
                "value": 3
            }
        ]
        self.assertTrue(
            From(subject).any(
                lambda x: x["value"] == 2 or x["value"] == 3
            )
        )

    def test_any(self):
        self.assertTrue(From([1, 2, 3, 4, 5, 6]).any(lambda x: x == 4))

        self.assertFalse(From([1, 2, 3, 4, 5, 6]).any(lambda x: x > 6))

        subject = [
            {
                "id": 1,
                "value": 2
            },{
                "id": 2,
                "value": 3
            }
        ]
        self.assertTrue(From(subject).any(lambda x: x["value"] == 2))

    def test_average(self):
        subject = [1, 2, 3, 4, 5]
        self.assertEqual(
            From(subject).average(),
            3
        )

        self.assertEqual(
            From(subject).average(lambda x: x*x),
            11
        )

        subject = [
            { "value": 1 },
            { "value": 2 },
            { "value": 3 }
        ]
        self.assertEqual(
            From(subject).average(lambda x: x["value"]),
            2
        )

    def test_concat(self):
        
        subjectA = [1, 2, 3]
        subjectB = [4, 5, 6]
        
        self.assertListEqual(
            From(subjectA).concat(subjectB).toList(),
            [1, 2, 3, 4, 5, 6]
        )

        subjectA = [
            { "value": 1},
            { "value": 2}
        ]
        subjectB = [
            { "value": 3 },
            { "value": 4 }
        ]
        self.assertListEqual(
            From(subjectA).select(lambda x: x["value"]).concat(
                From(subjectB).select(lambda x: x["value"])
            ).toList(),
            [1, 2, 3, 4]
        )

    def test_contains(self):
        self.assertTrue(From([1, 2, 3, 4]).contains(2))

        self.assertFalse(From([1, 2, 3, 4]).contains(5))

    def test_count(self):
        self.assertEqual(
            From([1, 2, 3, 4, 5, 6]).count(),
            6
        )

        self.assertEqual(
            From([1, 2, 3, 4, 5, 6]).count(lambda x: x > 3),
            3
        )

        subject = [
            {
                "id": 1,
                "value": 2
            },{
                "id": 2,
                "value": 3
            }
        ]
        self.assertEqual(
            From(subject).count(lambda x: x["value"] > 2),
            1
        )

    def test_distinct(self):
        subject = [1, 1, 2, 3, 3, 3]
        self.assertListEqual(
            From(subject).distinct().toList(),
            [1, 2, 3]
        )

        subject = [
            {
                "id": 1,
                "value": 3
            }, {
                "id": 1,
                "value": 3
            }, {
                "id": 2,
                "value": 4
            }, {
                "id": 2,
                "value": 4
            }
        ]
        self.assertListEqual(
            From(subject).distinct(lambda x: x["id"]).select(lambda x: x["value"]).toList(),
            [3, 4]
        )

        expected = [1,2,3,4]
        subject = [1,1,1,1,1,1,1,1,2,3,3,3,3,3,4]

        result = From(subject).distinct().toList()

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

        result = From(subject).distinct(lambda x: x["value"]).select(lambda x: x["value"]).toList()

        self.assertListEqual(expected,result)

    def test_elementat(self):
        subject = [1, 2, 3, 4]
        self.assertEqual(
            From(subject).elementAt(2),
            3
        )

        with self.assertRaises(IndexError):
            From(subject).elementAt(4)

        subject = [
            { "value": 1 },
            { "value": 2 }
        ]
        self.assertDictEqual(
            From(subject).elementAt(0),
            { "value": 1 }
        )

    def test_elementatornone(self):
        
        subject = [1, 2, 3, 4]
        self.assertEqual(
            From(subject).elementAtOrNone(2),
            3
        )

        self.assertIsNone(From(subject).elementAtOrNone(4))

        subject = [
            { "value": 1 },
            { "value": 2 }
        ]
        self.assertDictEqual(
            From(subject).elementAtOrNone(0),
            { "value": 1 }
        )

    def test_first(self):
        subject = [1, 2, 3, 4]
        self.assertEqual(
            From(subject).first(lambda x: x % 2 == 0),
            2
        )

        self.assertEqual(
            From(subject).first(),
            1
        )

        with self.assertRaises(NoSuchElementError):
            From(subject).first(lambda x: x > 4)

        subject = [
            { "value": 1 },
            { "value": 2 }
        ]
        self.assertDictEqual(
            From(subject).first(lambda x: x["value"] == 2),
            { "value": 2 }
        )

        expected = 2
        result = From(self.simple).first()
        self.assertEqual(expected, result)

        expected = 3
        result = From(self.simple).first(lambda x: x % 2 != 0)
        self.assertEqual(expected, result)

        with self.assertRaises(NoSuchElementError):
            From(self.simple).first(lambda x: x > 5)

    def test_firstornone(self):
        subject = [1, 2, 3, 4]
        self.assertEqual(
            From(subject).firstOrNone(lambda x: x % 2 == 0),
            2
        )

        self.assertIsNone(From(subject).firstOrNone(lambda x: x > 4))

        subject = [ 
            { "value": 1 },
            { "value": 2 }
        ]
        self.assertDictEqual(
            From(subject).first(lambda x: x["value"] == 2),
            { "value": 2 }
        )

    def test_groupby(self):
        subject = [
            {
                "id": 1,
                "data": 1
            },
            {
                "id": 1,
                "data": 2
            },
            {
                "id": 2,
                "data": 3
            },
            {
                "id": 2,
                "data": 4
            },
            {
                "id": 3,
                "data": 5
            },
            {
                "id": 4,
                "data": 6
            }
        ]

        result = (
            From(subject)
            .groupBy(lambda x: x["id"], lambda x: x["data"])
            .select(lambda x: x.values)
            .toList()
        )
        expected = [[1, 2], [3, 4], [5], [6]]
        self.assertListEqual(result, expected)

        result = (
            From(subject)
            .groupBy(lambda x: x["id"], lambda x: x["data"])
            .select(
                lambda x: From(x.values).max()
            )
            .toList()
        )
        expected = [2, 4, 5, 6]
        self.assertListEqual(result, expected)

        subject = [
            {
                "age": 10,
                "name": "Steven"
            }, {
                "age": 10,
                "name": "Johan"
            }, {
                "age": 11,
                "name": "Lars"
            }
        ]
        
        # Keys
        self.assertListEqual(

            From(subject).groupBy(
                lambda x: x["age"], 
                transform = lambda x: x["name"]
            ).select(lambda x: x.key).toList(),

            [10, 11]
        )

        # Names
        self.assertListEqual(
            
            From(subject).groupBy(
                lambda x: x["age"],
                transform=lambda x: x["name"]
            ).select(lambda x: x.values).toList(),

            [ ["Steven", "Johan" ], [ "Lars" ] ]
        )

    def test_intersect(self):
        subject1 = [1,2,3,4]
        subject2 = [3,4,5,6]

        result = From(subject1).intersect(subject2).toList()
        expected = [3,4]
        self.assertListEqual(result,expected)

        subjectA = [
            {
                "id": 1,
                "value": 3
            }, {
                "id": 2,
                "value": 4
            }
        ]
        subjectB = [
            {
                "id": 2,
                "value": 4
            }, {
                "id": 3,
                "value": 5
            }
        ]
        result = From(subjectA).intersect(subjectB, key=lambda x: x["id"]).select(lambda x: x["value"]).toList()
        expected = [4]
        self.assertListEqual(expected, result)

        subjectA = [1, 2, 3, 4]
        subjectB = [3, 4, 5, 6]
        self.assertListEqual(
            From(subjectA).intersect(subjectB).toList(),
            [3, 4]
        )

        subjectA = [
            {
                "id": 1,
                "value": 3
            }, {
                "id": 2,
                "value": 4
            }
        ]
        subjectB = [
            {
                "id": 2,
                "value": 4
            }, {
                "id": 3,
                "value": 5
            }
        ]
        self.assertListEqual(
            From(subjectA).intersect(subjectB, key=lambda x: x["id"]).select(lambda x: x["value"]).toList(),
            [4]
        )

    def test_last(self):
        subject = [1, 2, 3, 4]
        self.assertEqual(
            From(subject).last(lambda x: x < 4),
            3
        )

        self.assertEqual(
            From(subject).last(),
            4
        )

        with self.assertRaises(NoSuchElementError):
            From(subject).last(lambda x: x > 4)

        subject = [
            { "value": 1 },
            { "value": 2 }
        ]
        self.assertDictEqual(
            From(subject).last(lambda x: x["value"] > 0),
            { "value": 2 }
        )

    def test_lastornone(self):
        subject = [1, 2, 3, 4]
        self.assertEqual(
            From(subject).lastOrNone(lambda x: x % 2 == 0),
            4
        )

        self.assertIsNone(
            From(subject).lastOrNone(lambda x: x > 4)
        )

        subject = [ 
            { "value": 1 },
            { "value": 2 }
        ]
        self.assertDictEqual(
            From(subject).last(lambda x: x["value"] > 0),
            { "value": 2 }
        )

    def test_max(self):
        subject = [1, 2, 3, 4]
        self.assertEqual(
            From(subject).max(),
            4
        )

        subject = [
            { "value" : 1 },
            { "value" : 2 }
        ]
        self.assertEqual(
            From(subject).max(lambda x: x["value"]),
            2
        )

    def test_min(self):
        subject = [1, 2, 3, 4]
        self.assertEqual(
            From(subject).min(),
            1
        )

        subject = [
            { "value" : 1 },
            { "value" : 2 }
        ]
        self.assertEqual(
            From(subject).min(lambda x: x["value"]),
            1
        )

    def test_select(self):
        subject = [
            {
                "id": 1,
                "value": 2
            }, {
                "id": 2,
                "value": 3
            }
        ]
        self.assertListEqual(
            From(subject).select(lambda x: x["value"]).toList(),
            [2, 3]
        )

        subject = [1, 2]
        def shape(x):
            return {
                "value": x
            }
        
        self.assertListEqual(
            From(subject).select(shape).toList(),
            [ {"value": 1}, {"value": 2} ]
        )

    def test_selectmany(self):
        expected = [1, 2, 3, 4]
        obj = From([[1, 2], [3, 4]])

        result = obj.selectMany().toList()

        self.assertListEqual(expected, result)

        subject = [
            [1, 2, 3, 4],
            [5, 6, 7, 8]
        ]
        self.assertListEqual(
            From(subject).selectMany().toList(),
            [1, 2, 3, 4, 5, 6, 7, 8]
        )

        subject = [
            [{"value": 1}, {"value": 2}],
            [{"value": 3}, {"value": 4}]
        ]
        self.assertListEqual(
            From(subject).selectMany(lambda x: x["value"]).toList(),
            [1, 2, 3, 4]
        )

    def test_sum(self):
        subject = [1, 2, 3, 4, 5]
        self.assertEqual(
            From(subject).sum(),
            15
        )

        self.assertEqual(
            From(subject).sum(lambda x: x*x),
            55
        )

        subject = [
            { "value": 1 },
            { "value": 2 },
            { "value": 3 }
        ]
        self.assertEqual(
            From(subject).sum(lambda x: x["value"]),
            6
        )

    def test_tolist(self):
        self.assertListEqual(
            From([1, 2, 3, 4]).select(lambda x: x*x).toList(),
            [1, 4, 9, 16]
        )

        self.assertListEqual(
            From([1, 2, 3, 4]).toList(),
            [1, 2, 3, 4]
        )

    def test_foreach(self):
        res = []

        subject = [1, 2, 3]
        From(subject).forEach(lambda x: res.append(x))
        self.assertListEqual(
            res,
            subject
        )

    def test_where(self):
        expected = [2, 4]
        obj = From(self.simple)

        result = obj.where(lambda x: x % 2 == 0).toList()

        self.assertListEqual(expected, result)

        subject = [1, 2, 3, 4, 5, 6]
        self.assertListEqual(
            From(subject).where(lambda x: x > 3).toList(),
            [4, 5, 6]
        )

        subject = [
            { "value": 2 },
            { "value": 3 }
        ]
        self.assertListEqual(
            From(subject).where(lambda x: x["value"] == 3).select(lambda x: x["value"]).toList(),
            [3]
        )

    def test_groupjoin(self):
        grades = [
            {
                "userid": 1,
                "grade": "A"
            }, {
                "userid": 1,
                "grade": "B"
            }, {
                "userid": 2,
                "grade": "B"
            }, {
                "userid": 2,
                "grade": "B"
            }
        ]
        students = [
            {
                "id": 1,
                "name": "Jakob"
            }, {
                "id": 2,
                "name": "Johan"
            }
        ]
        
        self.assertListEqual(
            
            From(students).groupJoin(
                grades,
                innerKey = lambda x: x["id"],
                outerKey = lambda x: x["userid"],
                innerTransform = lambda x: x["name"],
                outerTransform = lambda x: x["grade"]
            ).select(lambda x: x.inner).toList(),
            
            ['Jakob', 'Johan']
        )

        self.assertListEqual(

            From(students).groupJoin(
                grades,
                innerKey = lambda x: x["id"],
                outerKey = lambda x: x["userid"],
                innerTransform = lambda x: x["name"],
                outerTransform = lambda x: x["grade"]
            ).select(lambda x: x.outer).toList(),

            [ ['A', 'B'], ['B', 'B'] ]
        )

        subjA = [1, 2, 3]
        subjB = [2, 2, 3, 4]

        result = From(subjA).groupJoin(
            subjB,
            lambda x: x,
            lambda x: x
        ).select(lambda x: x.outer).toList()
        expected = [[], [2, 2], [3]]
        self.assertListEqual(expected, result)

        grades = [
            {
                "userid": 1,
                "grade": "A"
            }, {
                "userid": 1,
                "grade": "B"
            }, {
                "userid": 2,
                "grade": "B"
            }, {
                "userid": 2,
                "grade": "B"
            }
        ]
        students = [
            {
                "id": 1,
                "name": "Jakob"
            }, {
                "id": 2,
                "name": "Johan"
            }
        ]
        names = From(students).groupJoin(
            grades,
            innerKey = lambda x: x["id"],
            outerKey = lambda x: x["userid"],
            innerTransform = lambda x: x["name"],
            outerTransform = lambda x: x["grade"]
        ).select(lambda x: x.inner).toList()

        expected = ["Jakob", "Johan"]
        self.assertListEqual(
            names,
            expected
        )

        grades = From(students).groupJoin(
            grades,
            innerKey = lambda x: x["id"],
            outerKey = lambda x: x["userid"],
            innerTransform = lambda x: x["name"],
            outerTransform = lambda x: x["grade"]
        ).select(lambda x: x.outer).toList()

        expected = [["A","B"], ["B","B"]]
        self.assertListEqual(
            grades,
            expected
        )

    def test_join(self):
        subjA = [1, 2, 3, 4, 5]
        subjB = [2, 3, 4, 5, 6]
        self.assertListEqual(
            
            From(subjA).join(
                subjB,
                lambda x: x,
                lambda x: x+1,
                lambda x, y: {"inner": x, "outer": y}
            ).toList(),

            [
                { "inner": 3, "outer": 2},
                { "inner": 4, "outer": 3},
                { "inner": 5, "outer": 4}
            ]
        )

        subject1 = [
            {
                "id": 1,
                "A": 2
            },
            {
                "id": 2,
                "A": 3
            },
            {
                "id": 3,
                "A": 4
            },
            {
                "id": 4,
                "A": 5
            },
            {
                "id": 5,
                "A": 6
            }
        ]
        subject2 = [
            {
                "id": 1,
                "B": 11
            },
            {
                "id": 2,
                "B": 12
            },
            {
                "id": 3,
                "B": 13
            },
            {
                "id": 4,
                "B": 14
            }
        ]

        result = (
            From(subject1)
            .join(
                subject2,
                lambda x: x["id"],
                lambda x: x["id"],
                lambda inner, outer: { "A": inner["A"], "B": outer["B"] }
            )
            .toList()
        )
        expected = [
            {
                "A": 2,
                "B": 11
            },
            {
                "A": 3,
                "B": 12
            },
            {
                "A": 4,
                "B": 13
            },
            {
                "A": 5,
                "B": 14
            }
        ]
        self.assertListEqual(expected, result)

    def test_take(self):
        self.assertListEqual(
            From([1, 2, 3]).take(2).toList(),
            [1, 2]
        )

    def test_takewhile(self):
        self.assertListEqual(
            From([1, 2, 3, 4, 5, 6]).takeWhile(lambda x: x % 3 != 0).toList(),
            [1, 2]
        )

    def test_order(self):
        self.assertListEqual(
            From([1, 2, 4, 3, 7, 6, 5]).order(descending=True).toList(),
            [7, 6, 5, 4, 3, 2, 1]
        )

        self.assertListEqual(
            From([1, 2, 4, 3, 7, 6, 5]).order().toList(),
            [1, 2, 3, 4, 5, 6, 7]
        )

        self.assertListEqual(
            From([1, 2, 4, 3, 7, 6, 5]).order(key=lambda x: x % 3).toList(),
            [3, 6, 1, 4, 7, 2, 5]
        )

    def test_union(self):
        self.assertListEqual(
            From([1, 2, 3]).union([3, 4, 5]).toList(),
            [1, 2, 3, 4, 5]
        )

        self.assertListEqual(
            From([1, 2, 3]).union([3, 4, 5], key = lambda x: x % 4).toList(),
            [1, 2, 3, 4] # Note 5 == 2 in modulo 4
        )

        self.assertListEqual(
            From([1, 2, 3]).union([3, 4, 5], transform = lambda x: x + 1).toList(),
            [2, 3, 4, 5, 6]
        )

    def test_wrapper(self):
        with self.assertRaises(ValueError):
            From(1)

        From("a")
        From([1,2,3])

        self.assertTrue(True)

    def test_skip(self):
        self.assertListEqual(
            From([1,2,3,4,5,6,7]).skip(3).toList(),
            [4,5,6,7]
        )

    def test_skipWhile(self):
        self.assertListEqual(
            From([1,2,3,4,5,6,7]).skipWhile(lambda x: x < 3).toList(),
            [3,4,5,6,7]
        )

        self.assertListEqual(
            From([1,2,3,4,5,6,7]).skipWhile(lambda x: x % 3 != 0).toList(),
            [3,4,5,6,7]
        )

    def test_toDict(self):
        self.assertDictEqual(
            From([1,2,3,4]).toDict(lambda x: str(x*x)),
            {
                '1': 1,
                '4': 2,
                '9': 3,
                '16': 4
            }
        )

        self.assertDictEqual(
            From([1,2,3,4]).toDict(lambda x: str(x), transform = lambda x: x*x),
            {
                '1': 1,
                '2': 4,
                '3': 9,
                '4': 16
            }
        )

        with self.assertRaises(KeyError):
            From([1,2,3,4]).toDict(lambda x: str(x % 3))