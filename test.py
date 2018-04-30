#!/usr/bin/env python

import doctest
import unittest

from diskarray import diskarray, vararray

def suitefn():
    suite = unittest.TestSuite()
    suite.addTests(doctest.DocTestSuite(diskarray))
    suite.addTests(doctest.DocTestSuite(vararray))
    return suite

if __name__ == "__main__":
    doctest.testmod(diskarray)
    doctest.testmod(vararray)
