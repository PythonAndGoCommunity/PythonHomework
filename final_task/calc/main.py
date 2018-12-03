import argparse
from calc.main_functions import reduction_expression, compare


def main():
    try:

        parser = argparse.ArgumentParser(description='Takes mathematical expression')
        parser.add_argument('string')
        s = parser.parse_args().string
        lis = reduction_expression(s)
        print(compare(lis))

    except Exception:
        print('ERROR: Unknown exit')
        exit()
