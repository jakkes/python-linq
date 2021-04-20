from __future__ import annotations
import collections.abc
from typing import Iterable, TypeVar, Any, List, Callable, Optional, Generic, NoReturn, Dict
from ._linq_exceptions import NoSuchElementError


T = TypeVar("T")
S = TypeVar("S")
U = TypeVar("U")
V = TypeVar("V")
KT = TypeVar("KT")
VT = TypeVar("VT")


class From(Iterable[T]):
    """Query builder."""

    def __init__(self, iterable: Iterable[T]):
        """
        Arguments:
            iterable (Iterable): An iterable collection of objects of type T

        Raises:
            ValueError: If `iterable` is not an iterable collection
        """
        if not isinstance(iterable, collections.abc.Iterable):
            raise ValueError("Object is not iterable")

        self._iterable: Iterable[T] = iterable
        self._extensions: List[Iterable[T]] = []

    def __contains__(self, obj: T) -> bool:
        for o in self:
            if o == obj:
                return True
        return False

    def contains(self, obj: T) -> bool:
        """Determines if the sequence contains the given object

        Arguments:
            obj (T): The object to look for

        Returns:
            bool: True if the object is found, otherwise `False`.
        """
        return obj in self

    def __iter__(self) -> T:
        for obj in self._iterable:
            yield obj

        for extension in self._extensions:
            for obj in extension:
                yield obj

    def count(self, condition: Callable[[T], bool] = lambda x: True) -> int:
        """Counts the objects satisfying the condition

        Keyword Arguments:
            condition (Callable[[T], bool]): Expression returning True or False. (default: counts all objects)

        Returns:
            int: The number of objects found satisfying the condition
        """

        return sum(1 for x in self if condition(x))

    def any(self, condition: Callable[[T], bool]) -> bool:
        """Checks whether the sequence contains any object fulfilling the condition

        Arguments:
            condition (Callable[[T], bool]): Expression returning True or False.

        Returns:
            bool: True if any satisfactory object is found, otherwise False
        """

        return any(condition(x) for x in self)

    def all(self, condition: Callable[[T], bool]) -> bool:
        """Checks whether all objects satisfy a given condition

        Arguments:
            condition (Callable[[T], bool]): Expression returning True or False.

        Returns:
            bool: True if all objects are found to satisfy the condition, otherwise False
        """

        return all(condition(x) for x in self)

    def select(self, transform: Callable[[T], S]) -> From[S]:
        """Transforms each object in the sequence.

        Arguments:
            transform (Callable[[T], S]): Function describing the transformation

        Returns:
            From: Returns a new query builder based on the transformed object.
        """
        return From(transform(x) for x in self)

    def selectMany(self, transform: Callable[[T], S] = lambda x: x) -> From[S]:
        """Selects objects, with the possibility of transforming them, from all underlying lists into
        one sequence. Useful when the collection is composed of multiple subcollections. 

        Keyword Arguments:
            transform: Expression describing the transformation. (default: no transform is applied and the underlying objects are selected as is)

        Returns:
            From: Returns a new query builder based on the transformed object.
        """

        return From(transform(x) for y in self for x in y)

    def where(self, condition: Callable[[T], bool]) -> From[T]:
        """Filters the sequence for the given condition

        Arguments:
            condition (Callable[[T], bool]): Expression returning True or False with a single input.

        Returns:
            From: Returns a new query builder based on the filtered objects.
        """

        return From(x for x in self if condition(x))

    def max(self) -> T:
        """Returns the maximum value found

        Returns:
            T: Returns the maximum value
        """
        return max(self)

    def argmax(self, key: Callable[[T], Any]) -> T:
        """Return the object that maximizes the value given by key. NOTE: does not return the index of the object.

        Arguments:
            key (Callable[[T], Any]): Expression determining which value to use

        Returns:
            T: Returns the object which maximizes the value
        """
        m = None
        vm = None
        for x in self:
            vx = key(x)
            if m is None or vx > vm:
                m = x
                vm = vx
        if m is None:
            raise ValueError("Cannot find maximum of an empty sequence")
        return m

    def min(self) -> T:
        """Returns the minimum value found

        Returns:
            T: Returns the maximum value
        """

        return min(self)

    def argmin(self, key: Callable[[T], Any]) -> T:
        """Return the object that minimizes the value given by key.

        Arguments:
            key (Callable[[T], Any]): Expression determining which value to use

        Returns:
            T: Returns the object which minimizes the value
        """
        m = None
        for x in self:
            if m is None or key(x) < key(m):
                m = x
        if m is None:
            raise ValueError("Cannot find maximum in an empty sequence")
        return m

    def first(self, condition: Callable[[T], bool] = lambda x: True) -> T:
        """Returns the first element found to satisfy the given condition

        Keyword Arguments:
            condition (Callable[[T], bool]): Expression returning True or False (default: Returns the first element in the sequence)

        Raises:
            NoSuchElementError: If no element is found to satisfy the condition

        Returns:
            T: The first element found to satisfy the given condition
        """

        for x in self:
            if condition(x):
                return x

        raise NoSuchElementError()

    def firstOrNone(self, condition: Callable[[T], bool] = lambda x: True) -> Optional[T]:
        """Returns the first element found to satisfy the given condition

        Keyword Arguments:
            condition (Callable[[T], bool]): Expression returning True or False (default: (lambda x: True))

        Returns:
            Optional[T]: The first element found to satisfy the given condition. If no element is found, None is returned.
        """

        for x in self:
            if condition(x):
                return x
        return None

    def lastOrNone(self, condition: Callable[[T], bool] = lambda x: True) -> Optional[T]:
        """Returns the last element found to satisfy the given condition

        Keyword Arguments:
            condition (Callable[[T], bool]): Expression returning True or False (default: (lambdax:True))

        Returns:
            Optional[T]: The last element found to satisfy the given condition. If no element is found, None is returned.
        """
        last = None
        for x in self:
            if condition(x):
                last = x
        return last

    def last(self, condition: Callable[[T], bool] = lambda x: True) -> T:
        """Returns the last element found to satisfy the given condition

        Keyword Arguments:
            condition (Callable[[T], bool]): Expression returning True or False (default: Returns the first element in the sequence)

        Raises:
            NoSuchElementError: If no element is found to satisfy the condition

        Returns:
            T: The last element found to satisfy the given condition
        """

        last = self.lastOrNone(condition)

        if last is None:
            raise NoSuchElementError()
        else:
            return last

    def sum(self) -> T:
        """Returns the sum over all elements

        Returns:
            T: The sum over all elements
        """
        return sum(self)

    def average(self) -> T:
        """Returns the average of all elements

        Returns:
            T: The average of all elements
        """
        s = 0
        n = 0
        for x in self:
            s += x
            n += 1
        return s / n

    def concat(self, iterable: Iterable[T]) -> From[T]:
        """Adds an iterable to the sequence

        Arguments:
            iterable (Iterable): The collection to add

        Raises:
            ValueError: If the supplied object is not iterable

        Returns:
            From: Query builder with the extension concatenated.
        """

        if not isinstance(iterable, collections.abc.Iterable):
            raise ValueError("Object is not iterable")

        self._extensions.append(iterable)
        return self

    def distinct(self, key: Callable[[T], Any] = lambda x: x) -> From[T]:
        """Filters all objects that are unique in the given key function, i.e. having unique return values.

        Keyword Arguments:
            key (Callable[[T], Any]): Expression determining which key to use. The key must be hashable (default: Uses the elements as is)

        Returns:
            From: Query builder with only distinct elements.
        """

        cache = set()

        def sequence():
            for x in self:
                if key(x) in cache:
                    continue
                else:
                    cache.add(key(x))
                    yield x

        return From(sequence())

    def elementAtOrNone(self, i: int) -> Optional[T]:
        """Returns the element at the given position. If there is no element at the given position, `None` is returned.

        Arguments:
            i (int): The position at which to retrieve the element from

        Returns:
            Optional[T]: The object at the given position. `None` if there is none.
        """

        n = 0
        for o in self:
            if n == i:
                return o
            n += 1
        return None

    def elementAt(self, i: int) -> T:
        """Returns the element at the given position.

        Arguments:
            i (int): The position at which to retrieve the element from

        Raises:
            IndexError: If there is no object at the given position

        Returns:
            T: The element at the given position
        """

        result = self.elementAtOrNone(i)
        if result is None:
            raise IndexError()
        else:
            return result

    def intersect(self, iterable: Iterable[T], key: Callable[[T], Any] = lambda x: x) -> From[T]:
        """Returns all elements found in both sequences.

        Arguments:
            iterable (Iterable): The other iterable to compare to.

        Keyword Arguments:
            key (Callable[[T], Any]): Expression determining which key to use. Key must be hashable. (default: The elements are used as is)

        Raises:
            ValueError: If the given iterable is not Iterable

        Returns:
            From: Query builder on the intersection of self and the given iterable.
        """

        if not isinstance(iterable, collections.abc.Iterable):
            raise ValueError("Object is not iterable")

        def sequence():
            for x in self:
                kx = key(x)
                if From(iterable).any(lambda y: kx == key(y)):
                    yield x

        return From(sequence())

    def toList(self) -> List[T]:
        """Returns the sequence as a list.

        Returns:
            List: A list containing all elements in the sequence.
        """
        return list(self)

    def groupBy(self, key: Callable[[T], KT], transform: Callable[[T], VT] = lambda x: x) -> From[Grouping[KT, VT]]:
        """Groups all elements based on the given key.

        Arguments:
            key (Callable[[T], KT]): Expression determining which key to use

        Keyword Arguments:
            transform (Callable[[T], VT]): Expression describing the transform the objects when creating the groups.
            Can be any lambda expression or function with a single input argument (default: Use the elements as is)

        Returns:
            From[Grouping[KT, VT]]: Query builder object wrapping a sequence of `Grouping` objects.
            Every `Grouping` object has two attributes, `key`, and `values` which contains the
            transformed objects.
        """

        def sequence():
            groups = dict()
            for x in self:
                k = key(x)
                if k in groups:
                    groups[k].append(transform(x))
                else:
                    groups[k] = [transform(x)]

            for k in groups:
                yield Grouping(k, groups[k])

        return From(sequence())

    def forEach(self, func: Callable[[T], NoReturn]) -> NoReturn:
        """Executes a function for each element.
        """

        for x in self:
            func(x)

    def groupJoin(self, extension: Iterable[S], innerKey: Callable[[T], Any], outerKey: Callable[[S], Any], innerTransform: Callable[[T], U], outerTransform: Callable[[S], V]) -> From[Joining[U, V]]:
        """Joins the sequence with objects from another sequence.

        Arguments:
            extension (Iterable[S]): The other sequence
            innerKey (Callable[[T], Any]): Expression determining what key to use from the inner objects
            outerKey (Callable[[S], Any]): Expression determining what key to use from the outer objects
            innerTransform (Callable[[T], U]): The transform to apply to the inner objects
            outerTransform (Callable[[S], V]): The transform to apply to the outer objects

        Returns:
            From[Joining[U, V]]: Query builder object wrapping a sequence of `Joining` objects. Each `Joining` object contains
            the properties `inner` and `outer`. `inner` gives the inner object and `outer` is a collection of all objects in the
            extension that were paried with the inner object.
        """

        def sequence():
            for innerObj in self:
                outerObjs = (
                    From(extension)
                    .where(lambda x: innerKey(innerObj) == outerKey(x))
                    .select(outerTransform)
                    .toList()
                )
                yield Joining(
                    innerTransform(innerObj),
                    outerObjs
                )

        return From(sequence())

    def join(self, extension: Iterable[S], innerKey: Callable[[T], Any], outerKey: Callable[[S], Any], transform: Callable[[T, S], U]) -> From[U]:
        """Joins the sequence of objects with another sequence of objects on the given keys and yields a
        a new sequence of objects according to the transform specified. Equivalent to INNER JOIN in SQL.

        Arguments:
            extension (Iterable): The sequence to join into the current one
            innerKey (Callable[[T], Any]): Expression determining which key to use on the current sequence
            outerKey (Callable[[S], Any]): Expression determining which key to use on the extending sequence
            transform (Callable[[T, S], U]): Expression shaping the objects which to returns.

        Raises:
            ValueError: If the extension is not Iterable

        Returns:
            From: Query build object wrapping the new sequence of objects.
        """

        if not isinstance(extension, collections.abc.Iterable):
            raise ValueError("Object is not iterable")

        def sequence():
            for x in self:
                outerObjs = From(extension).where(
                    lambda y: innerKey(x) == outerKey(y))
                for outerObj in outerObjs:
                    yield transform(x, outerObj)

        return From(sequence())

    def take(self, count: int) -> From[T]:
        """Selects the amount of elements specified

        Arguments:
            count: The number of elements to select

        Returns:
            From: Query builder object wrapping the selected elements
        """

        def sequence():
            n = 0
            for x in self:

                if n >= count:
                    break

                yield x
                n += 1

        return From(sequence())

    def takeWhile(self, condition: Callable[[T], bool]) -> From[T]:
        """Selects elements as long as the condition is fulfilled

        Arguments:
            condition (Callable[[T], bool]): Expression returning True or False

        Returns:
            From: Query builder object wrapping the selected elements
        """

        def sequence():
            for x in self:
                if condition(x):
                    yield x
                else:
                    break

        return From(sequence())

    def order(self, key: Callable[[T], Any] = lambda x: x, descending=False) -> From[T]:
        """Orders the sequence with respect to the given key

        Keyword Arguments:
            key (Callable[[T], Any]): Expression determining which key to use (default: uses the elements as is)
            descending (bool): Whether or not to sort in descending order (default: (False))

        Returns:
            From: Query builder object wrapping the sorted sequence
        """

        def sequence():
            yield from sorted(self, key=key, reverse=descending)

        return From(sequence())

    def skip(self, count: int) -> From[T]:
        """Skips the first elements in the sequence

        Arguments:
            count (int): The number of elements to skip

        Returns:
            From: Query builder wrapping the remaining elements.
        """

        def sequence():
            i = 0
            for obj in self:
                if i < count:
                    i += 1
                    continue

                yield obj

        return From(sequence())

    def skipWhile(self, condition: Callable[[T], bool]) -> From[T]:
        """Skips the first elements in the sequence while the condition evaluates `True`

        Arguments:
            condition (Callable[[T], bool]): The number of elements to skip

        Returns:
            From: The remaining elements wrapped in a query builder object.
        """
        def sequence():
            skipping = True
            for obj in self:
                if skipping:
                    if condition(obj):
                        continue
                    else:
                        skipping = False
                yield obj

        return From(sequence())

    def toDict(self, key: Callable[[T], KT], transform: Callable[[T], VT]=lambda x: x) -> Dict[KT, VT]:
        """Returns the sequence as a dictionary where the key is given by `key`.

        Arguments:
            key (Callable[[T], KT]): Expression determining the key for each element. Much evaluate to a unique value for each element.

        Keyword Arguments:
            transform (Callable[[T], VT]): Expression describing the transform of the elements before added to the dictionary

        Returns:
            Dict[KT, VT]: A dictionary where the keys are giving by `key` and elements by `transform`.

        """

        re = {}
        keys = set()
        for el in self:
            k_ey = key(el)
            if k_ey in keys:
                raise KeyError("Key already exists.")
            keys.add(k_ey)
            re[k_ey] = transform(el)

        return re

    def union(self, outer: Iterable[T], key: Callable[[T], Any]=lambda x: x) -> From[T]:
        """Find the union of two sequences, i.e. all objects that are within either one the two sequences.
        Only unique objects (with respect to the key) are returned.

        Arguments:
            outer (Iterable): The other sequence

        Keyword Arguments:
            key (Callable[[T], Any]): Expression determining which key to use for comparison. Key must be hashable (default: uses the elements as is)

        Raises:
            ValueError: If `outer` is of instance Iterable

        Returns:
            From: Query builder object wrapping the new elements
        """

        if not isinstance(outer, collections.abc.Iterable):
            raise ValueError("Object is not iterable")

        cache = set()

        def sequence():
            for x in self:
                if key(x) in cache:
                    continue
                else:
                    cache.add(key(x))
                    yield x

            for x in outer:
                if key(x) in cache:
                    continue
                else:
                    cache.add(key(x))
                    yield x

        return From(sequence())


class Grouping(Generic[KT, VT]):
    def __init__(self, key: KT, values: List[VT]):
        self._values = values
        self._key = key

    @property
    def values(self) -> List[VT]:
        return self._values

    @property
    def key(self) -> KT:
        return self._key

    def __iter__(self):
        yield from self._values

    def __repr__(self):
        return {
            self._key: self._values
        }.__repr__()


class Joining(Generic[T, S]):
    def __init__(self, inner: T, outer: Iterable[S]):
        self._inner = inner
        self._outer = outer

    @property
    def inner(self) -> T:
        return self._inner

    @property
    def outer(self) -> List[S]:
        return self._outer

    def __iter__(self):
        yield from self._outer

    def __repr__(self):
        return {
            "inner": self._inner,
            "outer": self._outer
        }.__repr__()
