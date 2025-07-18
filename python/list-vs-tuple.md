## List vs Tuple in Python

- Lists are mutable (can be modified). Tuples are immutable (cannot be modified).
- Iteration over lists is time-consuming. Iterations over tuple is faster.
- Lists are better for performing operations, such as insertion and deletion. Tuples are more suitable for accessing elements efficiently.
- Lists consume more memory. Tuples consume less memory.
- Lists have several built-in methods. Tuples have fewer built-in methods.
- Lists are more prone to unexpected changes and errors. Tuples, being immutable, are less error prone.


# Example
```python
# List
my_list = [1, 2, 3, 4, 5]
# Tuple
my_tuple = (1, 2, 3, 4, 5)
# Modifying a list
my_list[0] = 10
# Attempting to modify a tuple (will raise an error)
try:
    my_tuple[0] = 10
except TypeError as e:
    print(f"Error: {e}")
# Output
# Error: 'tuple' object does not support item assignment
```