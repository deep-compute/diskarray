import numpy as np
from diskarray import DiskArray

#dtype = [('x', np.uint8), ('y', np.float32, 3), ('path', 'S', 64)]
d = DiskArray('/tmp/pras.array', shape=(2, 2),dtype=np.float32)

a = np.ndarray((2, 2), dtype=np.float32)
d.extend(a)

print(d[:])
