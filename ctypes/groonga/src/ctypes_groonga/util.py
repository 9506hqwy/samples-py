"""Utility module."""

from collections import namedtuple
from typing import Any


def create_cmd(opt: dict[str, Any]) -> str:
    """Create command line."""
    args = [f"--{k} '{_escape(str(v))}'" for k, v in opt.items()]
    return " ".join(args)


def filter_opt(params: set[str], **kwargs: str) -> dict[str, str]:
    """Filter keys."""
    keys = set(kwargs.keys()) & params
    opt = {}
    for key in keys:
        opt[key] = kwargs[key]
    return opt


def mknamedtuple(name: str, keys: list[str], values: list[list[Any]]) -> list:
    """Create named tuple."""
    ks = [k.lstrip("_") for k in keys]
    t = namedtuple(name, ks)  # type: ignore[misc] # noqa: PYI024
    return [t(*v) for v in values]


def _escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace("'", "\\'")
