from linq import Query, errors
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
            Query(subject).mean(),
            3
        )

        self.assertEqual(
            Query(subject).select(lambda x: x*x).mean(),
            11
        )

        subject = [
            { "value": 1 },
            { "value": 2 },
            { "value": 3 }
        ]
        self.assertEqual(
            Query(subject).select(lambda x: x["value"]).mean(),
            2
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
            Query(subject).distinct().to_list(),
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
            Query(subject).distinct(lambda x: x["id"]).select(lambda x: x["value"]).to_list(),
            [3, 4]
        )

        expected = [1,2,3,4]
        subject = [1,1,1,1,1,1,1,1,2,3,3,3,3,3,4]

        result = Query(subject).distinct().to_list()

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

        result = Query(subject).distinct(lambda x: x["value"]).select(lambda x: x["value"]).to_list()

        self.assertListEqual(expected,result)

    def test_elementat(self):
        subject = [1, 2, 3, 4]
        self.assertEqual(
            Query(subject).element_at(2),
            3
        )

        with self.assertRaises(IndexError):
            Query(subject).element_at(4)

        subject = [
            { "value": 1 },
            { "value": 2 }
        ]
        self.assertDictEqual(
            Query(subject).element_at(0),
            { "value": 1 }
        )

    def test_elementatornone(self):
        
        subject = [1, 2, 3, 4]
        self.assertEqual(
            Query(subject).element_at_or_none(2),
            3
        )

        self.assertIsNone(Query(subject).element_at_or_none(4))

        subject = [
            { "value": 1 },
            { "value": 2 }
        ]
        self.assertDictEqual(
            Query(subject).element_at_or_none(0),
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
            Query(subject).first_or_none(lambda x: x % 2 == 0),
            2
        )

        self.assertIsNone(Query(subject).first_or_none(lambda x: x > 4))

        subject = [ 
            { "value": 1 },
            { "value": 2 }
        ]
        self.assertDictEqual(
            Query(subject).first(lambda x: x["value"] == 2),
            { "value": 2 }
        )


    def test_intersect(self):
        subject1 = [1,2,3,4]
        subject2 = [3,4,5,6]

        result = Query(subject1).intersect(subject2).to_list()
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
        result = Query(subjectA).intersect(subjectB, key=lambda x: x["id"]).select(lambda x: x["value"]).to_list()
        expected = [4]
        self.assertListEqual(expected, result)

        subjectA = [1, 2, 3, 4]
        subjectB = [3, 4, 5, 6]
        self.assertListEqual(
            Query(subjectA).intersect(subjectB).to_list(),
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
            Query(subjectA).intersect(subjectB, key=lambda x: x["id"]).select(lambda x: x["value"]).to_list(),
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
            Query(subject).last_or_none(lambda x: x % 2 == 0),
            4
        )

        self.assertIsNone(
            Query(subject).last_or_none(lambda x: x > 4)
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
            Query(subject).select(lambda x: x["value"]).to_list(),
            [2, 3]
        )

        subject = [1, 2]
        def shape(x):
            return {
                "value": x
            }
        
        self.assertListEqual(
            Query(subject).select(shape).to_list(),
            [ {"value": 1}, {"value": 2} ]
        )

    def test_flatten(self):
        expected = [1, 2, 3, 4]
        obj = Query([[1, 2], [3, 4]])

        result = obj.flatten().to_list()

        self.assertListEqual(expected, result)

        subject = [
            [1, 2, 3, 4],
            [5, 6, 7, 8]
        ]
        self.assertListEqual(
            Query(subject).flatten().to_list(),
            [1, 2, 3, 4, 5, 6, 7, 8]
        )

        subject = [
            [{"value": 1}, {"value": 2}],
            [{"value": 3}, {"value": 4}]
        ]
        self.assertListEqual(
            Query(subject).flatten().select(lambda x: x["value"]).to_list(),
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
            Query([1, 2, 3, 4]).select(lambda x: x*x).to_list(),
            [1, 4, 9, 16]
        )

        self.assertListEqual(
            Query([1, 2, 3, 4]).to_list(),
            [1, 2, 3, 4]
        )


    def test_where(self):
        expected = [2, 4]
        obj = Query(self.simple)

        result = obj.where(lambda x: x % 2 == 0).to_list()

        self.assertListEqual(expected, result)

        subject = [1, 2, 3, 4, 5, 6]
        self.assertListEqual(
            Query(subject).where(lambda x: x > 3).to_list(),
            [4, 5, 6]
        )

        subject = [
            { "value": 2 },
            { "value": 3 }
        ]
        self.assertListEqual(
            Query(subject).where(lambda x: x["value"] == 3).select(lambda x: x["value"]).to_list(),
            [3]
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
            ).to_list(),

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
            .to_list()
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
            Query([1, 2, 3]).take(2).to_list(),
            [1, 2]
        )

    def test_takewhile(self):
        self.assertListEqual(
            Query([1, 2, 3, 4, 5, 6]).take_while(lambda x: x % 3 != 0).to_list(),
            [1, 2]
        )

    def test_order(self):
        self.assertListEqual(
            Query([1, 2, 4, 3, 7, 6, 5]).order(descending=True).to_list(),
            [7, 6, 5, 4, 3, 2, 1]
        )

        self.assertListEqual(
            Query([1, 2, 4, 3, 7, 6, 5]).order().to_list(),
            [1, 2, 3, 4, 5, 6, 7]
        )

        self.assertListEqual(
            Query([1, 2, 4, 3, 7, 6, 5]).order(value=lambda x: x % 3).to_list(),
            [3, 6, 1, 4, 7, 2, 5]
        )

    def test_union(self):
        self.assertListEqual(
            Query([1, 2, 3]).union([3, 4, 5]).to_list(),
            [1, 2, 3, 4, 5]
        )

        self.assertListEqual(
            Query([1, 2, 3]).union([3, 4, 5], value = lambda x: x % 4).to_list(),
            [1, 2, 3, 4] # Note 5 == 2 in modulo 4
        )

        self.assertListEqual(
            Query([1, 2, 3]).union([3, 4, 5]).select(lambda x: x+1).to_list(),
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
            Query([1,2,3,4,5,6,7]).skip(3).to_list(),
            [4,5,6,7]
        )

    def test_skipWhile(self):
        self.assertListEqual(
            Query([1,2,3,4,5,6,7]).skip_while(lambda x: x < 3).to_list(),
            [3,4,5,6,7]
        )

        self.assertListEqual(
            Query([1,2,3,4,5,6,7]).skip_while(lambda x: x % 3 != 0).to_list(),
            [3,4,5,6,7]
        )

    def test_toDict(self):
        self.assertDictEqual(
            Query([1,2,3,4]).to_dict(lambda x: str(x*x)),
            {
                '1': 1,
                '4': 2,
                '9': 3,
                '16': 4
            }
        )

        self.assertDictEqual(
            Query([1,2,3,4]).to_dict(lambda x: str(x), value = lambda x: x*x),
            {
                '1': 1,
                '2': 4,
                '3': 9,
                '4': 16
            }
        )

        with self.assertRaises(KeyError):
            Query([1,2,3,4]).to_dict(lambda x: str(x % 3))