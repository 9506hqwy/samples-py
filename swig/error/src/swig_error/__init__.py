"""SWIG Error Package."""

from . import error  # type: ignore[attr-defined]


def error0() -> None:
    """正常に終了する場合."""
    ret = error.error0(0)
    print(ret)


def error1() -> None:
    """RuntimeError を raise する場合.

    RuntimeError の引数に文字列を設定した。
    """
    try:
        error.error0(1)
    except RuntimeError as e:
        _inspect_exception(e)


def error2() -> None:
    """RuntimeError を raise する場合.

    RuntimeError の引数に error0 の引数を設定した。
    """
    try:
        error.error0(2)
    except RuntimeError as e:
        _inspect_exception(e)


def error3() -> None:
    """ユーザ定義例外を raise する場合.

    例外の引数に error0 の引数を設定した。
    """
    try:
        error.error0(3)
    except error.Error as e:
        _inspect_exception(e)


def _inspect_exception(exc: Exception) -> None:
    print(f"Inspecting exceptions: {exc}")
    for name in dir(exc):
        value = getattr(exc, name)
        print(f"{name}: {value}")


if __name__ == "__main__":
    error0()
    error1()
    error2()
    error3()
