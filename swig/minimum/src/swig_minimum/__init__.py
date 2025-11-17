"""SWIG Minimum Package."""

import sys

from . import arithmetic  # type: ignore[attr-defined]


def main() -> None:
    """拡張モジュールを実行する."""
    print(f"SWIG Minimum Sample: {sys.version}")
    print(arithmetic.add(1, 3))
    print(arithmetic.sub(7, 3))


if __name__ == "__main__":
    main()
