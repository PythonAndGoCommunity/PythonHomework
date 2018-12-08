import argparse
from pycalc import PyCalc


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("EXPRESSION", help="expression string to evaluate")
    args = parser.parse_args()
    calc = PyCalc()
    result = calc.calculate(args.EXPRESSION)
    print(result)


if __name__ == '__main__':
    main()
