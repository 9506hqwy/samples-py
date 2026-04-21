"""Database column module."""

from typing import Any


class Column:
    """Database column."""

    def __init__(self, **kwargs: Any) -> None:  # noqa: ANN401
        """Initialize."""
        self.__dict__.update(kwargs)
