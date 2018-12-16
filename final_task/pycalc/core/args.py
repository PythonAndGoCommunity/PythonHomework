"""
This module allows to work with command line arguments
"""
import argparse


def arg_parser():
    """
    Parse arguments of command line
    :return: arguments of command line
    """
    parser = argparse.ArgumentParser(description='Pure-python command-line calculator.')
    parser.add_argument('EXPRESSION', help='expression string to evaluate')
    parser.add_argument('-m', '--use-modules', nargs='+', dest='MODULE', help='additional modules to use')

    return parser.parse_args()
