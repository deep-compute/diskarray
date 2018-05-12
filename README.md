# DiskArray

A resizable and readable numpy array on disk.

This module is built on numpy `memmap` used for accessing and modifying small segments of large files on disk, without reading the entire file into memory.

This module also supports appending your numpy arrays to disk array at any time.

## Installation

> Prerequisites: Python

```bash
$ sudo pip install diskarray
```

## Quick Example

```python
>>> import numpy as np
>>> from diskarray import DiskArray

>>> data = np.array([[2 , 3, 4], [1, 2, 3]])

>>> da = DiskArray('/tmp/disk.array', shape=(0, 3), dtype=np.float32)

>>> da.extend(data)

>>> print(da[:])
```

## Usage

`DiskArray` supports two methods, extend and append.

`extend` is used to append arrays to disk array.

`append` is used to append single array at a time.

### Importing

#### Using extend

Example1:

```python
>>> import numpy as np
>>> from diskarray import DiskArray

>>> data = np.array([[2 , 3, 4], [1, 2, 3]])

# creating object to disk array
>>> da = DiskArray('/tmp/disk.array', shape=(0, 3), capacity=(10, 3), growby=200, dtype=np.float32)

# extend the data to disk array
>>> da.extend(data)

# Get the full array
>>> print(da[:])

# Get the data which is in first row
>>> print(da[1])

# Get the data from first row to third row
>>> print(da[1:3])

# Get the data which is in 1st row 1st column
>>> print(da[1][1])
```

- `/tmp/disk.array` is the file which holds disk arrays.
- `shape` is the size of the disk array.
- `capacity` is the total capacity of the disk array.
This is used because when we want to extend arrays which are larger than `shape` then DiskArray creates again memmap to the file which is costliear operation.
So we are using `capacity` to directly create disk array with the size of `capacity`

- `capacity` and `growby` are optional which takes `shape` as `capacity` and `growby` as `10000` when these are not given.

Example2:

```python
>>> import numpy as np
>>> from diskarray import DiskArray

>>> dtype = [('token', np.uint32), ('count', np.uint32), ('vec', np.float32)]

>>> data = np.array([[(1, 0,  0.), (0, 2,  0.), (0, 2,  0.)], [(1, 0,  0.), (0, 2,  0.), (0, 2,  0.)]], dtype=dtype)

>>> da = DiskArray('/tmp/disk.array', shape=(0, 3), capacity=(10, 3), dtype=dtype)

>>> da.extend(data)

# Get the full array
>>> print(da[:])

# Get the count values at 1th row
>>> print(da[1]['count'])

# Get the token value at 1th row 2nd column
>>> print(da[1][2]['token'])

# Modify the vec value at 1th row 2nd column
>>> da[1][2]['vec'] = 10.0
```

#### Using append

Example:

```python
>>> import numpy as np
>>> from diskarray import DiskArray

>>> data = np.array([[2 , 3, 4])

# creating object to disk array
>>> da = DiskArray('/tmp/disk.array', shape=(0, 3), capacity=(10, 3), growby=200, dtype=np.float32)

# append 1 dimensional array to disk array
>>> da.append(data)
>>> da.append(data + 1)

# Get the full array
>>> print(da[:])

# Get the data which is in first row
>>> print(da[1])

# Get the data from first row to third row
>>> print(da[1:3])

# Get the data which is in 1st row 1st column
>>> print(da[1][1])
```

`growby` is used to increase the size of disk array when it reaches to it's maximum limit.

### Interactive console

```bash
# diskarray provides command to directly interact with it

$ diskarray interact <fpath> <shape> <dtype> --capacity <capacity> --growby <growby> --mode <mode>

# <fpath> is the input file which is used to store disk arrys.
# <shape> is the size of the disk array.
# <dtype> is the data type of the disk array.
# <capacity> is the total capacity of the disk array.
# <growby> is used to increase the size of the disk array when it reaches to it's maximum limit.
# <mode> is to open the disk array in that mode.
```

Example:

```bash
$ diskarray interact /tmp/test '(0, 3)' np.float32 --capacity '(10, 3)' --growby 5 --mode r+
DiskArray Console
>>> import numpy as np
>>> da.append(np.array([1, 2, 3]))
```

## Running Tests

```
$ python setup.py test
```
