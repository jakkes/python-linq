`From.select(transform)`
========================

Transforms the elements in the collection into a new collection

Parameters
----------

- `transform`
    - Function returning a transformed element.

Returns
-------

Iterable: A `From` object wrapping the transformed elements.

Examples
--------

```python

>>> subject = [
>>>     {
>>>         "id": 1,
>>>         "value": 2
>>>     }, {
>>>         "id": 2,
>>>         "value": 3
>>>     }
>>> ]
>>> From(subject).select(lambda x: x["value"]).toList()
[2, 3]

>>> subject = [1, 2]
>>> def shape(x):
>>>     return {
>>>         "value": x
>>>     }
>>> 
>>> From(subject).select(shape).toList()
[ {"value": 1}, {"value": 2} ]
```