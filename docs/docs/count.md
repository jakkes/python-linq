`From.count(condition)`
=======================

Counts the number of elements fulfilling the specified condition

Parameters
----------

- `condition`
    - Expression returning `True` or `False` based on the element as input.
    - __Default__: `True` no matter input, i.e. counting the number of elements.

Returns
-------

Integer: the number of elements fulfilling the condition.

Examples
--------

```python
>>> From([1, 2, 3, 4, 5, 6]).count()
6

>>> From([1, 2, 3, 4, 5, 6]).count(lambda x: x > 3)
3

>>> subject = [
>>>     {
>>>         "id": 1,
>>>         "value": 2
>>>     },{
>>>         "id": 2,
>>>         "value": 3
>>>     }
>>> ]
>>> From(subject).count(lambda x: x["value"] > 2)
1
```