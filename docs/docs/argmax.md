`From.argmax(key)`
===============

Finds the object that maximizes the value of the elements' given key.

Parameters
----------

- `key`
    - Expression determining which value to find the maximum of.

Returns
-------

The object maximizing the value.

Examples
--------

```python
>>> subject = [1, 2, 3, 4]
>>> From(subject).argmax(lambda x: x)
4

>>> subject = [
>>>     { "value" : 1 },
>>>     { "value" : 2 }
>>> ]
>>> From(subject).argmax(lambda x: x["value"])
{ "value": 2 }
```