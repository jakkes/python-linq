# Python-linq
Provides simple to use LINQ features to Python.

Inspired by `py-linq` and `linq.py`.

## Install
Install using pip
```
pip install python-linq
```

## Usage
1. Import the Linq class
    - `from python_linq import Linq`
1. Wrap an iterable using the Linq class
    - `numbers = Linq([1, 2, 3])`
1. Write beautiful queries!
    - `sq3 = numbers.select(lambda x: x * x + 3).to_list()`
        - `>>> [4, 7, 12]`

## Examples
Coming soon... Meanwhile, have a look at the tests.

## Documentation
Coming soon...