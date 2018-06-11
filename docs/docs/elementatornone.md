`From.elementAtOrNone(i)`
=========================

Returns an element at a specific location in the sequence.

Parameters
----------

- `i`
    - The index of the element sought for.

Returns
-------
The element at the specified location. If there is no element, `None` is returned.

Examples
--------
```python
>>> subject = [1, 2, 3, 4]
>>> From(subject).elementAtOrNone(2)
3

>>> From(subject).elementAtOrNone(4)
None

>>> subject = [
>>>     { "value": 1 },
>>>     { "value": 2 }
>>> ]
>>> From(subject).elementAtOrNone(0)
{ "value": 1 }
```