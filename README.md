# pytest-typechecker

this is a plugin for pytest that allows you to create tests
that verify how a type checker responds to your code.

This currently supports these type checkers:

* pyright
* mypy

## File name format

this plugin looks for files starting with `test` and ending with `types.py` or `types_xfail.py`.
for example `test_something_types.py`

### global xfail

if you want to mark the hole test as `xfail` end it with `types_xfail.py`, for example.

```python
# test_wrong_types_xfail.py

x: 123 = "abc"
y: str = 123
```

### Only run specific checkers

if you include the name of a checker with `_` around it only those checkers will be run.
for example `test_recursion_pyright_types.py`

### xfail specific checkers

if you provide a `x` before the checker name, it will be run in xfail mode.
for example `test_recursion_xmypy_types.py` will run all checkers, but mark the mypy one as `xfail`

if you only want to run mypy and have it be xfail use this workaround: `test_recursion_mypy_types_xfail.py`

this can be combined, for example `test_recursion_pyright_xmypy_types.py` will run only pyright and mypy, but run mypy in xfail mode.

### dont run specific checkers
if you provide a `n` before the checker name, it will not be run.
for example `test_recursion_nmypy_types.py` will run all checkers, except mypy.