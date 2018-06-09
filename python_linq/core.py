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

    def selectMany(self, predicate = lambda x: x):

        """
        Combines elements from multiple lists.

        Example:

        l = From([[1, 2], [3, 4]])  
        result = l.selectMany().to_list()

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

    def firstOrNone(self, predicate = lambda x: True):
        """
        Returns first element satisfying the condition. If no element is found, None is returned.
        """
        for x in self:
            if predicate(x):
                return x
        return None

    def lastOrNone(self, predicate = lambda x: True):
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
        last = self.lastOrNone(predicate)

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
        
    def elementAtOrNone(self, i):
        """
        Returns the element at index i. If index is out of range, None is returned
        """
        n = 0
        for o in self:
            if n == i:
                return o
            n += 1
        return None

    def elementAt(self, i):
        """
        Returns the element at index i. Raises IndexError if index is out of range
        """
        result = self.elementAtOrNone(i)
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

    def toList(self):
        """
        Returns the objects in a list format
        """
        return list(x for x in self)

    def groupBy(self, key_func, selector_func = lambda x: x):
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

    def groupJoin(self, extension, innerKey, outerKey, selector):
        
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
                outerObj = From(extension).firstOrNone(lambda x: innerKey(innerObj) == outerKey(x))
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
                outerObj = From(outer).firstOrNone(lambda y: innerKey(x) == outerKey(y))
                if outerObj is None:
                    yield result(x, NoneDict())
                else:
                    yield result(x, outerObj)

        return From(x for x in sequence())

    def take(self, i):
        """
        Returns i objects from the sequence
        """
        def sequence():
            n = 0
            for x in self:
                
                if n >= i:
                    break
                
                yield x
                n += 1

        return From(x for x in sequence())

    def takeWhile(self, predicate):
        """
        Returns objects as long as the condition is fulfilled
        """

        def sequence():
            for x in self:
                if predicate(x):
                    yield x
                else:
                    break

        return From(x for x in sequence())

    def orderBy(self, key, descending = False):
        """
        Returns an order sequence with respect to the given key
        """

        def sequence():
            yield from sorted(self, key, descending)

        return From(x for x in sequence())

    def union(self, outer, key = lambda x: x):

        """
        Returns the union of two sequences, that is all unique elements that exist in either of the two sequences
        """

        if not isinstance(outer, collections.Iterable):
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

        return From(x for x in sequence())

class Grouping:
    def __init__(self, key, values):
        self.values = values
        self.key = key

    def __iter__(self):
        yield from self.values

class NoneDict(dict):
    def __setitem__(self, key, item):
        pass

    def __getitem__(self, key):
        return None

    def __repr__(self):
        return None

    def __len__(self):
        return 0

    def __delitem__(self, key):
        pass

    def clear(self):
        pass

    def copy(self):
        return NoneDict()

    def has_key(self, k):
        return False

    def update(self, *args, **kwargs):
        return NoneDict()

    def keys(self):
        return []

    def values(self):
        return []

    def items(self):
        return []

    def pop(self, *args):
        return None

    def __contains__(self, item):
        return False

    def __iter__(self):
        yield None

    def __str__(self):
        return None