"""Database table module."""

import json
from typing import Any, cast

from . import error, util
from .column import Column
from .groonga import Context
from .record import Record

_column_create_param_keys: set[str] = set(
    [
        "name",
        "flags",
        "type",
        "source",
        "path",
        "generator",
        "progress_log_level",
    ]
)

_load_param_keys: set[str] = set(
    [
        "values",
        "table",
        "columns",
        "ifexists",
        "input_type",
        "each",
        "output_ids",
        "output_errors",
        "lock_table",
    ]
)

_table_create_param_keys: set[str] = set(
    [
        "name",
        "flags",
        "key_type",
        "value_type",
        "default_tokenizer",
        "normalizer",
        "token_filters",
        "path",
    ]
)


class Table:
    """Database table."""

    def __init__(self, ctx: Context, **kwargs: Any) -> None:  # noqa: ANN401
        """Initialize."""
        self.ctx = ctx
        self.__dict__.update(kwargs)
        self.columns = self.list_columns()

    @property
    def count(self) -> int:
        """Count records."""
        num, _ = self.select(limit=0)
        return num

    def clear(self) -> None:
        """Delete all records."""
        _, records = self.select(limit=self.count)
        for r in records:
            self.delete(id=r.id)  # type: ignore[attr-defined]

    def delete(self, **kwargs: Any) -> bool:  # noqa: ANN401
        """Delete matching records."""
        base_opt = {"table": self.name}  # type: ignore[attr-defined]
        opt = kwargs | base_opt

        cmd = f"delete {util.create_cmd(opt)}"

        self.ctx.send(cmd)
        return cast(bool, self.ctx.recv())

    def load(self, **kwargs: Any) -> int:  # noqa: ANN401
        """Insert records."""
        values = kwargs.get("values", None)

        base_opt = {
            "table": self.name,  # type: ignore[attr-defined]
            "values": json.dumps(values),
        }
        opt = kwargs | base_opt

        opt = util.filter_opt(_load_param_keys, **opt)
        cmd = f"load {util.create_cmd(opt)}"

        self.ctx.send(cmd)
        return cast(int, self.ctx.recv())

    def select(self, **kwargs: Any) -> tuple[int, list[Record]]:  # noqa: ANN401
        """Get matching records."""
        limit = kwargs.get("limit", -1)
        if limit == -1:
            limit = self.count

        base_opt = {
            "limit": limit,
            "table": self.name,  # type: ignore[attr-defined]
        }
        opt = kwargs | base_opt

        cmd = f"select {util.create_cmd(opt)}"

        self.ctx.send(cmd)
        ret = cast(list, self.ctx.recv())

        result = ret[0]
        hits = result[0][0]
        info = result[1]
        records = result[2:]

        if not records:
            return hits, []

        keys = [i[0] for i in info]
        return hits, [Record(**r._asdict()) for r in util.mknamedtuple("Record", keys, records)]

    def create_column(self, **kwargs: str) -> Column:
        """Create and add column to table."""
        opt = util.filter_opt(_column_create_param_keys, **kwargs)
        cmd = f"column_create --table {self.name} {util.create_cmd(opt)}"  # type: ignore[attr-defined]

        self.ctx.send(cmd)
        self.ctx.recv()

        name = kwargs.get("name", None)

        columns = self.list_columns()
        if columns is None:
            raise error.ColumnNotFoundError(name)

        column = [c for c in columns if c.name == name]  # type: ignore[attr-defined]
        if len(column) != 1:
            raise error.ColumnNotFoundError(name)

        self.columns.append(column[0])
        return column[0]

    def list_columns(self) -> list[Column]:
        """List columns in table."""
        cmd = f"column_list --table {self.name}"  # type: ignore[attr-defined]

        self.ctx.send(cmd)
        ret = cast(list, self.ctx.recv())

        info = ret[0]
        columns = ret[1:]

        if not columns:
            return []

        keys = [i[0] for i in info]
        return [Column(**c._asdict()) for c in util.mknamedtuple("Column", keys, columns)]


def create_table(ctx: Context, **kwargs: str) -> Table:
    """Create new table."""
    opt = util.filter_opt(_table_create_param_keys, **kwargs)
    cmd = f"table_create {util.create_cmd(opt)}"

    ctx.send(cmd)
    ctx.recv()

    name = kwargs.get("name", None)

    tables = list_tables(ctx)
    if tables is None:
        raise error.TableNotFoundError(name)

    table = [t for t in tables if t.name == name]  # type: ignore[attr-defined]
    if len(table) != 1:
        raise error.TableNotFoundError(name)

    return table[0]


def list_tables(ctx: Context) -> list[Table]:
    """List tables in database."""
    cmd = "table_list"

    ctx.send(cmd)
    ret = cast(list, ctx.recv())

    info = ret[0]
    tables = ret[1:]

    if not tables:
        return []

    keys = [i[0] for i in info]
    return [Table(ctx, **t._asdict()) for t in util.mknamedtuple("Table", keys, tables)]
