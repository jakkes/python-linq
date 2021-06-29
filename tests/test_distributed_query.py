from linq import DistributedQuery


def square(x):
    return x*x


def test_distributed_query():
    assert DistributedQuery(range(100), processes=1).select(square).max() == 99**2
