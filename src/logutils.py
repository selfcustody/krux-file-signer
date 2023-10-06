""" 
logutils.py

simple log utilities
"""
import time


# pylint: disable=too-few-public-methods
class Bcolors:
    """
    Simple class to manage colors in terminal
    """

    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    INFO = "\033[92m"
    WARN = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

    @staticmethod
    # pylint: disable=inconsistent-return-statements
    def build_v_type(v_type: str) -> str:
        """
        Get a type and convert into formated color
        """
        if v_type == "INFO":
            return f"{Bcolors.BOLD}{Bcolors.INFO}{v_type}{Bcolors.ENDC}"

        if v_type == "WARN":
            return f"{Bcolors.BOLD}{Bcolors.WARN}{v_type}{Bcolors.ENDC}"

        if v_type == "FAIL":
            return f"{Bcolors.BOLD}{Bcolors.FAIL}{v_type}{Bcolors.ENDC}"


def now() -> str:
    """Return some formated time"""
    return time.strftime("%X %x %Z")


def verbose_log(v_type: str, v_data: str):
    """
    Prints verbose data preceded by current time

    Example:

    ```bash
    >>> import logutils
    >>> verbose_log('Hello world')
    [ksigner 08:08:08 8/8/88 -08] Hello World

    ```
    Args:
        :param v_data
            the message to be verbose
    """
    vtype = Bcolors.build_v_type(v_type)
    print(f"[{vtype}   ] [KSigner     ] [{now()}] {v_data}")
