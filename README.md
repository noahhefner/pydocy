# Pydocy

Documentation generator for Python

## Overview

Things that are documented:

- Modules: Docstring at the top of a Python file.
- Classes: Docstring under the defintion of a class.
- Functions: Docstring under the definition of a function.

Docstrings should contain valid yaml syntax for parsing.

## Out of Scope

The following are out of scope for the initial implementation:

- functions / classes defined within functions
- evaluating types in function signatures

## Parsing

Stage One

iterate over every python file in the tree. record the

for file in src

    if file is .py file



## Ideas

Perhaps packages could also be documented by the first docstring in the __init__ file?