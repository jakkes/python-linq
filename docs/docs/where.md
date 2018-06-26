`From.where(condition)`
=======================

Filters elements based on a specified condition into a new collection.

Parameters
----------
- `condition`
    - Expression returning `True` or `False` based on an element as input.

Returns
-------
Iterable: `From` object wrapping all the elements found to satisfy the condition.

Examples
--------

```python
>>> subject = [1, 2, 3, 4, 5, 6]
>>> From(subject).where(lambda x: x > 3).toList()
[4, 5, 6]

>>> subject = [
>>>     { "value": 2 },
>>>     { "value": 3 }
>>> ]
>>> From(subject).where(lambda x: x["value"] == 3).select(lambda x: x["value"]).toList()
[3]
```