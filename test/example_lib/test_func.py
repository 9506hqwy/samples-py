from pytest_benchmark.fixture import BenchmarkFixture

from example_lib.func import (
    add,
    sub,
)


def test_add() -> None:
    ret = 3
    assert add(2, 1) == ret


def test_sub() -> None:
    ret = 1
    assert sub(2, 1) == ret


def test_add_bench(benchmark: BenchmarkFixture) -> None:  # pragma: no cover
    ret = 3
    assert benchmark(add, 2, 1) == ret


def test_sub_benchmark(benchmark: BenchmarkFixture) -> None:  # pragma: no cover
    ret = 1
    assert benchmark(sub, 2, 1) == ret
