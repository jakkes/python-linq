from linq import DistributedQuery


def square(x):
    return x*x


def test_distributed_query():
    assert DistributedQuery(range(100), processes=1).select(square).max() == 99**2


def test_distributed_query2():
    assert DistributedQuery(range(100), processes=4).select(square).min() == 0
