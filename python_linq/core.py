import collections
from python_linq.linq_exceptions import NoSuchElementError

class From():

    def __init__(self, iterable):
        """Wraps an iterable object
        
        Arguments:
            iterable {Iterable} -- An iterable collection of objects
        
        Raises:
            ValueError -- If iterable is not an iterable collection
        """
        if not isinstance(iterable, collections.Iterable):
            raise ValueError("Object is not iterable")

        
        self.iterable = iterable
        self.extensions = []

    def __contains__(self, obj):
        for o in self:
            if o == obj:
                return True
        return False

    def contains(self, obj):
        """Determines if sequence contains the given object
        
        Arguments:
            obj -- The object to look for
        
        Returns:
            bool -- `True` if the object is found, otherwise `False`.
        """
        return obj in self
    
    def __iter__(self):
        for obj in self.iterable:
            yield obj
        
        for extension in self.extensions:
            for obj in extension:
                yield obj

    def count(self, condition = lambda x: True):
        """Counts the objects satisfying the condition
        
        Keyword Arguments:
            condition {[type]} -- Expression returning `True` or `False`. (default: counts all objects)
        
        Returns:
            int -- The number of objects found satisfying the condition
        """

        return sum(1 for x in self if condition(x))

    def any(self, condition):
        """Checks whether any object fulfilling the condition is found
        
        Arguments:
            condition -- Expression returning `True` or `False`. Could be any lambda expression or function with a single input argument.
        
        Returns:
            bool -- `True` if any satisfactory object is found, otherwise `False`
        """

        return any(condition(x) for x in self)

    def all(self, condition):
        """Checks whether all objects satisfy a given condition
        
        Arguments:
            condition -- Expression returning `True` or `False`. Could be any lambda expression or function with a single input argument.

        Returns:
            bool -- `True` if all objects are found to satisfy the condition, otherwise `False`
        """

        return all(condition(x) for x in self)

    def select(self, transform):
        """Transforms each object in the sequence.
        
        Arguments:
            transform -- Function describing the transformation
        
        Returns:
            Iterable {From} -- Returns a `From` object wrapping the new objects for further use
        """
        return From(transform(x) for x in self)

    def selectMany(self, transform = lambda x: x):
        """Selects objects, with the possibility of transforming them, for all the underlying lists into
        one sequence. Useful when the collection is composed of multiple subcollections containing objects. 
        
        Keyword Arguments:
            transform -- Expression describing the transformation. (default: no transform is applied and the underlying objects are selected as is)
        
        Returns:
            Iterable {From} -- Returns a `From` object wrapping the new objects for further use.
        """

        return From(transform(x) for y in self for x in y)

    def where(self, condition):
        """Filters the sequence for the given condition
        
        Arguments:
            condition -- Expression returning `True` or `False` with a single input.
        
        Returns:
            Iterable {From} -- Returns a `From` object wrapping all objects for which the condition is True.
        """

        return From(x for x in self if condition(x))

    def max(self, key = lambda x: x):
        """Returns the maximum value found
        
        Keyword Arguments:
            key -- Expression determining which value to use (default: Uses the element as is)
        
        Returns:
            object -- Returns the maximum value
        """

        return max(key(x) for x in self)

    def min(self, key = lambda x: x):
        """Returns the minimum value found
        
        Keyword Arguments:
            key -- Expression determining which value to use (default: Uses the element as is)
        
        Returns:
            object -- Returns the maximum value
        """

        return min(key(x) for x in self)

    def first(self, condition = lambda x: True):
        """Returns the first element found to satisfy the given condition
        
        Keyword Arguments:
            condition -- Expression returning `True` or `False` (default: Returns the first element in the sequence)
        
        Raises:
            NoSuchElementError -- If no element is found to satisfy the condition
        
        Returns:
            object -- The first element found to satisfy the given condition
        """

        for x in self:
            if condition(x):
                return x

        raise NoSuchElementError()

    def firstOrNone(self, condition = lambda x: True):
        """Returns the first element found to satisfy the given condition
        
        Keyword Arguments:
            condition -- Expression returning `True` or `False` (default: {lambdax:True})
        
        Returns:
            object -- The first element found to satisfy the given condition. If no element is found, None is returned.
        """

        for x in self:
            if condition(x):
                return x
        return None

    def lastOrNone(self, condition = lambda x: True):
        """Returns the last element found to satisfy the given condition
        
        Keyword Arguments:
            condition -- Expression returning `True` or `False` (default: {lambdax:True})
        
        Returns:
            object -- The last element found to satisfy the given condition. If no element is found, None is returned.
        """
        last = None
        for x in self:
            if condition(x):
                last = x
        return last

    def last(self, condition = lambda x: True):
        """Returns the last element found to satisfy the given condition
        
        Keyword Arguments:
            condition -- Expression returning `True` or `False` (default: Returns the first element in the sequence)
        
        Raises:
            NoSuchElementError -- If no element is found to satisfy the condition
        
        Returns:
            object -- The last element found to satisfy the given condition
        """
        
        last = self.lastOrNone(condition)

        if last is None:
            raise NoSuchElementError()
        else:
            return last

    def sum(self, key = lambda x: x):
        """Returns the sum over all elements
        
        Keyword Arguments:
            key -- Expression determining which key to use (default: Uses the elements as is)
        
        Returns:
            object -- The sum over all elements
        """

        return sum(key(x) for x in self)

    def average(self, key = lambda x: x):
        """Returns the average of all elements
        
        Keyword Arguments:
            key -- Expression determining which key to use (default: Uses the elements as is)
        
        Returns:
            object -- The average of all elements
        """

        return self.sum(key) * 1.0 / self.count()

    def concat(self, iterable):
        """Adds an iterable to the sequence
        
        Arguments:
            iterable {Iterable} -- The collection to add
        
        Raises:
            ValueError -- If the supplied object is not iterable
        
        Returns:
            Iterable {From} -- Returns a `From` object that wraps the new collection of objects
        """


        if not isinstance(iterable, collections.Iterable):
            raise ValueError("Object is not iterable")

        self.extensions.append(iterable)
        return self

    def distinct(self, key = lambda x: x):
        """Gives all objects that are distinct in the given key, i.e. having unique return values in key.
        
        Keyword Arguments:
            key -- Expression determining which key to use. The key must be Hashable (default: Uses the elements as is)
        
        Returns:
            [type] -- [description]
        """

        cache = set()

        def sequence():
            for x in self:
                if key(x) in cache:
                    continue
                else:
                    cache.add(key(x))
                    yield x

        return From(x for x in sequence())
        
    def elementAtOrNone(self, i):
        """Returns the element at the given position. If there is no element at the given position, `None` is returned.
        
        Arguments:
            i {int} -- The position at which to retrieve the element from
        
        Returns:
            object -- The object at the given position. `None` if there is none.
        """

        n = 0
        for o in self:
            if n == i:
                return o
            n += 1
        return None

    def elementAt(self, i):
        """Returns the element at the given position.
        
        Arguments:
            i {int} -- The position at which to retrieve the element from
        
        Raises:
            IndexError -- If there is no object at the given position
        
        Returns:
            object -- The element at the given position
        """

        result = self.elementAtOrNone(i)
        if result is None:
            raise IndexError()
        else:
            return result

    def intersect(self, iterable, key = lambda x: x):
        """Returns all elements found in both sequences.
        
        Arguments:
            iterable {Iterable} -- The other iterable to compare to.
        
        Keyword Arguments:
            key -- Expression determining which key to use. Key must be hashable. (default: The elements are used as is)
        
        Raises:
            ValueError -- If the given iterable is not Iterable
        
        Returns:
            Iterable {From} -- Returns a `From` object wrapping the new sequence of elements.
        """

        if not isinstance(iterable, collections.Iterable):
            raise ValueError("Object is not iterable")
        
        def sequence():
            for x in self:
                if From(iterable).any(lambda y: x == y):
                    yield x

        return From(x for x in sequence())

    def toList(self):
        """Returns the sequence as a list.
        
        Returns:
            List -- A list containing all elements in the sequence.
        """

        return list(x for x in self)

    def groupBy(self, key, transform = lambda x: x):
        """Groups all elements based on the given key.
        
        Arguments:
            key -- Expression determining which key to use
        
        Keyword Arguments:
            transform -- Expression describing the transform the objects when creating the groups.
            Can be any lambda expression or function with a single input argument (default: Use the elements as is)
        
        Returns:
            Iterable {From} -- A `From` object wrapping a collection of `Grouping` objects.
            Every `Grouping` object has two attributes, `key` and `values` which contains the
            transformed objects.
        """

        def sequence():

            ### TODO: Rewrite this using yield

            groups = dict()
            for x in self:
                k = key(x)
                if k in groups:
                    groups[k].append(transform(x))
                else:
                    groups[k] = [transform(x)]

            for k in groups:
                yield Grouping(k, groups[k])

        return From(x for x in sequence())

    def forEach(self, func):
        
        """Executes a function for each element.
        """

        for x in self:
            func(x)

    def groupJoin(self, extension, innerKey, outerKey, innerTransform = lambda x: x, outerTransform = lambda x: x):
        
        """Joins the sequence with objects from another sequence.
        
        Arguments:
            extension {Iterable} -- The other sequence
            innerKey -- Expression determining what key to use from the inner objects
            outerKey -- Expression determining what key to use from the outer objects
        
        Keyword Arguments:
            innerTransform -- The transform to apply to the inner objects (default: no transform applied)
            outerTransform -- The transform to apply to the outer objects (default: no transform applied)
        
        Returns:
            Iterable {From} -- Returns a `From` object wrapping a collection of `Joining` objects. Each `Joining` object contains
            the properties `inner` and `outer`. `inner` gives the inner object and `outer` is a collection of all outer object
            paired with said inner object.
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

        return From(x for x in sequence())

    def join(self, extension, innerKey, outerKey, transform):
        """Joins the sequence of objects with another sequence of objects on the given keys and yields a
        a new sequence of objects according to the transform specified. Equivalent to INNER JOIN in SQL.
        
        Arguments:
            extension {Iterable} -- The sequence to join into the current one
            innerKey -- Expression determining which key to use on the current sequence
            outerKey -- Expression determining which key to use on the extending sequence
            transform -- Expression shaping the objects which to returns. Can be any
            lambda expression or function with two inputs, the inner object followed by the outer object.
        
        Raises:
            ValueError -- If the extension is not Iterable
        
        Returns:
            Iterable {From} -- `From` object wrapping the new sequence of objects.
        """


        if not isinstance(extension, collections.Iterable):
            raise ValueError("Object is not iterable")

        def sequence():
            for x in self:
                outerObjs = From(extension).where(lambda y: innerKey(x) == outerKey(y))
                for outerObj in outerObjs:
                    yield transform(x, outerObj)

        return From(x for x in sequence())

    def take(self, count):
        """Selects the amount of elements specified
        
        Arguments:
            count -- The number of elements to select
        
        Returns:
            Iterable {From} -- `From` object wrapping the selected elements
        """

        def sequence():
            n = 0
            for x in self:
                
                if n >= count:
                    break
                
                yield x
                n += 1

        return From(x for x in sequence())

    def takeWhile(self, condition):
        """Selects elements as long as the condition is fulfilled
        
        Arguments:
            condition -- Expression returning `True` or `False`
        
        Returns:
            Iterable {From} -- `From` object wrapping the selected elements
        """


        def sequence():
            for x in self:
                if condition(x):
                    yield x
                else:
                    break

        return From(x for x in sequence())

    def order(self, key = lambda x: x, descending = False):
        """Orders the sequence with respect to the given key
        
        Keyword Arguments:
            key -- Expression determining which key to use (default: uses the elements as is)
            descending {bool} -- Whether or not to sort in descending order (default: {False})
        
        Returns:
            Iterable {From} -- `From` object wrapping the sorted sequence
        """

        def sequence():
            yield from sorted(self, key=key, reverse=descending)

        return From(x for x in sequence())

    def skip(self, count):
        """Skips the first elements in the sequence

        Arguments:
            count {int} -- The number of elements to skip

        Returns:
            Iterable {From} -- The remaining elements wrapped in a From object.
        """

        def sequence():
            i = 0
            for obj in self:
                if i < count:
                    i += 1
                    continue

                yield obj

        return From(x for x in sequence())

    def skipWhile(self, condition):
        """Skips the first elements in the sequence while the condition evaluates `True`

        Arguments:
            condition -- The number of elements to skip

        Returns:
            Iterable {From} -- The remaining elements wrapped in a From object.
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
        
        return From(x for x in sequence())

    def toDict(self, key, transform = lambda x: x):
        
        """Returns the sequence as a dictionary where the key is given by `key`.

        Arguments:
            key -- Expression determining the key for each element. Much evaluate to a unique value for each element.

        Keyword Arguments:
            transform -- Expression describing the transform of the elements before added to the dictionary

        Returns:
            {Dictionary} -- A dictionary where the keys are giving by `key` and elements by `transform`.

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

    def union(self, outer, key = lambda x: x, transform = lambda x: x):
        """Find the union of two sequences, i.e. all objects that are within either one the two sequences.
        Only unique objects (with respect to the key) are returned.
        
        Arguments:
            outer {Iterable} -- The other sequence
        
        Keyword Arguments:
            key -- Expression determining which key to use for comparison. Key must be hashable (default: uses the elements as is)
            transform -- Expression determining the transform of the elements selected (default: no transform applied)
        
        Raises:
            ValueError -- If `outer` is of instance Iterable
        
        Returns:
            Iterable {From} -- `From` object wrapping the new elements
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
                    yield transform(x)

            for x in outer:
                if key(x) in cache:
                    continue
                else:
                    cache.add(key(x))
                    yield transform(x)

        return From(x for x in sequence())

class Grouping:
    def __init__(self, key, values):
        self.values = values
        self.key = key

    def __iter__(self):
        yield from self.values

    def __repr__(self):
        return {
            self.key: self.values
        }.__repr__()

class Joining:
    def __init__(self, inner, outer):
        self.inner = inner
        self.outer = outer

    def __iter__(self):
        yield from self.outer

    def __repr__(self):
        return {
            "inner": self.inner,
            "outer": self.outer
        }.__repr__()
