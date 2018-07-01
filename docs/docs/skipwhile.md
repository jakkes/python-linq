`From.skipWhile(condition)`
===========================

Skips elements as long as the given condition is `True`.

Parameters
----------

- `condition`
    - Expression returning `True` or `False`
    - __Note__: Elements are skipped until the condition returns `False` the first time. To filter elements that do not fulfill the condition, see the [where](where.md) method.

Returns
-------

`From` object wrapping the remaining elements.

Examples
--------

```python
>>> From([1,2,3,4,5,6,7]).skipWhile(lambda x: x % 3 != 0).toList()
[3,4,5,6,7]
```