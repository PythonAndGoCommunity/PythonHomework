import argparse
import sys
from pycalc.importmodules import FunctionParser
from pycalc.evaluator import calculate


def get_args():
    '''This function parses and return arguments passed in'''
    parser = argparse.ArgumentParser(
        description='Script retrieves schedules from a given server')
    parser.add_argument(
        'expression',  help='')

    parser.add_argument(
         '-m', '--use-modules', nargs='+', help='', required=False)
    return parser.parse_args()


def main():
    try:
        # args = get_args()
        # parser = FunctionParser()
        # if args.use_modules:
        #     parser.parse_modules(args.use_modules)
        # parser.parse_modules(['time'])
        # result = calculate(args.expression)
        # print(calculate('time()'))
        # print(f'{result}')


    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

