from linq import Query, Grouping, errors
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
        self.assertFalse(Query([1, 2, 3, 4, 5, 6]).all(lambda x: x == 4))

        self.assertTrue(Query([1, 2, 3, 4, 5, 6]).all(lambda x: x < 7))

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
            Query(subject).any(
                lambda x: x["value"] == 2 or x["value"] == 3
            )
        )

    def test_any(self):
        self.assertTrue(Query([1, 2, 3, 4, 5, 6]).any(lambda x: x == 4))

        self.assertFalse(Query([1, 2, 3, 4, 5, 6]).any(lambda x: x > 6))

        subject = [
            {
                "id": 1,
                "value": 2
            },{
                "id": 2,
                "value": 3
            }
        ]
        self.assertTrue(Query(subject).any(lambda x: x["value"] == 2))

    def test_average(self):
        subject = [1, 2, 3, 4, 5]
        self.assertEqual(
            Query(subject).average(),
            3
        )

        self.assertEqual(
            Query(subject).select(lambda x: x*x).average(),
            11
        )

        subject = [
            { "value": 1 },
            { "value": 2 },
            { "value": 3 }
        ]
        self.assertEqual(
            Query(subject).select(lambda x: x["value"]).average(),
            2
        )

    def test_concat(self):
        
        subjectA = [1, 2, 3]
        subjectB = [4, 5, 6]
        
        self.assertListEqual(
            Query(subjectA).concat(subjectB).toList(),
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
            Query(subjectA).select(lambda x: x["value"]).concat(
                Query(subjectB).select(lambda x: x["value"])
            ).toList(),
            [1, 2, 3, 4]
        )

    def test_contains(self):
        self.assertTrue(Query([1, 2, 3, 4]).contains(2))

        self.assertFalse(Query([1, 2, 3, 4]).contains(5))

    def test_count(self):
        self.assertEqual(
            Query([1, 2, 3, 4, 5, 6]).count(),
            6
        )

        self.assertEqual(
            Query([1, 2, 3, 4, 5, 6]).count(lambda x: x > 3),
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
            Query(subject).count(lambda x: x["value"] > 2),
            1
        )

    def test_distinct(self):
        subject = [1, 1, 2, 3, 3, 3]
        self.assertListEqual(
            Query(subject).distinct().toList(),
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
            Query(subject).distinct(lambda x: x["id"]).select(lambda x: x["value"]).toList(),
            [3, 4]
        )

        expected = [1,2,3,4]
        subject = [1,1,1,1,1,1,1,1,2,3,3,3,3,3,4]

        result = Query(subject).distinct().toList()

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

        result = Query(subject).distinct(lambda x: x["value"]).select(lambda x: x["value"]).toList()

        self.assertListEqual(expected,result)

    def test_elementat(self):
        subject = [1, 2, 3, 4]
        self.assertEqual(
            Query(subject).elementAt(2),
            3
        )

        with self.assertRaises(IndexError):
            Query(subject).elementAt(4)

        subject = [
            { "value": 1 },
            { "value": 2 }
        ]
        self.assertDictEqual(
            Query(subject).elementAt(0),
            { "value": 1 }
        )

    def test_elementatornone(self):
        
        subject = [1, 2, 3, 4]
        self.assertEqual(
            Query(subject).elementAtOrNone(2),
            3
        )

        self.assertIsNone(Query(subject).elementAtOrNone(4))

        subject = [
            { "value": 1 },
            { "value": 2 }
        ]
        self.assertDictEqual(
            Query(subject).elementAtOrNone(0),
            { "value": 1 }
        )

    def test_first(self):
        subject = [1, 2, 3, 4]
        self.assertEqual(
            Query(subject).first(lambda x: x % 2 == 0),
            2
        )

        self.assertEqual(
            Query(subject).first(),
            1
        )

        with self.assertRaises(errors.NoSuchElementError):
            Query(subject).first(lambda x: x > 4)

        subject = [
            { "value": 1 },
            { "value": 2 }
        ]
        self.assertDictEqual(
            Query(subject).first(lambda x: x["value"] == 2),
            { "value": 2 }
        )

        expected = 2
        result = Query(self.simple).first()
        self.assertEqual(expected, result)

        expected = 3
        result = Query(self.simple).first(lambda x: x % 2 != 0)
        self.assertEqual(expected, result)

        with self.assertRaises(errors.NoSuchElementError):
            Query(self.simple).first(lambda x: x > 5)

    def test_firstornone(self):
        subject = [1, 2, 3, 4]
        self.assertEqual(
            Query(subject).firstOrNone(lambda x: x % 2 == 0),
            2
        )

        self.assertIsNone(Query(subject).firstOrNone(lambda x: x > 4))

        subject = [ 
            { "value": 1 },
            { "value": 2 }
        ]
        self.assertDictEqual(
            Query(subject).first(lambda x: x["value"] == 2),
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
            Query(subject)
            .groupBy(lambda x: x["id"], lambda x: x["data"])
            .select(lambda x: x.values)
            .toList()
        )
        expected = [[1, 2], [3, 4], [5], [6]]
        self.assertListEqual(result, expected)

        result = (
            Query(subject)
            .groupBy(lambda x: x["id"], lambda x: x["data"])
            .select(
                lambda x: Query(x.values).max()
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

            Query(subject).groupBy(
                lambda x: x["age"], 
                transform = lambda x: x["name"]
            ).select(lambda x: x.key).toList(),

            [10, 11]
        )

        # Names
        self.assertListEqual(
            
            Query(subject).groupBy(
                lambda x: x["age"],
                transform=lambda x: x["name"]
            ).select(lambda x: x.values).toList(),

            [ ["Steven", "Johan" ], [ "Lars" ] ]
        )

    def test_intersect(self):
        subject1 = [1,2,3,4]
        subject2 = [3,4,5,6]

        result = Query(subject1).intersect(subject2).toList()
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
        result = Query(subjectA).intersect(subjectB, key=lambda x: x["id"]).select(lambda x: x["value"]).toList()
        expected = [4]
        self.assertListEqual(expected, result)

        subjectA = [1, 2, 3, 4]
        subjectB = [3, 4, 5, 6]
        self.assertListEqual(
            Query(subjectA).intersect(subjectB).toList(),
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
            Query(subjectA).intersect(subjectB, key=lambda x: x["id"]).select(lambda x: x["value"]).toList(),
            [4]
        )

    def test_last(self):
        subject = [1, 2, 3, 4]
        self.assertEqual(
            Query(subject).last(lambda x: x < 4),
            3
        )

        self.assertEqual(
            Query(subject).last(),
            4
        )

        with self.assertRaises(errors.NoSuchElementError):
            Query(subject).last(lambda x: x > 4)

        subject = [
            { "value": 1 },
            { "value": 2 }
        ]
        self.assertDictEqual(
            Query(subject).last(lambda x: x["value"] > 0),
            { "value": 2 }
        )

    def test_lastornone(self):
        subject = [1, 2, 3, 4]
        self.assertEqual(
            Query(subject).lastOrNone(lambda x: x % 2 == 0),
            4
        )

        self.assertIsNone(
            Query(subject).lastOrNone(lambda x: x > 4)
        )

        subject = [ 
            { "value": 1 },
            { "value": 2 }
        ]
        self.assertDictEqual(
            Query(subject).last(lambda x: x["value"] > 0),
            { "value": 2 }
        )

    def test_argmax(self):
        subject = [1, 2, 3, 4]
        self.assertEqual(
            Query(subject).argmax(lambda x: x),
            4
        )

        subject = [
            { "value" : 1 },
            { "value" : 2 }
        ]
        self.assertEqual(
            Query(subject).argmax(lambda x: x["value"]),
            { "value": 2 }
        )

    def test_max(self):
        subject = [1, 2, 3, 4]
        self.assertEqual(
            Query(subject).max(),
            4
        )

        subject = [
            { "value" : 1 },
            { "value" : 2 }
        ]
        self.assertEqual(
            Query(subject).select(lambda x: x["value"]).max(),
            2
        )

    def test_argmin(self):
        subject = [1, 2, 3, 4]
        self.assertEqual(
            Query(subject).argmin(lambda x: x),
            1
        )

        subject = [
            { "value" : 1 },
            { "value" : 2 }
        ]
        self.assertEqual(
            Query(subject).argmin(lambda x: x["value"]),
            { "value": 1 }
        )

    def test_min(self):
        subject = [1, 2, 3, 4]
        self.assertEqual(
            Query(subject).min(),
            1
        )

        subject = [
            { "value" : 1 },
            { "value" : 2 }
        ]
        self.assertEqual(
            Query(subject).select(lambda x: x["value"]).min(),
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
            Query(subject).select(lambda x: x["value"]).toList(),
            [2, 3]
        )

        subject = [1, 2]
        def shape(x):
            return {
                "value": x
            }
        
        self.assertListEqual(
            Query(subject).select(shape).toList(),
            [ {"value": 1}, {"value": 2} ]
        )

    def test_selectmany(self):
        expected = [1, 2, 3, 4]
        obj = Query([[1, 2], [3, 4]])

        result = obj.selectMany().toList()

        self.assertListEqual(expected, result)

        subject = [
            [1, 2, 3, 4],
            [5, 6, 7, 8]
        ]
        self.assertListEqual(
            Query(subject).selectMany().toList(),
            [1, 2, 3, 4, 5, 6, 7, 8]
        )

        subject = [
            [{"value": 1}, {"value": 2}],
            [{"value": 3}, {"value": 4}]
        ]
        self.assertListEqual(
            Query(subject).selectMany(lambda x: x["value"]).toList(),
            [1, 2, 3, 4]
        )

    def test_sum(self):
        subject = [1, 2, 3, 4, 5]
        self.assertEqual(
            Query(subject).sum(),
            15
        )

        self.assertEqual(
            Query(subject).select(lambda x: x*x).sum(),
            55
        )

        subject = [
            { "value": 1 },
            { "value": 2 },
            { "value": 3 }
        ]
        self.assertEqual(
            Query(subject).select(lambda x: x["value"]).sum(),
            6
        )

    def test_tolist(self):
        self.assertListEqual(
            Query([1, 2, 3, 4]).select(lambda x: x*x).toList(),
            [1, 4, 9, 16]
        )

        self.assertListEqual(
            Query([1, 2, 3, 4]).toList(),
            [1, 2, 3, 4]
        )

    def test_foreach(self):
        res = []

        subject = [1, 2, 3]
        Query(subject).forEach(lambda x: res.append(x))
        self.assertListEqual(
            res,
            subject
        )

    def test_where(self):
        expected = [2, 4]
        obj = Query(self.simple)

        result = obj.where(lambda x: x % 2 == 0).toList()

        self.assertListEqual(expected, result)

        subject = [1, 2, 3, 4, 5, 6]
        self.assertListEqual(
            Query(subject).where(lambda x: x > 3).toList(),
            [4, 5, 6]
        )

        subject = [
            { "value": 2 },
            { "value": 3 }
        ]
        self.assertListEqual(
            Query(subject).where(lambda x: x["value"] == 3).select(lambda x: x["value"]).toList(),
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
            
            Query(students).groupJoin(
                grades,
                innerKey = lambda x: x["id"],
                outerKey = lambda x: x["userid"],
                innerTransform = lambda x: x["name"],
                outerTransform = lambda x: x["grade"]
            )
            .select(lambda x: x.inner).toList(),
            
            ['Jakob', 'Johan']
        )

        self.assertListEqual(

            Query(students).groupJoin(
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

        result = Query(subjA).groupJoin(
            subjB,
            lambda x: x,
            lambda x: x,
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
        names = Query(students).groupJoin(
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

        grades = Query(students).groupJoin(
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
            
            Query(subjA).join(
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
            Query(subject1)
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
            Query([1, 2, 3]).take(2).toList(),
            [1, 2]
        )

    def test_takewhile(self):
        self.assertListEqual(
            Query([1, 2, 3, 4, 5, 6]).takeWhile(lambda x: x % 3 != 0).toList(),
            [1, 2]
        )

    def test_order(self):
        self.assertListEqual(
            Query([1, 2, 4, 3, 7, 6, 5]).order(descending=True).toList(),
            [7, 6, 5, 4, 3, 2, 1]
        )

        self.assertListEqual(
            Query([1, 2, 4, 3, 7, 6, 5]).order().toList(),
            [1, 2, 3, 4, 5, 6, 7]
        )

        self.assertListEqual(
            Query([1, 2, 4, 3, 7, 6, 5]).order(key=lambda x: x % 3).toList(),
            [3, 6, 1, 4, 7, 2, 5]
        )

    def test_union(self):
        self.assertListEqual(
            Query([1, 2, 3]).union([3, 4, 5]).toList(),
            [1, 2, 3, 4, 5]
        )

        self.assertListEqual(
            Query([1, 2, 3]).union([3, 4, 5], key = lambda x: x % 4).toList(),
            [1, 2, 3, 4] # Note 5 == 2 in modulo 4
        )

        self.assertListEqual(
            Query([1, 2, 3]).union([3, 4, 5]).select(lambda x: x+1).toList(),
            [2, 3, 4, 5, 6]
        )

    def test_wrapper(self):
        with self.assertRaises(ValueError):
            Query(1)

        Query("a")
        Query([1,2,3])

        self.assertTrue(True)

    def test_skip(self):
        self.assertListEqual(
            Query([1,2,3,4,5,6,7]).skip(3).toList(),
            [4,5,6,7]
        )

    def test_skipWhile(self):
        self.assertListEqual(
            Query([1,2,3,4,5,6,7]).skipWhile(lambda x: x < 3).toList(),
            [3,4,5,6,7]
        )

        self.assertListEqual(
            Query([1,2,3,4,5,6,7]).skipWhile(lambda x: x % 3 != 0).toList(),
            [3,4,5,6,7]
        )

    def test_toDict(self):
        self.assertDictEqual(
            Query([1,2,3,4]).toDict(lambda x: str(x*x)),
            {
                '1': 1,
                '4': 2,
                '9': 3,
                '16': 4
            }
        )

        self.assertDictEqual(
            Query([1,2,3,4]).toDict(lambda x: str(x), transform = lambda x: x*x),
            {
                '1': 1,
                '2': 4,
                '3': 9,
                '4': 16
            }
        )

        with self.assertRaises(KeyError):
            Query([1,2,3,4]).toDict(lambda x: str(x % 3))