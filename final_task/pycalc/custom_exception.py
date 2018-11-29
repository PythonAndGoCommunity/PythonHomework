#!/usr/bin/env python3
"""Module for my custom exception."""


class VerifyError(Exception):
    """Created a custom exception for handling errors in expression"""
    def __init__(self, msg, position=None):
        if position is not None:
            msg = "{0} Position - {1}".format(msg, position)
        else:
            super(VerifyError, self).__init__(msg)
        self.msg = msg
