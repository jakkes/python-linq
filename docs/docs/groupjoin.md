`From.groupJoin(extension, innerKey, outerKey, innerTransform, outerTransform`
==============================================================================

Joins two iterables based on `innerKey` and `outerKey`. The join is performed such that each element in the extension is associated to an element using a `Joining` object. Each element may have multiple elements from the extension associated to it.

Parameters
----------

- `extension`
    - The outer iterable.
- `innerKey`
    - Expression determining which key to use from the inner sequence.
- `outerKey`
    - Expression determining which key to use from the outer sequence.
- `innerTransform`
    - Expression describing the transform of the inner objects.
    - __Default__: No transform is applied.
        - `innerTransform = lambda x: x`
- `outerTransform`
    - Expression describing the transform of the outer objects.
    - __Default__: No transform is applied.
        - `innerTransform = lambda x: x`

Raises
------
- `ValueError`
    - If `extension` is not iterable.

Returns
-------

`From` object wrapping a collection of `Joining` objects.

### Joining objects ###
Each `Joining` object has two attributes, `inner` and `outer`.
- `Joining.inner`
    - The inner element associated to all of the outer elements.
- `Joining.outer`
    - A list of outer elements associated to the inner element.

Examples
--------

```python
>>> grades = [
>>>     {
>>>         "userid": 1,
>>>         "grade": "A"
>>>     }, {
>>>         "userid": 1,
>>>         "grade": "B"
>>>     }, {
>>>         "userid": 2,
>>>         "grade": "B"
>>>     }, {
>>>         "userid": 2,
>>>         "grade": "B"
>>>     }
>>> ]
>>> students = [
>>>     {
>>>         "id": 1,
>>>         "name": "Jakob"
>>>     }, {
>>>         "id": 2,
>>>         "name": "Johan
>>>     }
>>> ]
>>> 
>>> From(students).groupJoin(
>>>     grades,
>>>     innerKey = lambda x: x["id"],
>>>     outerKey = lambda x: x["userid"],
>>>     innerTransform = lambda x: x["name"],
>>>     outerTransform = lambda x: x["grade"]
>>> ).select(lambda x: x.inner).toList()
['Jakob', 'Johan']

>>> From(students).groupJoin(
>>>     grades,
>>>     innerKey = lambda x: x["id"],
>>>     outerKey = lambda x: x["userid"],
>>>     innerTransform = lambda x: x["name"],
>>>     outerTransform = lambda x: x["grade"]
>>> ).select(lambda x: x.outer).toList()
[ ['A', 'B'], ['B', 'B'] ]

```