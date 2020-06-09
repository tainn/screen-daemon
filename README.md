# screen-daemon
![Version](https://img.shields.io/badge/version-v1.0-blue)
![License](https://img.shields.io/badge/license-GPLv3-orange)

Utility for simplified running of pre-specified processes as daemons through the `GNU Screen`.

## Usage
Processes should be specified separately in a local `daemons.json` file. `daemons.json` should be located in the same directory as the executable.

## Form
The `daemons.json` should have the following form, each entry being a separate dictionary, where `cd`, `execute` and `name` are required fixed key strings:
```json
{
  "command_1": {
    "cd": "/path/to/dir",
    "execute": "executable arguments",
    "name": "name"
  },
  "command_2": {
    "cd": "/path/to/dir",
    "execute": "executable arguments",
    "name": "name"
  }
}
```
The keys `command` can be passed as arguments when run from the terminal in order to run those specific processes. The value `name` represents the name of the daemon as marked by `GNU Screen`.

## Run
```sh
cd /path/to/screen

chmod +x ./screen.py

./screen.py <run/kill> <arguments>
```
