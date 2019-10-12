`From.argmin(key)`
===============

Finds the object that minimizes the value of the elements' given key.

Parameters
----------

- `key`
    - Expression determining which value to find the minimize of.

Returns
-------

The object minimizing the value.

Examples
--------

```python
>>> subject = [1, 2, 3, 4]
>>> From(subject).argmin(lambda x: x)
1

>>> subject = [
>>>     { "value" : 1 },
>>>     { "value" : 2 }
>>> ]
>>> From(subject).argmin(lambda x: x["value"])
{ "value": 1 }
```