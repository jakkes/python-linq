`From.elementAt(i)`
===================

Returns the element at the specified index.

Parameters
----------
- `i`
    - The index at which to retrieve the element.

Raises
------
- `IndexError`
    - If there is no element at the specified index.

Returns
-------
The element at the specified location.

Examples
--------
```python
>>> subject = [1, 2, 3, 4]
>>> From(subject).elementAt(2)
3

>>> try:
>>>     element = From(subject).elementAt(4)
>>>     print(element)
>>> except IndexError:
>>>     print("Error")
'Error'

>>> subject = [
>>>     { "value": 1 },
>>>     { "value": 2 }
>>> ]
>>> From(subject).elementAt(0)
{ "value": 1 }
```