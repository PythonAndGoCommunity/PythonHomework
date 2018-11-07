import sys
from .pycalc import pol, shunting_yard

HELP = 'usage: pycalc [-h] EXPRESSION\nPure-python command-line calculator.\npositional arguments:' \
       '\n  EXPRESSION            expression string to evaluate'


def main():
    try:
        if sys.argv[2] == '--help':
            print(HELP)
        else:
            print(pol(shunting_yard(sys.argv[2])))
    except Exception as err:
        print('ERROR:', err)


if __name__ == '__main__':
    main()
