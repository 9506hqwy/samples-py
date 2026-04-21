"""Error module."""


class GroongaError(Exception):
    """General error."""

    pass


class NotFoundError(Exception):
    """Not found error."""

    pass


class ColumnNotFoundError(NotFoundError):
    """Column not found error."""

    pass


class TableNotFoundError(NotFoundError):
    """Table not found error."""

    pass
