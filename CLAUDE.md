# PyDataProcessor Development Guide

## Build Commands
- Install dependencies: `pip install -e .`
- Compile C++ extension: `python setup.py build_ext --inplace`
- Run tests: `python -m unittest discover`
- Run code: `python analyze_data.py`

## Code Style Guidelines
- **Imports**: Standard library first, then third-party, then local modules
- **Formatting**: 4-space indentation, 80-character line limit
- **Naming**: 
  - Python: snake_case for variables/functions, CamelCase for classes
  - C++: camelCase for methods, PascalCase for classes
- **Error Handling**: Use try/except in Python, error checks in C++
- **Types**: Use NumPy arrays for numerical data, list for Python interfaces
- **Documentation**: Docstrings for Python functions, comment blocks for C++
- **Performance**: Optimize performance-critical code in C++ extensions
- **Memory Management**: Avoid memory leaks in C++ implementations