# hoverbotpy

Here lies all the software for running on the Raspberry Pi.

This is not packagable as a module yet, although perhaps it might be helpful to
make it one in the future (would need to change how we manage API keys). It is
just easier to develop it like this for now.

# Dependencies

Requires Python 3.9 or newer. The latest Raspbian has 3.9.

If you must, there is a makefile for the team member who wanted one. You can
install dependencies using make if you so choose.

## Python and Pip in a virtual env

Recommended. Also required for the Discord bot.

There is a makefile target: `venv`. It calls the script `setup-env.sh`. You can
also just call that.

`setup-env.sh` creates a virtual environment, installs dependencies and
activates it.

## System

Assumes Raspbian.

This installs the dependencies with the system package manager.

There is a makefile target: `dependencies_system`. You can also run

```
sudo apt install rpi.gpio python3-rpi.gpio python3-gpiozero
```

Note, that if you are using a virtual environment and pip, this is redundant.
