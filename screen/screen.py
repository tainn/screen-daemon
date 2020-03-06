#!/usr/bin/env python3

import sys
import os
import json
import subprocess as sp
from typing import Tuple, List


def main() -> None:
    """Sets initial data, retrieves parsed data, as well as runs respective commands"""

    raw_args = sys.argv[1:]
    commands = ['run', 'kill']
    help_ops = {'-h', '--help', 'help'}

    with open('daemons.json', 'r') as jf:
        daemons = json.load(jf)

    command, args = parse_args(raw_args, commands, help_ops, daemons)

    if command == 'run':
        run(daemons, args)
    else:
        kill(daemons, args)

    print('\nCompleted!')


def parse_args(raw_args: list, commands: list, help_ops: set, daemons: dict) -> Tuple[str, List[str]]:
    """Checks passed data and retuns the parsed command and arguments"""

    if not raw_args or set(raw_args).intersection(help_ops):
        format_help(daemons)

    if len(raw_args) != len(set(raw_args)):
        sys.exit('Repeated arguments')

    if raw_args[0] not in commands:
        sys.exit('Command <run/kill> not given')

    command, *args = raw_args

    if not args:
        sys.exit('No arguments given')

    if len(args) != len(set(args).intersection(daemons)) and 'all' not in args:
        sys.exit('One or more invalid arguments given')

    return command, args


def format_help(daemons: dict) -> None:
    """Formats the help output message and displays it"""

    output = './screen.py <run/kill> [arguments]\n' \
             '\nList of arguments:' \
             '\nall : kills all (kill-specific)'

    for command, (_, _, name) in daemons.items():
        output += f'\n{command} : {daemons.get(command).get(name)}'

    sys.exit(output)


def run(daemons: dict, args: List[str]) -> None:
    """Runs the passed processes in screen"""

    for arg in args:
        os.chdir(daemons.get(arg).get('cd'))
        sp.run(f'screen -dmS {daemons.get(arg).get("execute")}', shell=True)

        pname = daemons.get(arg).get('name')
        print(f'Run {pname}')


def kill(daemons: dict, args: List[str]) -> None:
    """Kills the passed processes"""

    ls = sp.check_output(['screen -ls'], shell=True).decode('utf-8')

    for line in ls.split('\n')[1:]:

        if '/run/' in line:
            break

        pid = line.split(".")[0]
        pname = line.split(".")[1].split()[0]

        for arg in args:

            if 'all' in args or pname == daemons.get(arg).get('name'):
                sp.run([f'kill {pid}'], shell=True)
                print(f'Killed {pname}')


if __name__ == '__main__':
    main()
