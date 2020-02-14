#!/usr/bin/env python3

import sys
import os
import subprocess as sp
import json
from typing import Tuple, List


def main() -> None:
    args = sys.argv[1:]
    commands = ['run', 'kill']
    help_flags = {'-h', '--help', 'help'}

    with open('options.json', 'r') as jf:
        options = json.load(jf)

    command, flags = args_parse(args, commands, help_flags, options)

    if command == 'run':
        run(options, flags)
    else:
        kill(options, flags)

    print('\nCompleted!')


def args_parse(args: list, commands: list, help_flags: set, options: dict) -> Tuple[str, List[str]]:
    if not args or set(args).intersection(help_flags):
        return_help(options)

    if len(args) != len(set(args)):
        sys.exit('Repeated arguments')

    if args[0] not in commands:
        sys.exit('Command <run/kill> not given')

    command, *flags = args

    if not flags:
        sys.exit('No arguments given')

    if len(flags) != len(set(flags).intersection(options)) and 'all' not in flags:
        sys.exit('One or more invalid arguments given')

    return command, flags


def return_help(options: dict) -> None:
    output = './screen.py <run/kill> [arguments]\n'
    output += '\nList of arguments:'
    output += '\nall : (kills all)'

    for command, (dc, screen) in options.items():
        output += f'\n{command} : {screen.split()[2]}'

    sys.exit(output)


def run(options: dict, flags: List[str]) -> None:
    for flag in flags:
        os.chdir(options.get(flag)[0])
        sp.run(options.get(flag)[1], shell=True)

        pname = options.get(flag)[1].split()[2]
        print(f'Run {pname}')


def kill(options: dict, flags: List[str]) -> None:
    ls = sp.check_output(['screen -ls'], shell=True).decode('utf-8')

    for line in ls.split('\n')[1:]:

        if '/run/' in line:
            break

        pid = line.split(".")[0]
        pname = line.split(".")[1].split()[0]

        for flag in flags:

            if 'all' in flags or pname == options.get(flag)[1].split()[2]:
                sp.run([f'kill {pid}'], shell=True)
                print(f'Killed {pname}')


if __name__ == '__main__':
    main()
