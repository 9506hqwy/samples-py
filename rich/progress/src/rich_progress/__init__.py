"""Rich Progress Package."""

import asyncio
from io import BytesIO

from rich.table import Column

from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    track,
    wrap_file,
)


def simple() -> None:
    """既定設定の進捗率を表示する.

    タイトル、バー、進捗率、残り時間を表示する。
    """
    asyncio.run(_simple_async())


def layout() -> None:
    """表示する項目を変更する.

    スピナー、進捗率、タイトル、完了数/総数を表示する。
    """
    asyncio.run(_layout_async())


def layout_table() -> None:
    """表示する項目の幅を変更する.

    スピナー、進捗率、タイトル、完了数/総数を表示する。
    """
    asyncio.run(_layout_table_async())


def iter_range() -> None:
    """イテレーション数を進捗率に設定する."""
    asyncio.run(_iter_range())


def iter_file() -> None:
    """ファイルサイズを進捗率に設定する."""
    asyncio.run(_iter_file())


async def _simple_async() -> None:
    # auto_refresh: 自動更新する(True)。
    # refresh_per_second: 自動更新の間隔(10/s)。
    # transient: 完了したあとも進捗率の表示を消す(False)。
    # redirect_stdout: 標準出力をリダイレクトする(True)。print() で表示が崩れないようにする。
    # redirect_stderr: 標準エラーをリダイレクトする(True)。print() で表示が崩れないようにする。
    # disable: 無効化(False)。
    # expand: 画面の幅に合わせる(False)。
    with Progress() as progress:
        # start: 開始状態にする(True)。開始しなかったタスクは start_task で開始する。
        # total: 総ステップ数(100)。None にするとバーが進捗ではなくなる。
        # completed: 完了ステップ数(0)。
        # visible: 表示する(True)。
        task_id = progress.add_task("[red] Processing ...")

        # すべてのタスクが完了したかどうか
        while not progress.finished:
            await asyncio.sleep(0.1)
            # advance に指定した値は completed に追加される。
            progress.update(task_id, advance=2)


async def _layout_async() -> None:
    # add_task の引数を埋め込める。
    progress = Progress(
        SpinnerColumn(),
        BarColumn(),
        TextColumn("{task.description}"),
        MofNCompleteColumn(),
    )
    with progress:
        task_id = progress.add_task("[red] Processing ...")
        while not progress.finished:
            await asyncio.sleep(0.1)
            progress.update(task_id, advance=2)


async def _layout_table_async() -> None:
    # table_column で表示する割り合いを指定する。
    progress = Progress(
        SpinnerColumn(table_column=Column(ratio=1)),
        BarColumn(bar_width=None, table_column=Column(ratio=4)),
        TextColumn("{task.description}", table_column=Column(ratio=3)),
        MofNCompleteColumn(table_column=Column(ratio=1)),
        expand=True,
    )
    with progress:
        task_id = progress.add_task("[red] Processing ...")
        while not progress.finished:
            await asyncio.sleep(0.1)
            progress.update(task_id, advance=2)


async def _iter_range() -> None:
    # イテレーション数が進捗率になる。
    for i in track(range(10)):
        await asyncio.sleep(0.1)


async def _iter_file() -> None:
    # ファイルサイズが進捗率になる。
    file = BytesIO(b"0\n1\n2\n3\n4\n5\n6\n7\n8\n9\n")

    with wrap_file(file, 20) as f:
        while _ := f.readline():
            await asyncio.sleep(0.1)
