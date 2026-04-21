"""Groonga ctypes binding module."""

from __future__ import annotations

import json
from collections.abc import Callable
from ctypes import (
    CDLL,
    POINTER,
    Structure,
    c_char,
    c_char_p,
    c_int,
    c_ubyte,
    c_uint,
    c_void_p,
    cdll,
    string_at,
)
from ctypes.util import find_library
from pathlib import Path
from types import TracebackType
from typing import Any, Self, cast

from . import error


class GrnCtx(Structure):
    """grn_ctx."""

    # https://groonga.org/docs/reference/api/struct__grn__ctx.html
    _fields_ = [
        ("rc", c_int),
        ("flags", c_int),
        ("encoding", c_int),
        ("ntrace", c_ubyte),
        ("errlvl", c_ubyte),
        ("stat", c_ubyte),
        ("seqno", c_uint),
        ("subno", c_uint),
        ("seqno2", c_uint),
        ("errline", c_uint),
        ("user_data", c_void_p),
        ("prev", c_void_p),
        ("next", c_void_p),
        ("errfile", c_char_p),
        ("errfunc", c_char_p),
        ("impl", c_void_p),
        ("trace", c_void_p * 16),
        ("errbuf", c_char * 0x80),
    ]


c_char_pp = POINTER(c_char_p)
c_int_p = POINTER(c_int)
c_uint_p = POINTER(c_uint)
grn_ctx_p = POINTER(GrnCtx)


