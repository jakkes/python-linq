import collections
from python_linq.linq_exceptions import NoSuchElementError

class From():

    def __init__(self, iterable):
        """
        Creates a wrapper on an iterable object
        """
        
        if not isinstance(iterable, collections.Iterable):
            raise ValueError("Object is not iterable")
        
        self.iterable = iterable
        self.extensions = []

    def __contains__(self, object):
        for obj in self:
            if obj == object:
                return True
        return False

    def contains(self, object):
        """
        Returns True if the object is found within the collection
        """
        return object in self
    
    def __iter__(self):
        for obj in self.iterable:
            yield obj
        
        for extension in self.extensions:
            for obj in extension:
                yield obj

    def count(self, predicate=lambda x: True):
        """
        Counts the objects satisfying the condition
        """
        return sum(1 for x in self if predicate(x))

    def any(self, predicate):
        """
        Returns True if any object is found to satisfy the given condition
        """
        return any(predicate(x) for x in self)

    def all(self, predicate):
        """
        Returns True if all objects are found to satisfy the given condition
        """
        return all(predicate(x) for x in self)

    def select(self, predicate = lambda x: x):
        """
        Selects the objects with the possiblity of modification

        Example:

        a = [1, 2, 3]

        def shape(x):
            return {"value": x}

        coolA = From(a).select(shape(x)).to_list()

        coolA == [
            {
                "value": 1
            }, {
                "value": 2
            }, {
                "value": 3
            }
        ]

        """
        return From(predicate(x) for x in self)

    def select_many(self, predicate = lambda x: x):

        """
        Combines elements from multiple lists.

        Example:

        l = From([[1, 2], [3, 4]])  
        result = l.select_many().to_list()

        result == [1, 2, 3, 4]
        """

        return From(predicate(x) for y in self for x in y)

    def where(self, predicate):
        """
        Filters according to the supplied condition

        Example:

        l = From([2, 3, 4])  
        result = l.where(lambda x: x % 2 == 0).to_list()

        result == [2, 4]
        """
        return From(x for x in self if predicate(x))

    def max(self, predicate = lambda x: x):
        """
        Returns the maximum value found
        """
        return max(predicate(x) for x in self)

    def min(self, predicate = lambda x: x):
        """
        Returns the minimum value found
        """
        return min(predicate(x) for x in self)

    def first(self, predicate = lambda x: True):
        """
        Returns first element satisfying the condition.

        NoSuchElementError is raised if no element is found
        """
        for x in self:
            if predicate(x):
                return x

        raise NoSuchElementError()

    def first_or_none(self, predicate = lambda x: True):
        """
        Returns first element satisfying the condition. If no element is found, None is returned.
        """
        for x in self:
            if predicate(x):
                return x
        return None

    def last_or_none(self, predicate = lambda x: True):
        """
        Returns the last element in the sequence that satifies the condition. If no element is found, None is returned
        """
        last = None
        for x in self:
            if predicate(x):
                last = x
        return last

    def last(self, predicate = lambda x: True):
        """
        Returns the last element in the sequence that satifies the condition. If no element is found, NoSuchElementError is raised
        """
        last = self.last_or_none(predicate)

        if last is None:
            raise NoSuchElementError()
        else:
            return last

    def sum(self, predicate = lambda x: x):
        """
        Returns the sum of all elements defined by the predicate.
        """
        return sum(predicate(x) for x in self)

    def average(self, predicate = lambda x: x):
        """
        Returns the average value of the elements defined by the predicate
        """
        return self.sum(predicate) * 1.0 / self.count()

    def median(self, predicate = lambda x: x):
        """
        Returns the median of the elements defined by the predicate
        """
        raise NotImplementedError()

    def concat(self, iterable):
        """
        Adds the supplied iterable to the sequence
        """

        if not isinstance(iterable, collections.Iterable):
            raise ValueError("Object is not iterable")

        self.extensions.append(iterable)

    def distinct(self, predicate = lambda x: x):
        """
        Returns objects that are distinct in the given value
        """
        cache = set()

        def sequence():
            for x in self:
                if predicate(x) in cache:
                    continue
                else:
                    cache.add(predicate(x))
                    yield x

        return From(x for x in sequence())
        
    def element_at_or_none(self, i):
        """
        Returns the element at index i. If index is out of range, None is returned
        """
        n = 0
        for o in self:
            if n == i:
                return o
            n += 1
        return None

    def element_at(self, i):
        """
        Returns the element at index i. Raises IndexError if index is out of range
        """
        result = self.element_at_or_none(i)
        if result is None:
            raise IndexError()
        else:
            return result

    def intersect(self, iterable):
        
        """
        Returns the intersection of this sequence and another one. In other words, returns only the objects that have equal keys in both iterables.
        """

        if not isinstance(iterable, collections.Iterable):
            raise ValueError("Object is not iterable")
        
        def sequence():
            for x in self:
                if From(iterable).any(lambda y: x == y):
                    yield x

        return From(x for x in sequence())

    def to_list(self):
        """
        Returns the objects in a list format
        """
        return list(x for x in self)

    def group_by(self, key_func, selector_func = lambda x: x):
        """
        Groups a list of objects into lists of objects defined by selector_func grouped by key
        """
        def sequence():

            ### TODO: Rewrite this using yield

            groups = dict()
            for x in self:
                key = key_func(x)
                if key in groups:
                    groups[key].append(selector_func(x))
                else:
                    groups[key] = [selector_func(x)]

            for key in groups:
                yield Grouping(key, groups[key])

        return From(x for x in sequence())

    def group_join(self, extension, innerKey, outerKey, selector):
        
        ### TODO: Fix if outerObj is None
        
        """
        Group joins two sequences based on equality of inner and outer and forms objects according to selector

        Keyword arguments:
        extension -- the other sequence  
        innerKey -- the object to use from THIS sequence for comparison with the extension sequence  
        outerKey -- the object to use from the EXTENSION sequence for comparison with this sequence  
        selector -- the object to form based on the inner and outer objects joined. Note, the second argument in selector (outerObject) can be None if none is found 
        """
        def sequence():
            for innerObj in self:
                outerObj = From(extension).first_or_none(lambda x: innerKey(innerObj) == outerKey(x))
                yield selector(innerObj, outerObj)

        return From(x for x in sequence())

    def join(self, outer, innerKey, outerKey, result):

        ### TODO: Fix if outerObj is None

        """
        Joins two sequences on the innerKey and outerKey functions and returns whatever specified in result(innerObj, outerObj)
        """

        if not isinstance(outer, collections.Iterable):
            raise ValueError("Object is not iterable")

        def sequence():
            for x in self:
                outerObj = From(outer).first_or_none(lambda y: innerKey(x) == outerKey(y))
                yield result(x, outerObj)

        return From(x for x in sequence())

    def union(self, outer):

        """
        Returns the union of two sequences, that is all unique elements that exist in either of the two sequences
        """

        if not isinstance(outer, collections.Iterable):
            raise ValueError("Object is not iterable")

        cache = set()

        def sequence():
            for x in self:
                if x in cache:
                    continue
                else:
                    cache.add(x)
                    yield x

            for x in outer:
                if x in cache:
                    continue
                else:
                    cache.add(x)
                    yield x

        return From(x for x in sequence())

    


class Grouping:
    def __init__(self, key, values):
        self.values = values
        self.key = key

    def __iter__(self):
        yield from self.values