# screen-daemon
Utility for simplified running of pre-specified processes as daemons through the `GNU Screen`.

## Usage
Processes should be specified separately in a local `daemons.json` file, located in the `data` directory.

```sh
./screen.py <run/kill> <arguments>
```

## Form
The `daemons.json` should have the following form, each entry being a separate dictionary, where `cd`, `execute` and `name` are required fixed key strings
```json
{
  "command_1": {
    "cd": "/path/to/dir",
    "execute": "executable and args",
    "name": "name"
  },
  "command_2": {
    "cd": "/path/to/dir",
    "execute": "executable and args",
    "name": "name"
  }
}
```
The keys `command` can be passed as arguments when run from the terminal in order to run those specific processes. The value `name` represents the name of the daemon as marked by `GNU Screen`.
