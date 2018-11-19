import argparse
import importlib
import sys

from .calculator import CONSTANTS, FUNCS, PREFIX, Calculator


def parse_args():
    """Parse an arguments from command line"""
    parser = argparse.ArgumentParser(
        description='Pure-python command-line calculator')
    parser.add_argument(
        'expression',
        metavar='EXPRESSION',
        help='expression string to evaluate')
    parser.add_argument(
        '-m', '--use-modules',
        metavar='MODULE',
        required=False,
        default=None,
        nargs='+',
        help='additional modules to use'
    )
    return parser.parse_args()


def import_modules():
    """Import modules provided by --use-modules arg im command line"""
    args = parse_args()
    if args.use_modules:
        for m in args.use_modules:
            try:
                module = importlib.import_module(m)
            except (ModuleNotFoundError):
                print('"{}" module not found'.format(m))
                continue
            for k, v in module.__dict__.items():
                if k.startswith('__'):
                    continue
                FUNCS.update({k: v}) if callable(
                    getattr(module, k)) else CONSTANTS.update({k: v})
                PREFIX.append(k)


def main():
    import_modules()
    try:
        print(Calculator(parse_args().expression).calc())
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
