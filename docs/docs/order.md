`From.order(key, descending)`
===============================

Orders the collection by given key.

Parameters
----------

- `key`
    - Expression determining which key to use
    - __Default__: Uses the elements as is
        - `key = lambda x: x`
- `descending`
    - `True` or `False` deciding whether the elements should be ordered in descending order or not.
    - __Default__: `False`

Returns
-------

`From` object wrapping the same but ordered collection.

Examples
--------

```python
>>> From([1, 2, 4, 3, 7, 6, 5]).order(descending=True).toList()
[7, 6, 5, 4, 3, 2, 1]

>>> From([1, 2, 4, 3, 7, 6, 5]).order().toList()
[1, 2, 3, 4, 5, 6, 7]

>>> From([1, 2, 4, 3, 7, 6, 5]).order(key=lambda x: x % 3).toList()
[3, 6, 1, 4, 7, 2, 5]
```