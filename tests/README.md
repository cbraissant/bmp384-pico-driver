# BMP384 Testing

To be able to test the device, a couple of tools need to be installed.

## MicroPython remote control: mpremote
The `mpremote` command line tool provides an integrated set of utilities to remotely interact with, manage the filesystem on, and automate a MicroPython device over a serial connection.

First, install `mpremote` on the dev computer (not on the micropython board):
```bash
$ pip install --user mpremote
```

For more information, read the [mpremote documentation](https://docs.micropython.org/en/latest/reference/mpremote.html)


The `mpremote` provides a convenient way to install packages from [micropython-lib](https://github.com/micropython/micropython-lib) using the `mip` tool

```bash
$ mpremote mip install <packages...>
```

## Unittest
To install the `unittest` framework on the micropython device, use `mpremote` and the `mip` package manager
```bash
$ mpremote mip install unittest
```

The `unittest` library will be installed on the board in `/lib/unittest/`.

For more information, read the [unittest documentation](https://docs.python.org/3/library/unittest.html) (keeping in mind that the `micropython-lib` libraries are a port of the `CPython` librairies and some discrepancies might occur)


## Runing the tests
Once `mpremote` and `unittest` are installed, run the the test file with the following command:
```bash
$ mpremote run <file.py>
```

This will execute the file directly from RAM on the device without copying it to the filesystem.