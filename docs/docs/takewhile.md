`From.takeWhile(condition)`
===========================

Takes elements to form a new collection as long as the condition is `True`.

Parameters
----------
- `condition`
    - Expression determining a boolean

Returns
-------

`From` object wrapping the new collection.

Examples
--------
```python
>>> From([1, 2, 3, 4, 5, 6]).takeWhile(lambda x: x % 3 != 0).toList()
[1, 2]
```