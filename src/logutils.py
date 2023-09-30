""" 
logutils.py

simple log utilities
"""
import time
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    INFO = '\033[92m'
    WARN = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

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
    if (v_type == 'INFO'):
        c = f"{bcolors.BOLD}{bcolors.INFO}"
    
    if (v_type == 'WARN'):
        c = f"{bcolors.BOLD}{bcolors.WARN}"
    
    if (v_type == 'FAIL'):
        c = f"{bcolors.BOLD}{bcolors.FAIL}"

    print(f"[{c}{v_type}{bcolors.ENDC}   ] [KSigner     ] [{now()}] {v_data}")
