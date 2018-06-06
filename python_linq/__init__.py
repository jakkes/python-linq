import collections
from python_linq.linq_exceptions import NoSuchElementError

class Linq():

    def __init__(self, iterable):
        """
        Creates a wrapper on an iterable object
        """
        
        if not isinstance(iterable, collections.Iterable):
            raise ValueError("Object is not iterable")
        
        self.iterable = iterable

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

        coolA = Linq(a).select(shape(x)).to_list()

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
        return Linq(predicate(x) for x in self)

    def select_many(self, predicate = lambda x: x):

        """
        Combines elements from multiple lists.

        Example:

        l = Linq([[1, 2], [3, 4]])  
        result = l.select_many().to_list()

        result == [1, 2, 3, 4]
        """

        return Linq(predicate(x) for y in self for x in y)

    def where(self, predicate):
        """
        Filters according to the supplied condition

        Example:

        l = Linq([2, 3, 4])  
        result = l.where(lambda x: x % 2 == 0).to_list()

        result == [2, 4]
        """
        return Linq(x for x in self if predicate(x))

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

    def to_list(self):
        """
        Returns the objects in a list format
        """
        return list(x for x in self)