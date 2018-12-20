"""
this is class for errors
"""


class Errors(Exception):

    def __init__(self, message):
        super().__init__('ERROR: ' + str(message))


"""
check that expression is not empty
"""


def is_empty(expr):
    if not expr:
        raise Errors("Your expression is empty")
