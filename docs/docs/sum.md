`From.sum(key)`
===============

Returns the sum of all elements.

Parameters
----------

- `key`
    - Expression determining what value to use for summation.
    - __Default__: Uses the elements as is.
        - `key = lambda x: x`

Returns
-------

The sum.

Examples
--------
```python
>>> subject = [1, 2, 3, 4, 5]
>>> From(subject).sum()
15

>>> From(subject).sum(lambda x: x*x)
55

>>> subject = [
>>>     { "value": 1 },
>>>     { "value": 2 },
>>>     { "value": 3 }
>>> ]
>>> From(subject).sum(lambda x: x["value"])
6
```