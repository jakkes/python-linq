`From.contains(obj)`
=======================

Determines if the given object is in the collection.

Parameters
----------

- `obj`
    - The object to check if in the collection.

Returns
-------
Boolean: `True` if the given object is found in the collection, otherwise `False`

Examples
--------

```python
>>> From([1, 2, 3, 4]).contains(2)
True

>>> From([1, 2, 3, 4]).contains(5)
False
```