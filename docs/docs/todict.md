`From.toDict(key, transform)`
=============================

Returns the collection as a dictionary.

Parameters
----------

- `key`
    - Expression determining the key for each elements. Must evaluate uniquely for each elements.
- `transform`
    - Expression describing the transform applied to the elements before added to the dictionary
    - __Default__: No transform applied
        - `transform = lambda x: x`

Raises
------

- `KeyError`
    - If two elements share the same key

Returns
-------

A Dictionary

Examples
--------

```python
>>> From([1,2,3,4]).toDict(lambda x: str(x*x))
{
    '1': 1,
    '4': 2,
    '9': 3,
    '16': 4
}

>>> From([1,2,3,4]).toDict(lambda x: str(x), transform = lambda x: x*x)
{
    '1': 1,
    '2': 4,
    '3': 9,
    '4': 16
}

>>> try:
>>>     From([1,2,3,4]).toDict(lambda x: str(x % 3))
>>> except KeyError:
>>>     print("error!")
'error!'
```