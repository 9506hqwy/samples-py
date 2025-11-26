"""Rich Live Package."""

import asyncio

from rich.console import RenderableType
from rich.panel import Panel

from rich.live import Live


def simple() -> None:
    """テキストを更新する."""
    asyncio.run(_simple_async())


def alt() -> None:
    """Alternate Screen を設定する."""
    asyncio.run(_alt())


def iter_render() -> None:
    """表示内容をイテレーションする."""
    asyncio.run(_iter())


async def _simple_async() -> None:
    # screen: Alternate Screen (False)。
    # auto_refresh: 自動更新する(True)。
    # refresh_per_second: 自動更新の間隔(4/s)。
    # transient: 完了したあとも表示を消す(False)。
    # redirect_stdout: 標準出力をリダイレクトする(True)。print() で表示が崩れないようにする。
    # redirect_stderr: 標準エラーをリダイレクトする(True)。print() で表示が崩れないようにする。
    with Live(Panel("count 0")) as live:
        for i in range(10):
            await asyncio.sleep(0.1)
            live.update(Panel(f"count {i + 1}"))


async def _alt() -> None:
    # screen を設定すると暗黙的に transient=True が設定される。
    # 画面が開始前にクリアされ、完了後に復元される。
    with Live(Panel("count 0"), screen=True) as live:
        for i in range(10):
            await asyncio.sleep(0.1)
            live.update(Panel(f"count {i + 1}"))


async def _iter() -> None:
    # refresh ごとに実行される。
    i = 0

    def renderables() -> RenderableType:
        nonlocal i
        i += 1
        return Panel(f"count {i + 1}")

    with Live(Panel("count 0"), get_renderable=renderables):
        await asyncio.sleep(1)
