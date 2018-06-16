`From.distinct(key)`
====================

Filters the elements such that the remaining ones are unique.

Parameters
----------

- `key`
    - Expression determining what value to use for comparision. 
        - Return type must be `Hashable`.
    - __Default__: Uses the elements as is.
        - `key = lambda x: x`
    - __Note__: If two objects' keys are equal but the objects are not equal, the first object in the sequence is used. Thus, __specifying a key should only be done when certain that two equal keys imply two equal objects__.

Returns
-------

`From` object wrapping all the remaining elements.

Examples
--------

```python
>>> subject = [1, 1, 2, 3, 3, 3]
>>> From(subject).distinct().toList()
[1, 2, 3]

>>> subject = [
>>>     {
>>>         "id": 1,
>>>         "value": 3
>>>     }, {
>>>         "id": 1,
>>>         "value": 3
>>>     }, {
>>>         "id": 2,
>>>         "value": 4
>>>     }, {
>>>         "id": 2,
>>>         "value": 4
>>>     }
>>> ]
>>> From(subject).distinct(lambda x: x["id"]).select(lambda x: x["value"]).toList()
[3, 4]
```
