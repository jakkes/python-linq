Documentation
=============

All usage is based on the `From` class which contains all methods. Import it by adding
``` python
from python_linq import From
```

Then wrap any Iterable object to start querying.

Functions
---------

| Function name | Description |
| -: | :- |
| [all](docs/all.md) | Determines whether all elements fulfill a specified condition |
| [any](docs/any.md) | Determines whether any element fulfills a specified condition |
| [average](docs/average.md) | Returns the average value |
| [concat](docs/concat.md) | Adds a collection to the sequence |
| [contains](docs/contains.md) | Checks whether an object is in the collection |
| [count](docs/count.md) | Gives the amount of elements fulfilling a specific condition |
| [distinct](docs/distinct.md) | Filters all elements such that the remaining ones are unique |
| [elementAt](docs/elementat.md) | Returns the element at a specific index |
| [elementAtOrNone](docs/elementatornone.md) | Returns the element at a specific index or `None` if none is found |
| [first](docs/first.md) | Returns the first element |
| [firstOrNone](docs/firstornone.md) | Returns the first element satisfying a given condition. If none is found, `None` is returned |
| [forEach](docs/foreach.md) | Executes a function for each element |
| [groupBy](docs/groupby.md) | Groups the elements by a specific key |
| [groupJoin](docs/groupjoin.md) | Joins the collection with objects from another collection |
| [intersect](docs/intersect.md) | Given another collection, filters the elements such that the remaining ones exist it both the given and the underlying collection |
| [join](docs/join.md) | Joins the collection with objects from another collection |
| [last](docs/lastornone.md) | Returns the last element |
| [lastOrNone](docs/lastornone.md) | Returns the last element satisfying a given condition. If no element is found, `None` is returned |
| [max](docs/max.md) | Finds the maximum value |
| [min](docs/min.md) | Finds the minimum value |
| [order](docs/order.md) | Orders the collection |
| [select](docs/select.md) | Transforms the elements in the collection into a new collection |
| [selectMany](doct/selectMany.md) | Selects elements from all sub-collections |
| [skip](docs/skip.md) | Skips a certain number of elements |
| [skipWhile](docs/skipWhile.md) | Skips elements while a given condition returns `True` |
| [sum](docs/sum.md) | Returns the sum of all elements |
| [take](docs/take.md) | Takes a given number of elements |
| [takeWhile](docs/takewhile.md) | Takes elements as long as a specified condition is `True` |
| [toDict](docs/todict.md) | Returns the iterable as a dictionary |
| [toList](docs/tolist.md) | Returns the iterable as a list |
| [union](docs/union.md) | Combines two collections into a collection containing all elements that are found in at least one of the collections |
| [where](docs/where.md) | Filters the elements based on a condition |