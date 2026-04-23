#!/usr/bin/env python
"""Index and query text."""

import os
import sys
from argparse import Namespace
from pathlib import Path
from typing import cast

from ctypes_groonga import (
    Context,
    Groonga,
    Table,
)
from ctypes_groonga.table import (
    create_table,
    list_tables,
)


def _index_source(path: Path, directory: Path) -> int:

    def index_content(table: Table, path: Path, i: int, line: str) -> int:
        content = line.rstrip("\n")
        if len(content.strip()) == 0:
            return 0

        data = {
            "path": str(path),
            "line": i,
            "content": content,
        }

        return table.load(
            values=[
                data,
            ]
        )

    def scan_file(table: Table, path: Path) -> int:
        if path.suffix != ".py":
            return 0

        ret = 0
        with path.open() as f:
            for i, line in enumerate(f, start=1):
                ret += index_content(table, path, i, line)

        return ret

    def walk(table: Table) -> int:
        ret = 0
        for parent, dirs, files in os.walk(directory):
            for file in files:
                ret += scan_file(table, Path(parent) / file)

        return ret

    with Groonga() as g:
        with g.create_ctx(path) as c:
            table, _ = _setup_table(c)
            return walk(table)


def _query_source(path: Path, query: str) -> int:
    with Groonga() as g:
        with g.open_ctx(path) as c:
            tables = list_tables(c)
            table = [
                t
                for t in tables
                if t.name == "Source"  # type: ignore[attr-defined]
            ]
            _, matches = table[0].select(match_columns="content", query=query)

            for match in matches:
                print(f"{match.path}#L{match.line}:{match.content}")  # type: ignore[attr-defined]
                sys.stdout.flush()

            return len(matches)


def _setup_table(ctx: Context) -> tuple[Table, Table]:
    t = create_table(ctx, name="Source", flags="TABLE_NO_KEY")
    t.create_column(name="path", type="ShortText")
    t.create_column(name="line", type="UInt16")
    t.create_column(name="content", type="ShortText")

    i = create_table(
        ctx,
        name="Term",
        flags="TABLE_PAT_KEY",
        key_type="ShortText",
        default_tokenizer="TokenBigram",
        normalizer="NormalizerAuto",
    )
    i.create_column(
        name="source_content",
        flags="COLUMN_INDEX|WITH_POSITION",
        type=t.name,  # type: ignore[attr-defined]
        source="content",
    )

    return t, i


def _main(args: Namespace) -> int:
    d = vars(args)
    func = d.pop("func")
    path = cast(str, d.pop("path"))
    return cast(int, func(Path(path), **d))


if __name__ == "__main__":
    import sys
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("path", help="specify the database file path")

    subparser = parser.add_subparsers()

    index = subparser.add_parser("index")
    index.add_argument("directory", help="specify the directory")
    index.set_defaults(func=_index_source)

    query = subparser.add_parser("query")
    query.add_argument("query", help="specify the query")
    query.set_defaults(func=_query_source)

    args = parser.parse_args()
    sys.exit(_main(args))
