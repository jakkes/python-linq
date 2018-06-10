`From.max(key)`
===============

Finds the maximum value of the elements' given key.

Parameters
----------

- `key`
    - Expression determining which value to find the maximum of.
    - __Default__: Uses the elements as is.

Returns
-------

The maximum value found. If the collection consists of Comparable objects, the object which is greater than all other is returned.

Examples
--------

```python
>>> subject = [1, 2, 3, 4]
>>> From(subject).max()
4

>>> subject = [
>>>     { "value" : 1 },
>>>     { "value" : 2 }
>>> ]
>>> From(subject).max(lambda x: x["value"])
2
```