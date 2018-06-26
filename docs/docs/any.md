`From.any(condition)`
=======================

Determines whether any element fulfills a specified condition.

Parameters
----------

- `condition`
    - Expression returning `True` or `False` based on an element as input.

Returns
-------

Boolean: `True` if any element fulfilling the condition is found, otherwise `False`.

Examples
--------

```python
>>> From([1, 2, 3, 4, 5, 6]).any(lambda x: x == 4)
True

>>> From([1, 2, 3, 4, 5, 6]).any(lambda x: x > 6)
False

>>> subject = [
>>>     {
>>>         "id": 1,
>>>         "value": 2
>>>     },{
>>>         "id": 2,
>>>         "value": 3
>>>     }
>>> ]
>>> From(subject).any(lambda x: x["value"] == 2)
True
```