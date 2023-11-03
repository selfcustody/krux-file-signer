""" 
log.py

simple log utilities
"""
import logging
import sys
import time


# pylint: disable=too-few-public-methods
class Colors:
    """
    Simple class to manage ANSI colors in terminal

    see https://gist.github.com/rene-d/9e584a7dd2935d0f461904b9f2950007
    """

    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    BROWN = "\033[0;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    LIGHT_GRAY = "\033[0;37m"
    DARK_GRAY = "\033[1;30m"
    LIGHT_RED = "\033[1;31m"
    LIGHT_GREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    LIGHT_BLUE = "\033[1;34m"
    LIGHT_PURPLE = "\033[1;35m"
    LIGHT_CYAN = "\033[1;36m"
    LIGHT_WHITE = "\033[1;37m"
    BOLD = "\033[1m"
    FAINT = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    NEGATIVE = "\033[7m"
    CROSSED = "\033[9m"
    END = "\033[0m"

    # cancel SGR codes if we don't write to a terminal
    if not __import__("sys").stdout.isatty():
        for _ in dir():
            if isinstance(_, str) and _[0] != "_":
                locals()[_] = ""

    else:
        # set Windows console in VT mode
        if __import__("platform").system() == "Windows":
            kernel32 = __import__("ctypes").windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            del kernel32

    @staticmethod
    # pylint: disable=inconsistent-return-statements
    def log(level: int) -> str:
        """
        Get a level and convert into formated color.

        Supported levels are those from :mod:`logging` module

        - :const:`logging.NOTSET`
        - :const:`logging.DEBUG`
        - :const:`logging.INFO`
        - :const:`logging.WARNING`
        - :const:`logging.ERROR`
        - :const:`logging.CRITICAL`

        Parameters
        ----------
        *level* : The level from :mod:`logging`

        Returns
        -------
        *str*: The formated color with level name
        """
        if level == logging.DEBUG:
            return f"{Colors.BOLD}{Colors.BLUE}DEBUG{Colors.END}"

        if level == logging.INFO:
            return f"{Colors.BOLD}{Colors.GREEN}INFO{Colors.END}"

        if level == logging.WARNING:
            return f"{Colors.BOLD}{Colors.YELLOW}WARNING{Colors.END}"

        if level == logging.ERROR:
            return f"{Colors.BOLD}{Colors.BROWN}ERROR{Colors.END}"

        if level == logging.CRITICAL:
            return f"{Colors.BOLD}{Colors.RED}CRITICAL{Colors.END}"


def now() -> str:
    """
    Return some formated time
    """
    return time.strftime("%X %x %Z")


def build_logger(name: str, level: str):
    """
    Setup logger
    :param:
        level: could be one of `info`, `warning`,
        `error` or `critical`
    """

    # Setup logger
    numeric_level = getattr(logging, level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {numeric_level}")

    log_format = logging.Formatter("[%(levelname)s  ] [%(name)s    ] - %(message)s")
    log = logging.getLogger(name)
    log.setLevel(numeric_level)

    # writing to stdout
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(numeric_level)
    handler.setFormatter(log_format)
    log.addHandler(handler)

    return log
