`From.selectMany(transform)`
============================

Selects and transforms elements from sub-collections into one single collection. Useful when the iterable object is made up by multiple iterable objects that you would like to aggregate into one.

Parameters
----------
- `transform`
    - The transform to be applied to each object. Should be a function with a single input argument returning a transformed object.
    - __Default__: No transformed applied, i.e. `transform = lambda x: x`

Returns
-------
Iterable: `From` object wrapping the new elements.

Examples
--------

Note that `selectMany` works much like `select`, only that it concatenates multiple collections into one.

```python
>>> subject = [
>>>     [1, 2, 3, 4],
>>>     [5, 6, 7, 8]
>>> ]
>>> From(subject).selectMany().toList()
[1, 2, 3, 4, 5, 6, 7, 8]

>>> subject = [
>>>     [{"value": 1}, {"value": 2}],
>>>     [{"value": 3}, {"value": 4}]
>>> ]
>>> From(subject).selectMany(lambda x: x["value"]).toList()
[1, 2, 3, 4]
```

You may also use regular functions to shape new objects
```python
>>> def shape(x):
>>>     return {"value": x}
>>> 
>>> subject = [
>>>     [1, 2],
>>>     [3, 4]
>>> ]
>>> From(subject).selectMany(shape).toList()
[
    [ { "value": 1 }, { "value": 2 } ],
    [ { "value": 3 }, { "value": 4 } ]
]
```