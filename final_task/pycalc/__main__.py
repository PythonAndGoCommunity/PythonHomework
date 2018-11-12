import sys
from .pycalc import postfix_eval, shunting_yard_alg

HELP = 'usage: pycalc [-h] EXPRESSION\nPure-python command-line calculator.\npositional arguments:' \
       '\n  EXPRESSION            expression string to evaluate'


def main():
    try:
        if sys.argv[2] == '--help':
            print(HELP)
        else:
            print(postfix_eval(shunting_yard_alg(sys.argv[2])))
    except Exception as err:
        print('ERROR:', err)


if __name__ == '__main__':
    main()
