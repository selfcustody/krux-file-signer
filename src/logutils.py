import time

def now() -> str:
    """Return some formated time"""
    return time.strftime("%X %x %Z")


def verbose_log(v_data: str):
    """
    Prints verbose data preceded by current time

    Example:

    ```bash
    >>> import logutils
    >>> verbose_log('Hello world')
    [08:08:08 8/8/88 -08] Hello World

    ```
    Args:
        :param v_data
            the message to be verbose
    """
    print(f"[{now()}] {v_data}")
