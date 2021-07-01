from typing import Iterable, Any as _Any
import abc


class Base(abc.ABC):

    @abc.abstractmethod
    def aggregate(self, data: Iterable[_Any]) -> _Any:
        raise NotImplementedError


class All(Base):
    def aggregate(self, data: Iterable[_Any]) -> _Any:
        return all(data)


class Any(Base):
    def aggregate(self, data: Iterable[_Any]) -> _Any:
        return any(data)


class ArgMax(Base):
    def __init__(self, value_fn, invert_value=False):
        super().__init__()
        self.value_fn = value_fn
        self.invert_value = invert_value

    def aggregate(self, data: Iterable[_Any]) -> _Any:
        max_value = None
        max_arg = None
        for x in data:
            if max_value is None:
                max_value = self.value_fn(x)
                max_arg = x
                continue

            value = self.value_fn(x)
            if (value > max_value and not self.invert_value) or (value < max_value and self.invert_value):
                max_value = value
                max_arg = x
        return max_arg


class Contains(Base):
    def __init__(self, obj):
        super().__init__()
        self.obj = obj

    def aggregate(self, data: Iterable[_Any]) -> _Any:
        return self.obj in data


class Count(Base):
    def aggregate(self, data: Iterable[_Any]) -> _Any:
        return sum(1 for _ in data)


class FirstOrNone(Base):
    def __init__(self, condition_fn):
        super().__init__()
        self.condition_fn = condition_fn

    def aggregate(self, data: Iterable[_Any]) -> _Any:
        for x in data:
            if self.condition_fn(x):
                return x
        return None


class LastOrNone(Base):
    def __init__(self, condition_fn):
        super().__init__()
        self.condition_fn = condition_fn

    def aggregate(self, data: Iterable[_Any]) -> _Any:
        re = None
        for x in data:
            if self.condition_fn(x):
                re = x
        return re


class List(Base):
    def aggregate(self, data: Iterable[_Any]) -> _Any:
        return list(data)


class Max(Base):
    def aggregate(self, data: Iterable[_Any]) -> _Any:
        return max(data)


class Min(Base):
    def aggregate(self, data: Iterable[_Any]) -> _Any:
        return min(data)


class Sum(Base):
    def aggregate(self, data: Iterable[_Any]) -> _Any:
        return sum(data)


class SumAndCount(Base):
    def aggregate(self, data: Iterable[_Any]) -> _Any:
        s = 0; c = 0
        for x in data:
            s += x
            c += 1
        return (s, c)

class Dict(Base):
    def __init__(self, key, value):
        super().__init__()
        self.key = key
        self.value = value

    def aggregate(self, data: Iterable[_Any]) -> _Any:
        return {self.key(x): self.value(x) for x in data}
