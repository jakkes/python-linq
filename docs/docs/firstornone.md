`From.firstOrNone(condition)`
=======================

Returns the first element that satisfies the given condition. If no element satisfies the condition, `None` is returned.

Parameters
----------

- `condition`
    - Expression returning `True` or `False` based on an element as input.

Returns
-------

The first element satisfying the condition or `None`.

Examples
--------

```python
>>> subject = [1, 2, 3, 4]
>>> From(subject).firstOrNone(lambda x: x % 2 == 0)
2

>>> From(subject).firstOrNone(lambda x: x > 4)
None

>>> subject = [ 
>>>     { "value": 1 },
>>>     { "value": 2 }
>>> ]
>>> From(subject).first(lambda x: x["value"] == 2)
{ "value": 2 }
```