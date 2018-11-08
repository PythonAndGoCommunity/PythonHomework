#!/usr/bin/env python3
"""Module for processing command line argument to string"""

import argparse

parser = argparse.ArgumentParser(description="Pyre=python command-line calculator.")
parser.add_argument("Expression", action="store", nargs=1, type=str, metavar="EXPRESSION")


def parse_argument(args):
    """Parses expression from command line to string and returns it
        to our main function for following processing
    """
    parsed_exp = parser.parse_args(args)
    return parsed_exp.Expression[0]
