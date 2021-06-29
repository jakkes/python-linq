from linq import DistributedQuery


def square(x):
    return x*x

def smaller_than_10(x):
    return x < 10


def test_distributed_query_single_process():
    assert DistributedQuery(range(100), processes=1).select(square).max() == 99**2


def test_distributed_query_multiple_processes():
    assert DistributedQuery(range(100), processes=4).select(square).min() == 0


def test_count():
    assert DistributedQuery(range(100), processes=1).count() == 100


def test_where():
    assert DistributedQuery(range(100), processes=1).where(smaller_than_10).count() == 10
