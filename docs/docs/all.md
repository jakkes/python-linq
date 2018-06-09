`From.all(condition)`
=======================

Determines whether all elements fulfill a specified condition.

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
>>> From([1, 2, 3, 4, 5, 6]).all(lambda x: x == 4)
False

>>> From([1, 2, 3, 4, 5, 6]).count(lambda x: x < 7)
True

>>> subject = [
>>>     {
>>>         "id": 1,
>>>         "value": 2
>>>     },{
>>>         "id": 2,
>>>         "value": 3
>>>     }
>>> ]
>>> From(subject).any(
>>>    lambda x: x["value"] == 2 or x["value"] == 3
>>> )
True
```