`From.intersect(iterable, key)`
===============================

Filters the elements such that the remaining ones exist in both the collections.

Parameters
----------

- `iterable`
    - The other collection of elements
- `key`
    - Expression determining what value to use for comparision. 
        - Return type must be `Hashable`.
    - __Default__: Uses the elements as is.
        - `key = lambda x: x`
    - __Note__: If two objects' keys are equal but the objects are not equal, the first object in the sequence is used. Thus, __specifying a key should only be done when certain that two equal keys imply two equal objects__. If this is not the case, use with caution.

Raises
------
- `ValueError`
    - If the supplied object is not iterable.

Returns
-------
`From` object wrapping the remaining elements.

Examples
--------

```python
>>> subjectA = [1, 2, 3, 4]
>>> subjectB = [3, 4, 5, 6]
>>> From(subjectA).intersect(subjectB).toList()
[3, 4]

>>> subjectA = [
>>>     {
>>>         "id": 1,
>>>         "value": 3
>>>     }, {
>>>         "id": 2,
>>>         "value": 4
>>>     }
>>> ]
>>> subjectB = [
>>>     {
>>>         "id": 2,
>>>         "value": 4
>>>     }, {
>>>         "id": 3,
>>>         "value": 5
>>>     }
>>> ]
>>> From(subjectA).intersect(subjectB, key=lambda x: x["id"]).select(lambda x: x["value"]).toList()
[4]
```