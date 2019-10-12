Python-LINQ
===========

Python-LINQ aims to bring the useful LINQ features from C# to Python. LINQ makes your code handling data much easier to write and read. For example, let us assume we have the following data set

| id | name | spending |
| :---------: | :-----------: | :---------------: |
| 1 | Steven | 10 |
| 2 | Ann | 20 |
| 3 | Gabriel | 15 |

stored in a variable `data`. We can now use LINQ to query this data, much like SQL. For example

``` python
>>> From(data).sum(lambda x: x["spending"])
45
>>> From(data).avg(lambda x: x["spending"])
15
```

Moreover, by the use of generator functions, the queries require no intermediate lists which significantly increases the performance.

Installation
------------

To install, simply run

``` bash
pip3 install python-linq
```

Documentation & Examples
------------------------

[See this link](docs.md)