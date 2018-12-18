import argparse
from calc.main_functions import reduction_expression, check_compared


def main():
    try:
        parser = argparse.ArgumentParser(description='Takes mathematical expression')
        parser.add_argument('string')
        s = parser.parse_args().string
        composition = reduction_expression(s)
        print(check_compared(composition))
    except Exception as e:
        print('ERROR: ', e)
