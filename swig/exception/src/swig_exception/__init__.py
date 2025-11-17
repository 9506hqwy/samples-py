"""SWIG Exception Package."""

from . import exception  # type: ignore[attr-defined]


def exception0() -> None:
    """例外指定(C++17 で廃止)がある場合.

    例外指定のクラスは Exception を継承して raise される。
    """
    exc = exception.NativeException()
    try:
        exc.exception0()
    except exception.Error0 as e:
        _inspect_exception(e)


def exception1() -> None:
    """例外指定がない場合.

    %catches 機能で例外指定と同様の処理になる。
    """
    exc = exception.NativeException()
    try:
        exc.exception1()
    except exception.Error1 as e:
        _inspect_exception(e)


def exception2() -> None:
    """例外処理のカスタマイズ.

    例外指定または %catches 機能を使用している場合に例外の対応処理を実装する。
    RuntimeError を raise する処理を実装した。
    """
    exc = exception.NativeException()
    try:
        exc.exception2()
    except RuntimeError as e:
        _inspect_exception(e)


def exception3() -> None:
    """例外処理のカスタマイズ.

    例外の検出および対応処理を実装する。
    RuntimeError を raise する処理を実装した。
    """
    exc = exception.NativeException()
    try:
        exc.exception3()
    except RuntimeError as e:
        _inspect_exception(e)


def _inspect_exception(exc: Exception) -> None:
    print(f"Inspecting exceptions: {exc}")
    for name in dir(exc):
        value = getattr(exc, name)
        print(f"{name}: {value}")


if __name__ == "__main__":
    exception0()
    exception1()
    exception2()
    exception3()
