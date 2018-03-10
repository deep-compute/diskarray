class DiskArrayException(Exception):
    pass

class AppendNotSupported(DiskArrayException):
    def __init__(self, naxes):
        self.naxes = naxes
