`From.join(extension, innerKey, outerKey, transform)`
=====================================================

Joins two collections on the given key

Parameters
----------

- `extension`
    - The other collection to join the current one with.
- `innerKey`
    - Expression determining which key to use of the objects in the wrapped collection.
- `outerKey`
    - Expression determining which key to use of the objects in the extension
- `transform`
    - Expression giving the object to create based on the two joined objects.
    - Must be a function with two input parameters where the first one is the object associated to the `innerKey` and the other associated to the `otherKey`

Raises
------

- `ValueError`
    - If the extension collection is not iterable

Returns
-------

`From` object wrapping the collection of joined objects.

Notes
-----

- This method is equivalent to the `INNER JOIN` of SQL, i.e. only returns elements that were successfully paired with another. If an outer join is what is sought for, see [groupJoin](groupjoin.md)
- If two objects from the extension are found to pair with an element from the wrapped collection then two joined objects are returned, one for each pairing.

Examples
--------

```python
>>> subjA = [1, 2, 3, 4, 5]
>>> subjB = [2, 3, 4, 5, 6]
>>> From(subjA).join(
>>>     subjB,
>>>     lambda x: x,
>>>     lambda x: x+1,
>>>     lambda x, y: {"inner": x, "outer": y}
>>> ).toList()
[
    { "inner": 3, "outer": 2},
    { "inner": 4, "outer": 3},
    { "inner": 5, "outer": 4}
]
```