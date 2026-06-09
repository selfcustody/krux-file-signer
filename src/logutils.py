"""
logutils.py

Logging setup for ksigner. Call `configure_logging()` once at start-up,
then use `logging.getLogger(__name__)` in each module.
"""

import logging
import time


def now() -> str:
    """Return the current time formatted for interactive prompts."""
    return time.strftime("%X %x %Z")


def configure_logging(verbose: bool = False):
    """
    Send timestamped logs to the console.

    INFO is shown by default; DEBUG (the verbose detail) is shown when
    `verbose` is True.
    """
    logging.basicConfig(
        format="[%(asctime)s] %(message)s",
        datefmt="%X %x %Z",
        level=logging.DEBUG if verbose else logging.INFO,
    )
