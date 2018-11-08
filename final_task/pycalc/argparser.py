"""
    About
"""

import argparse


class Argparser:
    """
        About
    """

    def __init__(self):
        """
            About
        """

        self._parser = argparse.ArgumentParser(
            description='Pure-python command-line calculator')

        self._parser.add_argument('-m', '--use-modules', metavar='MODULE',
                                  nargs='+', help="additional modules to use",
                                  dest="modules")

        self._parser.add_argument(metavar='EXPRESSION', type=str, nargs=1,
                                  help="expression string to evaluate",
                                  dest="expression")

    def parse_input(self):
        """
            About
        """

        args = self._parser.parse_args()
        return args
