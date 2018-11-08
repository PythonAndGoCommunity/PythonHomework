#!/usr/bin/env python3
"""Module for custom dictionary class with __missing__"""


class MyDict(dict):
    """Created my class for dictionary with implementation of
    __missing__
    """
    def __missing__(self, key):
        return -1
