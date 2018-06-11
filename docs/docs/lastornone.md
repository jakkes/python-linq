`From.firstOrNone(condition)`
=======================

Returns the last element that satisfies the given condition. If no element satisfies the condition, `None` is returned.

Parameters
----------

- `condition`
    - Expression returning `True` or `False` based on an element as input.

Returns
-------

The last element satisfying the condition or `None`.

Examples
--------

```python
>>> subject = [1, 2, 3, 4]
>>> From(subject).lastOrNone(lambda x: x % 2 == 0)
4

>>> From(subject).lastOrNone(lambda x: x > 4)
None

>>> subject = [ 
>>>     { "value": 1 },
>>>     { "value": 2 }
>>> ]
>>> From(subject).last(lambda x: x["value"] > 0)
{ "value": 2 }
```