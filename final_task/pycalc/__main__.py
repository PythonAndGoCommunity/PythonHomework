import sys
from .pycalc import pol, shunting_yard

HELP = 'usage: pycalc [-h] EXPRESSION\nPure-python command-line calculator.\npositional arguments:' \
       '\n  EXPRESSION            expression string to evaluate'


def main():
    print(sys.argv)
    try:
        if sys.argv[1] == '--help':
            print(HELP)
        else:
            print(pol(shunting_yard(sys.argv[1])))
    except Exception as err:
        print('ERROR:', err)


if __name__ == '__main__':
    main()
