#!/usr/bin/env python3

# In a professional environment I would obviously use argparse or docopt to do this.

import sys

def usage(script_name):
    print(f"usage: {script_name} [-h] [-t {{titi,toto,tata}}]")

def parse_target(args):
    script_name = args[0]
    arg_position = -1

    if '-t' in args:
        arg_position = args.index('-t')

    if '--target' in args:
        arg_position = args.index('--target')

    if arg_position == -1:
        usage(args[0])
        print(f"{script_name}: error: missing argument -t/--target", file=sys.stderr)
        sys.exit(1)

    choice = args[arg_position + 1]

    if choice not in ["titi", "toto", "tata"]:
        usage(args[0])
        print(
            f"{script_name}: error: argument -t/--target: invalid choice:"
            f" '{choice}' (choose from 'titi', 'toto', 'tata')",
            file=sys.stderr
        )
        sys.exit(1)

    return choice



def main(args: list):
    script_name = args[0]

    if '-h' in args:
        usage(script_name)
        exit(0)

    choice = parse_target(args)

    if choice:
        print(f"Valid choice: {choice}")


if __name__ == '__main__':
    main(sys.argv)
