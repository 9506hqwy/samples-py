"""Database record module."""

from typing import Any


class Record:
    """Database record."""

    def __init__(self, **kwargs: Any) -> None:  # noqa: ANN401
        """Initialize."""
        self.__dict__.update(kwargs)
