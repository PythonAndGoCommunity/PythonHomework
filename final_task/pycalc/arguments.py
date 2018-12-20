"""
This module will parse command line arguments
"""
import argparse


def parse_arguments():
    """
    Parse command line arguments
    :return: command line arguments
    """
    parser = argparse.ArgumentParser(
        description='Pure-python command-line calculator.')
    parser.add_argument('EXPRESSION', help='expression string to evaluate')
    return parser.parse_args()
