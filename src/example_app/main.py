"""Example application entry point."""

from example_lib.func import add


def main() -> None:
    """Execute entry point for example-app."""
    i = add(1, 2)
    print(f"Result: {i}")


if __name__ == "__main__":  # pragma: no cover
    main()
