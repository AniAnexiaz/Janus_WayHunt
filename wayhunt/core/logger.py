"""
Logging utility for WayHunt.
"""

import logging

# Global verbose flag — set once at startup by janus_wayhunt.py
_verbose = False


def set_verbose(value: bool) -> None:
    """Enable or disable verbose logging."""
    global _verbose
    _verbose = value


def is_verbose() -> bool:
    return _verbose


def get_logger(name: str = "WayHunt") -> logging.Logger:
    """
    Create or retrieve a configured logger.

    In non-verbose mode the logger is set to WARNING so per-item
    messages are suppressed. Progress bars handle user feedback instead.

    Args:
        name: Logger name

    Returns:
        Configured logger instance
    """

    logger = logging.getLogger(name)

    if not logger.handlers:

        handler = logging.StreamHandler()

        formatter = logging.Formatter("[%(name)s] %(message)s")

        handler.setFormatter(formatter)

        logger.addHandler(handler)

    # Respect verbose flag — reconfigure level every time so callers
    # that get the logger before set_verbose() is called still work.
    logger.setLevel(logging.DEBUG if _verbose else logging.WARNING)

    return logger
