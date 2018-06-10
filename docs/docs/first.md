`From.first(condition)`
=======================

Returns the first element that satisfies the given condition. By default, the first element is returned.

Parameters
----------

- `condition`
    - Expression returning `True` or `False` based on an element as input.
    - __Default__: `True` for any element, i.e. returns the first element.
        - `condition = lambda x: True`

Returns
-------

The first element satisfying the condition.

Examples
--------

```python
>>> subject = [1, 2, 3, 4]
>>> From(subject).first(lambda x: x % 2 == 0)
2

>>> From(subject).first()
1

>>> subject = [ 
>>>     { "value": 1 },
>>>     { "value": 2 }
>>> ]
>>> From(subject).first(lambda x: x["value"] == 2)
{ "value": 2 }
```