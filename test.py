#!/usr/bin/env python

import doctest
import unittest

from diskarray import diskarray

def suitefn():
    suite = unittest.TestSuite()
    suite.addTests(doctest.DocTestSuite(diskarray))

    return suite

if __name__ == "__main__":
    doctest.testmod(diskarray)
