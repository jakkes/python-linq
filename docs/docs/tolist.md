`From.toList()`
===============

Returns the elements as a list.

Returns
-------
A list of all elements.

Examples
--------
```python
>>> From([1, 2, 3, 4]).select(lambda x: x*x).toList()
[1, 4, 9, 16]

>>> From([1, 2, 3, 4]).toList()
[1, 2, 3, 4]
```