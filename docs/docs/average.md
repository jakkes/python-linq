`From.average(key)`
===================

Returns the average value of all elements.

Parameters
----------

- `key`
    - Expression determining what value to use for the calculation.
    - __Default__: Uses the elements as is.
        - `key = lambda x: x`

Returns
-------

Returns the average value.

Examples
--------

```python
>>> subject = [1, 2, 3, 4, 5]
>>> From(subject).average()
3

>>> From(subject).average(lambda x: x*x)
11

>>> subject = [
>>>     { "value": 1 },
>>>     { "value": 2 },
>>>     { "value": 3 }
>>> ]
>>> From(subject).average(lambda x: x["value"])
2
```