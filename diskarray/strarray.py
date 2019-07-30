from logging import Logger

import numpy as np

from .vararray import DiskVarArray


class DiskStringArray(DiskVarArray):
    # Index to word
    def __init__(self, dpath, mode="r+", growby=DiskVarArray.GROWBY, log=Logger):
        super(DiskStringArray, self).__init__(
            dpath,
            dtype=np.uint8,
            dtype_index=np.uint64,
            mode=mode,
            growby=growby,
            log=log,
        )

    def __getitem__(self, idx):
        data = super(DiskStringArray, self).__getitem__(idx)
        return data.tostring()

    def append(self, v):
        v = np.array(list(v), dtype=np.uint8)
        return super(DiskStringArray, self).append(v)

    def extend(self, v):
        v = [np.array(list(x), dtype=np.uint8) for x in v]
        return super(DiskStringArray, self).extend(v)
