import os
import sys
from functools import reduce
from logging import Logger

import numpy as np

from .exception import AppendNotSupported

class DiskArray(object):
    GROWBY = 10000

    def __init__(self, fpath, dtype, mode='r+', shape=None,
        capacity=None, growby=GROWBY, log=Logger):
        '''
        >>> import numpy as np
        >>> da = DiskArray('/tmp/test.array', shape=(0, 3), dtype=np.float32)
        >>> print(da[:])
        []
        '''

        self._fpath = fpath
        self._shape = shape
        self._capacity_shape = capacity or shape
        self._dtype = dtype
        self._mode = mode
        self._growby = growby
        self.log = log

        if not os.path.exists(fpath):
            open(fpath, 'w').write('\x00') # touch file

        self.data = None
        self._update_ndarray()

    def _update_ndarray(self):
        if self.data is not None:
            self.data.flush()

        self._create_ndarray()

    def _create_ndarray(self):
        self.data = np.memmap(self._fpath,
                        shape=self._capacity_shape,
                        dtype=self._dtype,
                        mode=self._mode)

    def flush(self):
        self.data.flush()
        self._truncate_if_needed()

    def _shape_bytes(self, shape, dtype_bytes):
        return reduce((lambda x, y: x * y), shape) * dtype_bytes

    def _truncate_if_needed(self):
        fd = os.open(self._fpath, os.O_RDWR|os.O_CREAT)
        dtype_bytes = np.dtype(self._dtype).itemsize
        nbytes = self._shape_bytes(self._shape, dtype_bytes)
        os.ftruncate(fd, nbytes)
        self._create_ndarray()

    @property
    def shape(self):
        return self._shape

    @property
    def capacity(self):
        return self._capacity_shape

    @property
    def dtype(self):
        return self._dtype

    def __getitem__(self, idx):
        return self.data[idx]

    def __setitem__(self, idx, v):
        self.data[idx] = v

    def __len__(self):
        return self._shape[0]

    def _incr_shape(self, shape, n):
        _s = list(shape)
        _s[0] += n
        return tuple(_s)

    def append(self, v):
        '''
        >>> import numpy as np
        >>> da = DiskArray('/tmp/test.array', shape=(0, 3), growby=3, dtype=np.float32)
        >>> print(da[:])
        []
        >>> data = np.array([[2,3,4], [1, 2, 3]])
        >>> da.append(data[0])
        >>> print(da[:])
        [[ 2.  3.  4.]
         [ 0.  0.  0.]
         [ 0.  0.  0.]]
        '''

        # FIXME: for now we only support
        # append along axis 0 and only
        # for 1d and 2d arrays

        # FIXME: for now we only support
        # appending one item at a time

        nrows = self._shape[0]
        nrows_capacity = self._capacity_shape[0]

        if nrows == nrows_capacity:
            self._capacity_shape = self._incr_shape(self._capacity_shape, self._growby)
            self._update_ndarray()

        shapelen = len(self._shape)

        if shapelen not in (1, 2):
            raise AppendNotSupported(shapelen)

        self.data[nrows] = v
        self._shape = self._incr_shape(self._shape, 1)

    def extend(self, v):
        '''
        >>> import numpy as np
        >>> da = DiskArray('/tmp/test.array', shape=(0, 3), capacity=(10, 3), dtype=np.float32)
        >>> print(da[:])
	[[ 2.  3.  4.]
	 [ 0.  0.  0.]
	 [ 0.  0.  0.]
	 [ 0.  0.  0.]
	 [ 0.  0.  0.]
	 [ 0.  0.  0.]
	 [ 0.  0.  0.]
	 [ 0.  0.  0.]
	 [ 0.  0.  0.]
	 [ 0.  0.  0.]]
        >>> data = np.array([[2,3,4], [1, 2, 3]])
        >>> da.extend(data)
        >>> print(da[:])
	[[ 2.  3.  4.]
	 [ 1.  2.  3.]
	 [ 0.  0.  0.]
	 [ 0.  0.  0.]
	 [ 0.  0.  0.]
	 [ 0.  0.  0.]
	 [ 0.  0.  0.]
	 [ 0.  0.  0.]
	 [ 0.  0.  0.]
	 [ 0.  0.  0.]]
        >>> os.remove('/tmp/test.array')
        '''

        nrows = self._shape[0]
        nrows_capacity = self._capacity_shape[0]
        remaining_capacity = nrows_capacity - nrows

        if remaining_capacity < len(v):
            diff = len(v) - remaining_capacity
            self._capacity_shape = self._incr_shape(self._capacity_shape, diff)
            self._update_ndarray()

        self.data[nrows:nrows+len(v)] = v
        self._shape = self._incr_shape(self._shape, len(v))

    def grow(self, n):
        # FIXME: code
        pass

    def truncate(self, n):
        # FIXME: code
        pass

    def destroy(self):
        self.data = None
        os.remove(self._fpath)
