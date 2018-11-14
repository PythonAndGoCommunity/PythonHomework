"""This module contains 'is_number' function that is used in a few other pycalc modules"""


def is_number(token):
    """Determines whether token is a number"""
    try:
        float(token)
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    print("This module contains 'is_number' function that is used in a few other pycalc modules. For example: \n")
    print("For '3' token 'is_number' returns -", is_number('3'))
    print("For '+' token 'is_number' returns -", is_number('+'))
