# Python-linq
Provides simple to use LINQ features to Python 3.x.

Inspired by `py-linq` and `linq.py`.

## Install
Install using pip
```
pip install python-linq
```

## Usage
1. Import the From class
    - `from python_linq import From`
1. Write beautiful queries!
    - `sq3 = From([1, 2, 3]).select(lambda x: x * x + 3).to_list()`
        - `>>> [4, 7, 12]`

## Documentation & Examples
[See this link](https://jakkes.github.io/python-linq/docs.html)