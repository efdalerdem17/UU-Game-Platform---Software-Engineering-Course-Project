# UU Game
## AI
Credit to the AI component of the code goes to Group B. Use "--player1 medium" or similar to activate it.

## Contributing
You must follow the [project guidelines](CONTRIBUTING.md) to contribute.

## Running
If you are running Windows, first following the Windows-specific instructions below first. Then, use Python 3.10 or later and run the following command in the terminal:

    python src/run.py

Or see command line arguments for choosing which player(s) is the AI and what color goes first:

    python src/run.py --help

### Windows
* Use the Windows Command Prompt (or the official [Windows Terminal from the MS store](https://apps.microsoft.com/detail/9N0DX20HK701?hl=en-US&gl=US)) because Windows VSCode terminal doesn't have mouse or proper color support
* Use Python 3.11 or earlier due to a bug in windows-curses that prevents a new terminal screen from ever being created.[^1]
* Install the windows-curses package for the version of Python you installed:

      C:/Users/User/AppData/Local/Programs/Python/Python311/python.exe -m pip install windows-curses)



[^1]: https://github.com/zephyrproject-rtos/windows-curses/issues/50

