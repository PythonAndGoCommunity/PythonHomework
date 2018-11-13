#!/usr/bin/env python3
"""Main module, that takes the command line argument and sends it on its way to verify and calculate."""
import sys
import parse
import compexp


def main():
    """Main function of our python calculator"""
    args = sys.argv[1:]
    expression = parse.parse_argument(args)
    if expression == "":
        print("ERROR: empty string cannot be passed as argument.")
        sys.exit(1)
    answer = compexp.check_for_comp(expression)
    if type(answer) == str:
        print(answer)
        sys.exit(1)
    print(answer)


if __name__ == "__main__":
    main()
