import pytest
from linq import DistributedQuery, errors


def square(x):
    return x * x


def add_1(x):
    return x + 1


def negative_square(x):
    return -x * x


def smaller_than_10(x):
    return x < 10


def greater_than_0(x):
    return x > 0


def test_distributed_query_single_process():
    assert DistributedQuery(range(100), processes=1).select(square).max() == 99 ** 2


def test_distributed_query_multiple_processes():
    assert DistributedQuery(range(100), processes=2).select(square).min() == 0


def test_chunk_size():
    assert (
        DistributedQuery(range(100), processes=2, chunk_size=23).select(square).count()
        == 100
    )


def test_long_query():
    assert (
        DistributedQuery(range(100), processes=1)
        .select(square)
        .where(smaller_than_10)
        .select(square)
        .where(greater_than_0)
        .count()
        == 3
    )


def test_all_1():
    assert DistributedQuery(range(100), processes=1).select(add_1).all(greater_than_0)


def test_all_2():
    assert not DistributedQuery(range(100), processes=1).all(smaller_than_10)


def test_any_1():
    assert DistributedQuery(range(100), processes=1).select(square).any(greater_than_0)


def test_any_2():
    assert (
        not DistributedQuery(range(10, 100), processes=1)
        .select(add_1)
        .any(smaller_than_10)
    )


def test_count():
    assert DistributedQuery(range(100), processes=1).count() == 100


def test_where():
    assert (
        DistributedQuery(range(100), processes=1).where(smaller_than_10).count() == 10
    )


def test_contains_1():
    assert DistributedQuery(range(100), processes=1).contains(50)


def test_contains_2():
    assert not DistributedQuery(range(100), processes=1).contains(-1)


def test_contains_3():
    assert 50 in DistributedQuery(range(100), processes=1)


def test_contains_4():
    assert -1 not in DistributedQuery(range(100), processes=1)


def test_flatten():
    y = (
        DistributedQuery([[1, 2, 3], [4, 5, 6], [7, 8, 9]], processes=1)
        .flatten()
        .to_list()
    )
    for x in range(1, 10):
        assert x in y


def test_argmax():
    assert DistributedQuery(range(-4, 5)).argmax(negative_square) == 0


def test_argmin():
    assert DistributedQuery(range(-4, 5)).argmin(square) == 0


def test_take_one_and_close():
    q = DistributedQuery(range(100), processes=4)
    iterator = iter(q)
    next(iterator)
    q.close()


def test_context_manager():
    with DistributedQuery(range(100), processes=1) as q:
        next(iter(q))


def test_first():
    assert DistributedQuery(range(100), processes=1).first(greater_than_0) > 0
    with pytest.raises(errors.NoSuchElementError):
        DistributedQuery(range(100), processes=1).select(negative_square).first(
            greater_than_0
        )


def test_first_or_none():
    assert DistributedQuery(range(100), processes=1).first_or_none(greater_than_0) > 0

    assert (
        DistributedQuery(range(100), processes=1)
        .select(negative_square)
        .first_or_none(greater_than_0)
        is None
    )