class Groonga:
    """Groonga binding."""

    def __init__(self, path: Path | None = None) -> None:
        """Initialize."""
        p = path
        if p is None:
            lib_path = find_library("groonga")
            if isinstance(lib_path, str):
                p = Path(lib_path)

        if p is None:
            raise error.NotFoundError("Not found groonga library.")

        self._lib = cdll.LoadLibrary(str(p))
        self._setup(self._lib)
        self._lib.grn_init()

    def __call__(self) -> CDLL:
        """Get library."""
        return self._lib

    def __enter__(self) -> Self:
        """Enter context."""
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Exit context."""
        self.fin()

    @property
    def encoding(self) -> str:
        """Get encoding."""
        code = self._lib.grn_get_default_encoding()
        raw_value: bytes = self._lib.grn_encoding_to_string(code)
        return raw_value.decode()

    @encoding.setter
    def encoding(self, value: str) -> None:
        """Set encoding."""
        raw_value = value.encode()
        code = self._lib.grn_encoding_parse(raw_value)
        self._lib.grn_set_default_encoding(code)

    @property
    def version(self) -> str:
        """Get versoin."""
        raw_version: bytes = self._lib.grn_get_version()
        return raw_version.decode(self.encoding)

    def fin(self) -> None:
        """Dispose binding."""
        self._lib.grn_fin()

    def create_ctx(self, path: Path | None, flags: int = 0) -> Context:
        """Create new database."""
        raw_path = None if path is None else bytes(path)
        ctx = self._lib.grn_ctx_open(flags).contents
        self._lib.grn_db_create(ctx, raw_path, None)
        return Context(self, ctx)

    def open_ctx(self, path: Path, flags: int = 0) -> Context:
        """Open existing database."""
        ctx = self._lib.grn_ctx_open(flags).contents
        self._lib.grn_db_open(ctx, bytes(path))
        return Context(self, ctx)

    def close_ctx(self, ctx: Context) -> None:
        """Close database."""
        db = self._lib.grn_ctx_db(ctx.ctx)
        self._lib.grn_obj_unlink(ctx.ctx, db)
        self._lib.grn_ctx_close(ctx.ctx)

    def _check_grn_ctx(self, name: str) -> Callable:
        def check[T: Any](result: T, func: Callable, arguments: tuple[Any]) -> T:
            func_name = name
            if result is None or not bool(result):
                raise Exception(f"{func_name}{arguments}")
            return result

        return check

    def _check_grn_rc(self, name: str) -> Callable:
        def check[T: Any](result: T, func: Callable, arguments: tuple[Any]) -> T:
            func_name = name
            if result != 0:
                raise Exception(f"{func_name}{arguments}")
            return result

        return check

    def _check_grn_obj(self, name: str) -> Callable:
        def check[T: Any](result: T, func: Callable, arguments: tuple[Any]) -> T:
            func_name = name
            if result is None or not bool(result):
                raise Exception(f"{func_name}{arguments}")
            return result

        return check

    def _setup(self, lib: CDLL) -> None:
        # grn_ctx_db
        lib.grn_ctx_db.restype = c_void_p
        lib.grn_ctx_db.argtypes = [
            grn_ctx_p,
        ]
        lib.grn_ctx_db.errcheck = self._check_grn_obj("grn_ctx_db")

        # grn_ctx_open
        lib.grn_ctx_open.restype = grn_ctx_p
        lib.grn_ctx_open.argtypes = [
            c_int,
        ]
        lib.grn_ctx_open.errcheck = self._check_grn_ctx("grn_ctx_open")

        # grn_ctx_recv
        lib.grn_ctx_recv.restype = c_uint
        lib.grn_ctx_recv.argtypes = [
            grn_ctx_p,
            c_char_pp,
            c_uint_p,
            c_int_p,
        ]

        # grn_ctx_send
        lib.grn_ctx_send.restype = c_uint
        lib.grn_ctx_send.argtypes = [
            grn_ctx_p,
            c_char_p,
            c_uint,
            c_int,
        ]

        # grn_ctx_close
        lib.grn_ctx_close.restype = c_int
        lib.grn_ctx_close.argtypes = [
            grn_ctx_p,
        ]
        lib.grn_ctx_close.errcheck = self._check_grn_rc("grn_ctx_close")

        # grn_db_create
        lib.grn_db_create.restype = c_void_p
        lib.grn_db_create.argtypes = [
            grn_ctx_p,
            c_char_p,
            c_void_p,
        ]
        lib.grn_db_create.errcheck = self._check_grn_obj("grn_db_create")

        # grn_db_open
        lib.grn_db_open.restype = c_void_p
        lib.grn_db_open.argtypes = [
            grn_ctx_p,
            c_char_p,
        ]
        lib.grn_db_open.errcheck = self._check_grn_obj("grn_db_open")

        # grn_encoding_parse
        lib.grn_encoding_parse.restype = c_int
        lib.grn_encoding_parse.argtypes = [
            c_char_p,
        ]

        # grn_encoding_to_string
        lib.grn_encoding_to_string.restype = c_char_p
        lib.grn_encoding_to_string.argtypes = [
            c_int,
        ]

        # grn_fin
        lib.grn_fin.restype = c_int
        lib.grn_fin.argtypes = []
        lib.grn_fin.errcheck = self._check_grn_rc("grn_fin")

        # grn_get_default_encoding
        lib.grn_get_default_encoding.restype = c_int
        lib.grn_get_default_encoding.argtypes = []

        # grn_get_version
        lib.grn_get_version.restype = c_char_p
        lib.grn_get_version.argtypes = []

        # grn_init
        lib.grn_init.restype = c_int
        lib.grn_init.argtypes = []
        lib.grn_init.errcheck = self._check_grn_rc("grn_init")

        # grn_obj_unlink
        lib.grn_obj_unlink.argtypes = [grn_ctx_p, c_void_p]

        # grn_set_default_encoding
        lib.grn_set_default_encoding.restype = c_int
        lib.grn_set_default_encoding.argtypes = [c_int]
        lib.grn_set_default_encoding.errcheck = self._check_grn_rc("grn_set_default_encoding")


class Context:
    """grn_ctx wrapper."""

    def __init__(self, groonga: Groonga, ctx: GrnCtx) -> None:
        """Initialize."""
        self.groonga = groonga
        self.ctx = ctx

    def __enter__(self) -> Self:
        """Enter context."""
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Exit context."""
        self.groonga.close_ctx(self)

    def recv(self) -> bool | int | float | str | list | dict | None:
        """Receive data from database."""
        data = c_char_p()
        data_len = c_uint()
        flags = c_int()
        self.groonga().grn_ctx_recv(self.ctx, data, data_len, flags)

        r = None
        if data_len.value != 0:
            raw = string_at(data)[0 : data_len.value]
            r = raw.decode(self.groonga.encoding)

        return None if r is None else json.loads(r)

    def send(self, data: str, flags: int = 0) -> int:
        """Send data to database."""
        d = data.encode(self.groonga.encoding)

        self.groonga().grn_ctx_send(self.ctx, d, len(d), flags)
        if self.ctx.rc != 0:
            err = self.ctx.errbuf.decode(self.groonga.encoding)
            raise error.GroongaError(err)

        return cast(int, self.ctx.rc)
