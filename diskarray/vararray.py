import os
import shutil
from logging import Logger

import numpy as np

from .diskarray import DiskArray

class DiskVarArray(object):
    GROWBY = DiskArray.GROWBY

    def __init__(self, dpath, dtype, dtype_index=np.uint64,
            mode='r+', growby=
            GROWBY, log=Logger):
        '''
        >>> import numpy as np
        >>> from diskarray import DiskVarArray
        >>> d = DiskVarArray('/tmp/test1', dtype='uint32')
        >>> d # doctest:+ELLIPSIS
        <diskarray.vararray.DiskVarArray object at 0x...>
        '''

        self._dpath = dpath
        self._dtype = dtype
        self._dtype_index = dtype_index
        self._mode = mode
        self._growby = growby
        self.log = log

        if not os.path.exists(dpath):
            os.makedirs(dpath)

        self._data_fpath = os.path.join(dpath, 'data')
        self._data = DiskArray(self._data_fpath, dtype=dtype,
                mode=mode, growby=growby, log=log)

        self._index_fpath = os.path.join(dpath, 'index')
        self._index = DiskArray(self._index_fpath, dtype=dtype_index,
                mode=mode, growby=growby, log=log)

    def flush(self):
        self._data.flush()
        self._index.flush()

    @property
    def dtype(self):
        '''
        >>> import numpy as np
        >>> d = DiskVarArray('/tmp/test1', dtype='uint32')
        >>> d.dtype
        'uint32'
        >>> shutil.rmtree('/tmp/test1', ignore_errors=True)
        '''
        return self._dtype

    @property
    def dtype_index(self):
        '''
        >>> import numpy as np
        >>> d = DiskVarArray('/tmp/test1', dtype='uint32')
        >>> d.dtype_index
        <class 'numpy.uint64'>
        >>> shutil.rmtree('/tmp/test1', ignore_errors=True)
        '''
        return self._dtype_index

    def __getitem__(self, idx):
        '''
        >>> import numpy as np
        >>> d = DiskVarArray('/tmp/test1', dtype='uint32')
        >>> d.append([1, 2, 3, 4])
        >>> d.__getitem__(0)
        memmap([1, 2, 3, 4], dtype=uint32)
        >>> shutil.rmtree('/tmp/test1', ignore_errors=True)
        '''
        sindex = self._index[idx]

        if idx == (len(self._index) - 1):
            eindex = len(self._data)
        else:
            eindex = self._index[idx+1]

        return self._data[sindex:eindex]

    @property
    def num_elements(self):
        '''
        >>> import numpy as np
        >>> d = DiskVarArray('/tmp/test1', dtype='uint32')
        >>> d.append([1, 2, 3, 4])
        >>> d.num_elements
        4
        >>> shutil.rmtree('/tmp/test1', ignore_errors=True)
        '''
        return len(self._data)

    @property
    def num_lists(self):
        '''
        >>> import numpy as np
        >>> d = DiskVarArray('/tmp/test2', dtype='uint32')
        >>> d.append([1, 2, 3, 4])
        >>> d.num_lists
        1
        >>> d.append([5, 6, 7, 8])
        >>> d.num_lists
        2
        >>> shutil.rmtree('/tmp/test2', ignore_errors=True)
        '''
        return len(self._index)

    def append(self, v):
        '''
        >>> d = DiskVarArray('/tmp/test3', dtype='uint32')
        >>> d.append([1, 2, 3, 4])
        >>> d.__getitem__(0)
        memmap([1, 2, 3, 4], dtype=uint32)
        >>> d.append([5, 6, 7, 8])
        >>> d.__getitem__(1)
        memmap([5, 6, 7, 8], dtype=uint32)
        >>> shutil.rmtree('/tmp/test3', ignore_errors=True)
        '''
        self._index.append(len(self._data))
        self._data.extend(v)

    def extend(self, v):
        # FIXME: assert v properties
        # FIXME: can we avoid the for loop for perf?
        for index in enumerate(v):
            self.append(v[index])

    def destroy(self):
        '''
        >>> import numpy as np
        >>> d = DiskVarArray('/tmp/test4', dtype='uint32')
        >>> d.append([1, 2, 3, 4])
        >>> d.destroy # doctest:+ELLIPSIS
        <bound method DiskVarArray.destroy of <diskarray.vararray.DiskVarArray object at 0x...>>
        >>> shutil.rmtree('/tmp/test4', ignore_errors=True)
        '''

        self._data.destroy()
        self._data = None

        self._index.destroy()
        self._index = None
