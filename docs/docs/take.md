`From.take(count)`
==================

Takes the first given number of elements to form a new iterable collection.

Parameters
----------

- `count`
    - The number of elements to choose
    - __Note__: This parameter is only a maximum limit. If there are fewer elements than the given count, the remaining elements will be fewer than the specified count.

Returns
-------

`From` object wrapping the elements chosen.

Examples
--------

```python
>>> From([1, 2, 3]).take(2).toList()
[1, 2]
```