# LINQ
[![Build Status](http://drone.jakke.se/api/badges/jakkes/python-linq/status.svg)](http://drone.jakke.se/jakkes/python-linq)
# [![Coverage Status](https://coveralls.io/repos/github/jakkes/python-linq/badge.svg?branch=master)](https://coveralls.io/github/jakkes/python-linq?branch=master)

Provides simple to use LINQ features to Python 3.x.

## Documentation
See this link: https://jakkes.github.io/python-linq/

## Installing
### From pip
```bash
pip install python-linq
```
### From source
```bash
git clone https://github.com/jakkes/python-linq.git
cd python-linq
pip install -r requirements.txt
```

## Usage
1. Import the `Query` class
2. Write beautiful queries!
```python
>>> from linq import Query
>>> x = Query([1, 2, 3]).select(lambda x: x * x + 3).to_list()
>>> assert x == [4, 7, 12]
```

Distribute heavy queries across multiple processes.
```python
>>> import time
>>> from linq import DistributedQuery
>>> 
>>> def heavy_transformation(x: int):
>>>     time.sleep(10)
>>>     return x**2
>>> 
>>> def less_than_5(x: int):
>>>     return x < 5
>>> 
>>> x = (
>>>     DistributedQuery(range(100), processes=8)
>>>     .where(less_than_5)
>>>     .select(heavy_transformation)
>>>     .to_list()
>>> )
>>> assert x == [0, 1, 4, 9, 16]
```
