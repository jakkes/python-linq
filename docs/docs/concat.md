`From.concat(iterable)`
=======================

Extends the current collection with another collection.

Parameters
----------

- `iterable`
    - Iterable object

Raises
------

- `ValueError`
    - If the object supplied is not iterable

Returns
-------

- `From` object wrapping the new elements.

Examples
--------
```python
>>> subjectA = [1, 2, 3]
>>> subjectB = [4, 5, 6]
>>> From(subjectA).concat(subjectB).toList()
[1, 2, 3, 4, 5, 6]

>>> subjectA = [
>>>     { "value": 1},
>>>     { "value": 2}
>>> ]
>>> subjectB = [
>>>     { "value": 3 },
>>>     { "value": 4 }
>>> ]
>>> From(subjectA).select(lambda x: x["value"]).concat(
>>>     From(subjectB).select(lambda x: x["value"])
>>> ).toList()
[1, 2, 3, 4]
```