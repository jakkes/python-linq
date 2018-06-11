`From.last(condition)`
=======================

Returns the last element that satisfies the given condition. By default, the last element is returned.

Parameters
----------

- `condition`
    - Expression returning `True` or `False` based on an element as input.
    - __Default__: `True` for any element, i.e. returns the last element.
        - `condition = lambda x: True`

Returns
-------

The last element satisfying the condition.

Raises
------

- `NoSuchElementError`
    - If no element is found to satisfy the condition.
    - Imported by `from python_linq import NoSuchElementError`

Examples
--------

```python
>>> subject = [1, 2, 3, 4]
>>> From(subject).last(lambda x: x < 4)
3

>>> From(subject).last()
4

>>> try:
>>>     attempt = From(subject).last(lambda x: x > 4)
>>>     print(attempt)
>>> except NoSuchElementError:
>>>     print("Error")
'Error'

>>> subject = [
>>>     { "value": 1 },
>>>     { "value": 2 }
>>> ]
>>> From(subject).last(lambda x: x["value"] > 0)
{ "value": 2 }
```