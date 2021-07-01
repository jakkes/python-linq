from __future__ import annotations
from typing import (
    Iterable,
    TypeVar,
    Any,
    List,
    Callable,
    Optional,
    NoReturn,
    Dict,
    Iterator,
)
import collections.abc


import linq


T = TypeVar("T")
S = TypeVar("S")
KT = TypeVar("KT")
VT = TypeVar("VT")
U = TypeVar("U")
V = TypeVar("V")


class Query(Iterable[T]):
    """The most basic query."""

    def __init__(self, iterable: Iterable[T]):
        """
        Args:
            iterable (Iterable[T]): An iterable collection of objects of type `T`

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
        """Determines if the sequence contains the given object.

        Args:
            obj (T): Object to look for

        Returns:
            bool: `True` if the object is found, otherwise `False`.
        """
        return obj in self

    def __iter__(self) -> Iterator[T]:
        for obj in self._iterable:
            yield obj

        for extension in self._extensions:
            for obj in extension:
                yield obj

    def count(self, condition: Callable[[T], bool] = lambda x: True) -> int:
        """Counts the objects satisfying the condition

        Args:
            condition (Callable[[T], bool], optional): Expression returning `True` or
                `False`. Defaults to counting all objects.

        Returns:
            int: The number of objects found satisfying the condition
        """

        return sum(1 for x in self if condition(x))

    def any(self, condition: Callable[[T], bool]) -> bool:
        """Checks whether the sequence contains any object fulfilling the condition

        Args:
            condition (Callable[[T], bool]): Expression returning `True` or `False`.

        Returns:
            bool: `True` if any satisfactory object is found, otherwise `False`
        """

        return any(condition(x) for x in self)

    def all(self, condition: Callable[[T], bool]) -> bool:
        """Checks whether all objects satisfy a given condition

        Args:
            condition (Callable[[T], bool]): Expression returning `True` or `False`.

        Returns:
            bool: `True` if all objects are found to satisfy the condition, otherwise
                `False`
        """

        return all(condition(x) for x in self)

    def select(self, transform: Callable[[T], S]) -> Query[S]:
        """Transforms each object in the sequence.

        Args:
            transform (Callable[[T], S]): Function describing the transformation

        Returns:
            Query: Returns a new query builder based on the transformed objects.
        """
        return Query(transform(x) for x in self)

    def flatten(self) -> Query[T]:
        """Selects objects from all underlying lists into one sequence, i.e. a
        flattening operation. Useful when the collection is composed of multiple
        subcollections.

        Returns:
            Query: Returns a new query builder based on the flattened query.
        """

        return Query(x for y in self for x in y)

    def where(self, condition: Callable[[T], bool]) -> Query[T]:
        """Filters the sequence for the given condition

        Args:
            condition (Callable[[T], bool]): Expression returning `True` or `False`
                with a single input.

        Returns:
            Query: Returns a new query builder based on the filtered objects.
        """

        return Query(x for x in self if condition(x))

    def max(self) -> T:
        """Returns the maximum value found

        Returns:
            T: Returns the maximum value
        """
        return max(self)

    def argmax(self, value: Callable[[T], Any]) -> T:
        """Return the object that maximizes the given value function. NOTE: does not
        return the index of the object.

        Args:
            value (Callable[[T], Any]): Expression determining which value to use

        Returns:
            T: Returns the object which maximizes the value function
        """
        m = None
        vm = None
        for x in self:
            vx = value(x)
            if m is None or vx > vm:
                m = x
                vm = vx
        if m is None:
            raise ValueError("Cannot find the maximum of an empty sequence")
        return m

    def min(self) -> T:
        """Returns the minimum value found

        Returns:
            T: Returns the maximum value
        """

        return min(self)

    def argmin(self, value: Callable[[T], Any]) -> T:
        """Return the object that minimizes the value given by value.

        Args:
            value (Callable[[T], Any]): Expression determining which value to use

        Returns:
            T: Returns the object which minimizes the value
        """
        m = None
        for x in self:
            if m is None or value(x) < value(m):
                m = x
        if m is None:
            raise ValueError("Cannot find a minimum in an empty sequence")
        return m

    def first(self, condition: Callable[[T], bool] = lambda x: True) -> T:
        """Returns the first element found to satisfy the given condition

        Args:
            condition (Callable[[T], bool], optional): Expression returning `True` or
            `False`. By default, returns the first element in the sequence.

        Raises:
            linq.errors.NoSuchElementError: If no element is found to satisfy the
                condition

        Returns:
            T: The first element found to satisfy the given condition
        """

        for x in self:
            if condition(x):
                return x

        raise linq.errors.NoSuchElementError()

    def first_or_none(
        self, condition: Callable[[T], bool] = lambda x: True
    ) -> Optional[T]:
        """Returns the first element found to satisfy the given condition, or `None` if
        no such element was found.

        Args:
            condition (Callable[[T], bool], optional): Expression returning `True` or
            `False`. Defaults to returning `True` for any input.

        Returns:
            Optional[T]: The first element found to satisfy the given condition. If no
                element is found, then `None` is returned.
        """

        for x in self:
            if condition(x):
                return x
        return None

    def last_or_none(
        self, condition: Callable[[T], bool] = lambda x: True
    ) -> Optional[T]:
        """Returns the last element found to satisfy the given condition, or `None` if
        no such element was found.

        Args:
            condition (Callable[[T], bool], optional): Expression returning `True` or
                `False`. Defaults to returning `True` for any input.

        Returns:
            Optional[T]: The last element found to satisfy the given condition. If no
                element is found, then `None` is returned.
        """
        last = None
        for x in self:
            if condition(x):
                last = x
        return last

    def last(self, condition: Callable[[T], bool] = lambda x: True) -> T:
        """Returns the last element found to satisfy the given condition

        Args:
            condition (Callable[[T], bool], bool): Expression returning `True` or
                `False`. Defaults to returning `True` for any input.

        Raises:
            linq.errors.NoSuchElementError: If no element is found to satisfy the
                condition

        Returns:
            T: The last element found to satisfy the given condition
        """

        last = self.last_or_none(condition)

        if last is None:
            raise linq.errors.NoSuchElementError()
        else:
            return last

    def sum(self) -> T:
        """Returns the sum over all elements

        Returns:
            T: The sum over all elements
        """
        return sum(self)

    def mean(self) -> T:
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

    def distinct(self, key: Callable[[T], Any] = lambda x: x) -> Query[T]:
        """Filters all objects that are unique in the given key function, i.e. having
        unique return values.

        Args:
            key (Callable[[T], Any], optional): Expression determining the value to use
                for comparisons, must be hashable. By default, elements are compared as
                is, i.e. `lambda x: x`.

        Returns:
            Query: Query builder with only distinct elements, as defined by the `key`
                callable.
        """

        cache = set()

        def sequence():
            for x in self:
                if key(x) in cache:
                    continue
                else:
                    cache.add(key(x))
                    yield x

        return Query(sequence())

    def element_at_or_none(self, i: int) -> Optional[T]:
        """Returns the element at the given position. If there is no element at the
        given position, then `None` is returned.

        Args:
            i (int): The position at which to retrieve the element from

        Returns:
            Optional[T]: The object at the given position. `None` if there is no such
                element.
        """

        n = 0
        for o in self:
            if n == i:
                return o
            n += 1
        return None

    def element_at(self, i: int) -> T:
        """Returns the element at the given position.

        Args:
            i (int): The position at which to retrieve the element from

        Raises:
            IndexError: If there is no object at the given position

        Returns:
            T: The element at the given position
        """

        result = self.element_at_or_none(i)
        if result is None:
            raise IndexError()
        else:
            return result

    def intersect(
        self, iterable: Iterable[T], key: Callable[[T], Any] = lambda x: x
    ) -> Query[T]:
        """Returns all elements found in both sequences.

        Args:
            iterable (Iterable): The other iterable to compare to.
            key (Callable[[T], Any], optional): Expression determining value to use for
                comparison, must be hashable. Defaults to `lambda x: x`.

        Raises:
            ValueError: If the given iterable is not Iterable

        Returns:
            Query: Query builder on the intersection of self and the given iterable.
        """

        if not isinstance(iterable, collections.abc.Iterable):
            raise ValueError("Object is not iterable")

        def sequence():
            for x in self:
                kx = key(x)
                if Query(iterable).any(lambda y: kx == key(y)):
                    yield x

        return Query(sequence())

    def to_list(self) -> List[T]:
        """Returns the sequence as a list.

        Returns:
            List: A list containing all elements in the sequence.
        """
        return list(self)

    def join(
        self,
        extension: Iterable[S],
        innerKey: Callable[[T], Any],
        outerKey: Callable[[S], Any],
        transform: Callable[[T, S], U],
    ) -> Query[U]:
        """Joins the sequence of objects with another sequence of objects on the given
        keys and yields a new sequence of objects according to the transform specified.
        Equivalent to INNER JOIN in SQL.

        Args:
            extension (Iterable): The sequence to join into the query.
            innerKey (Callable[[T], Any]): Expression determining which key to join on
                in the query.
            outerKey (Callable[[S], Any]): Expression determining which key to join on
                in the extension.
            transform (Callable[[T, S], U]): Transform, taking two arguments, the inner
                and outer elements to join respectively, returning the joined object.

        Raises:
            ValueError: If the extension is not Iterable

        Returns:
            Query: Query build object wrapping the new sequence of objects.
        """

        if not isinstance(extension, collections.abc.Iterable):
            raise ValueError("Object is not iterable")

        def sequence():
            for x in self:
                outerObjs = Query(extension).where(lambda y: innerKey(x) == outerKey(y))
                for outerObj in outerObjs:
                    yield transform(x, outerObj)

        return Query(sequence())

    def take(self, count: int) -> Query[T]:
        """Selects the first `n` elements from the query.

        Args:
            count: The number of elements to select.

        Returns:
            Query: Query builder object wrapping the selected elements.
        """

        def sequence():
            for n, x in enumerate(self):
                if n >= count:
                    break
                yield x

        return Query(sequence())

    def take_while(self, condition: Callable[[T], bool]) -> Query[T]:
        """Selects elements as long as the condition is fulfilled.

        Args:
            condition (Callable[[T], bool]): Expression returning `True` or `False`.

        Returns:
            Query: Query builder object wrapping the selected elements.
        """

        def sequence():
            for x in self:
                if condition(x):
                    yield x
                else:
                    break

        return Query(sequence())

    def order(
        self, value: Callable[[T], Any] = lambda x: x, descending=False
    ) -> Query[T]:
        """Orders the sequence with respect to the given key

        Args:
            value (Callable[[T], Any], optional): Expression determining which value to
                sort on. Defaults to `lambda x: x`.
            descending (bool, optional): Whether or not to sort in descending order.
                Defaults to `False`.

        Returns:
            Query: Query builder object wrapping the sorted sequence
        """

        def sequence():
            yield from sorted(self, key=value, reverse=descending)

        return Query(sequence())

    def skip(self, count: int) -> Query[T]:
        """Skips the first elements in the sequence.

        Args:
            count (int): The number of elements to skip.

        Returns:
            Query: Query builder wrapping the remaining elements.
        """

        def sequence():
            i = 0
            for obj in self:
                if i < count:
                    i += 1
                    continue

                yield obj

        return Query(sequence())

    def skip_while(self, condition: Callable[[T], bool]) -> Query[T]:
        """Skips the first elements in the sequence while the condition is fulfilled.

        Args:
            condition (Callable[[T], bool]): Callable, elements are skipped as long as
                `True` is returned.

        Returns:
            Query: The remaining elements wrapped in a query builder object.
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

        return Query(sequence())

    def to_dict(
        self, key: Callable[[T], KT], value: Callable[[T], VT] = lambda x: x
    ) -> Dict[KT, VT]:
        """Returns the sequence as a dictionary where the key is given by `key`.

        Args:
            key (Callable[[T], KT]): Expression determining the key for each element.
                Must evaluate to a unique value for each element.
            value (Callable[[T], VT], optional): Expression describing the value of the
                elements before added to the dictionary. Defaults to `lambda x: x`.

        Returns:
            Dict[KT, VT]: A dictionary where the keys are giving by `key` and elements
                by `value`.

        """

        re = {}
        keys = set()
        for el in self:
            k_ey = key(el)
            if k_ey in keys:
                raise KeyError("Key already exists.")
            keys.add(k_ey)
            re[k_ey] = value(el)

        return re

    def union(
        self, outer: Iterable[T], value: Callable[[T], Any] = lambda x: x
    ) -> Query[T]:
        """Finds the union with another sequence, i.e. all objects that are within
        either one the two sequences. Only unique objects (with respect to the `value`)
        are returned.

        Args:
            outer (Iterable): The other sequence
            value (Callable[[T], Any]): Expression determining which value to use for
                comparison, must be hashable. Defaults to `lambda x: x`.

        Raises:
            ValueError: If `outer` is not of instance Iterable

        Returns:
            Query: Query builder object wrapping the new elements
        """

        if not isinstance(outer, collections.abc.Iterable):
            raise ValueError("Object is not iterable")

        cache = set()

        def sequence():
            for x in self:
                if value(x) in cache:
                    continue
                else:
                    cache.add(value(x))
                    yield x

            for x in outer:
                if value(x) in cache:
                    continue
                else:
                    cache.add(value(x))
                    yield x

        return Query(sequence())
