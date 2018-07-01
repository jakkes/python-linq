`From.skip(count)`
==================

Skips a specified number of elements.

Parameters
----------

- `count`
    - Integer, the number of elements to skip

Returns
-------

`From` object wrapping the remaining elements.

Examples
--------

```python
>>> From([1,2,3,4,5,6,7]).skip(3).toList()
[4,5,6,7]
```