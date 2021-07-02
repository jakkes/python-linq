Contributing
============

Tests
-------
Tests are executed using `pytest`. All test files must be placed in `tests/`.

There is also a utility script for executing tests with limited CPUs. This requires
Docker to be installed and configured in your shell. Run
```python
python scripts/run_tests_with_limited_cpu.py -p 1
```
to run all tests with one CPU only.
