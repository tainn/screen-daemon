#!/usr/bin/env python3

import sys
import os
import json
import subprocess as sp
from typing import Tuple, List


def main() -> None:
    """Sets initial data, retrieves parsed data, as well as runs respective commands"""

    args = sys.argv[1:]
    commands = ['run', 'kill']
    help_flags = {'-h', '--help', 'help'}

    with open('options.json', 'r') as jf:
        options = json.load(jf)

    command, arguments = args_parse(args, commands, help_flags, options)

    if command == 'run':
        run(options, arguments)
    else:
        kill(options, arguments)

    print('\nCompleted!')


def args_parse(args: list, commands: list, help_flags: set, options: dict) -> Tuple[str, List[str]]:
    """Checks passed data and retuns the parsed command and arguments"""

    if not args or set(args).intersection(help_flags):
        return_help(options)

    if len(args) != len(set(args)):
        sys.exit('Repeated arguments')

    if args[0] not in commands:
        sys.exit('Command <run/kill> not given')

    command, *arguments = args

    if not arguments:
        sys.exit('No arguments given')

    if len(arguments) != len(set(arguments).intersection(options)) and 'all' not in arguments:
        sys.exit('One or more invalid arguments given')

    return command, arguments


def return_help(options: dict) -> None:
    """Formats the help output message and displays it"""

    output = './screen.py <run/kill> [arguments]\n'
    output += '\nList of arguments:'
    output += '\nall : kills all (kill-specific)'

    for command, (_, _, name) in options.items():
        output += f'\n{command} : {options.get(command).get(name)}'

    sys.exit(output)


def run(options: dict, arguments: List[str]) -> None:
    """Runs the passed processes"""

    for arg in arguments:
        os.chdir(options.get(arg).get('cd'))
        sp.run(f'screen -dmS {options.get(arg).get("execute")}', shell=True)

        pname = options.get(arg).get('name')
        print(f'Run {pname}')


def kill(options: dict, arguments: List[str]) -> None:
    """Kills the passed processes"""

    ls = sp.check_output(['screen -ls'], shell=True).decode('utf-8')

    for line in ls.split('\n')[1:]:

        if '/run/' in line:
            break

        pid = line.split(".")[0]
        pname = line.split(".")[1].split()[0]

        for arg in arguments:

            if 'all' in arguments or pname == options.get(arg).get('name'):
                sp.run([f'kill {pid}'], shell=True)
                print(f'Killed {pname}')


if __name__ == '__main__':
    main()
