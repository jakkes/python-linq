`From.groupby(key, transform)`
==============================

Groups the elements into a collection of `Grouping` objects. A `Grouping` object has a property `key` and `values`. See [Grouping](docs/grouping.md).

Parameters
----------

- `key`
    - Expression determining which value to group by.
- `transform`
    - Expression describing the transform applied to the elements.
    - __Default__: No transform applied.
        - `transform = lambda x: x`

Returns
-------

`From` object wrapping a collection of `Grouping` objects. See [Grouping](docs/grouping.md).

Examples
--------
```python
>>> subject = [
>>>     {
>>>         "age": 10,
>>>         "name": "Steven"
>>>     }, {
>>>         "age": 10,
>>>         "name": "Johan"
>>>     }, {
>>>         "age": 11,
>>>         "name": "Lars"
>>>     }
>>> ]
>>> 
>>> # Keys
>>> From(subject).groupBy(lambda x: x["age"]).select(lambda x: x.key).toList()
[10, 11]

>>> # Names
>>> From(subject).groupBy(lambda x: x["age"]).select(lambda x: x.values).toList()
[ ["Steven", "Johan" ], [ "Lars" ] ]
```