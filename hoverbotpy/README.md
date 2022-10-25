# hoverbotpy

Python codebase for Hovercraft managed through [Poetry](https://python-poetry.org/).

Poetry lets you manage dependencies and packaging. While it is helpful for
uploading to PyPI, we will not be doing that.

# Project Structure

```
hoverbotpy
├── README.md
├── poetry.lock
├── pyproject.toml
└── src
    └── hoverbotpy
        ├── __init__.py # Makes it a package
        ├── controllers
        |   ├── __init__.py # Makes it a subpackage
        │   ├── controller_abc.py
        │   ├── # All controller modules here
        ├── drivers
        │   ├── __init__.py
        │   ├── driver_abc.py
        │   ├── # All driver modules here
        └── hoverbot_discord
            ├── __init__.py
            └── bot.py
```

If you add a new subpackage, (directory within `src/hoverbotpy/`), make sure
you create a `__init__.py` file. This file just needs to be empty, so `touch
__init__.py` will work.

# Usage

## Install Poetry

Install Poetry (for more details refer to the [documentation](https://python-poetry.org/docs/).

```
curl -sSL https://install.python-poetry.org | python3-
```

This will install poetry to `$XDG_DATA_HOME/pypoetry` (`XDG_DATA_HOME` is
`~/.local/share/`) if you do not explicitly set it.

Poetry also by default installs its run script to `~/.local/bin/`, so you will
need to make sure that is part of your `$PATH` after you install.

## Setup Virtual Environment

Poetry makes it dead easy to setup a virtual environment. It reads your
`pyproject.toml` file and installs dependencies. Additionally, if `poetry.lock`
is present, it will use the specific versions there. This ensures all
developers have identical environments.

From the directory of this readme:

```
poetry install
```

## Adding to the dependency list

You can add to the dependency list with

```
poetry add DEPENDENCY
```

This will add it to `pyproject.toml` as well as install it in your virtual
environment with `pip`. PLEASE PLEASE PLEASE add dependencies with this instead
of just installing them without adding them anywhere.

## Running Things

Assumes you are in this project directory.

You can run modules from the project virtual environment with

```
poetry run python -m mymodule # Example
poetry run python -m hoverbotpy.hoverbot_discord.bot APIKEY # Start the discord bot.
```

You can also configure specific shorthands in `pyproject.toml` in the
`[tool.poetry.scripts]` section. For example, to run the Discord bot:

```
poetry run hoverbot-discord APIKEY
```

## Referencing Other Modules Within a Module

See [documentation](https://docs.python.org/3/tutorial/modules.html#packages)
on Python project packages and modules.

This only works if your Python project is properly packaged, hence this code
restructuring.

For example, if you wanted to add a motor driver to the Discord bot, you could
use:

```python
# src/hoverbotpy/hoverbot_discord/bot.py
import hoverbotpy.drivers.driver_dummy  # Absolute path (preferred)
import ..drivers.driver_dummy           # Relative path
```

`hoverbotpy` is the name of the main package, `drivers` is a sub package,
`driver_dummy` is the module we are importing (a dummy motor driver).
