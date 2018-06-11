`From.forEach(func)`
====================

Executes a function for each element.

Parameters
----------

- `func`
    - The function to be executed.

Examples
--------

```python
>>> subject = [1, 2, 3]
>>> From(subject).forEach(lambda x: print(x))
1
2
3
```