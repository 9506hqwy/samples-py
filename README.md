# Template for Python Package

This repository provides a template for python package.

This repository uses [uv](https://github.com/astral-sh/uv) for project management.

## Prepare

1. Install [uv](https://github.com/astral-sh/uv).
2. Replace the keyword in the `pyproject.toml`.
   - `PACKAGE_NAME`: package's name
   - `PACKAGE_DESCRIPTION`: package's description
   - `USERNAME`: package's author
3. Update other content in the `pyproject.toml`.
4. Implement `src` and `test` directories.

## Development

Install require libraries.

```sh
uv sync --all-groups
```

Format, lint, check type annotation and execute test code.

```sh
uv run tox
```

### Formatting

Format source code.

```sh
uv format
```

### Linting

Lint source code.

```sh
uv run ruff check
```

### Type Checking

Check type annotation.

```sh
uv run mypy ./src
```

### Testing

Execute test code.

```sh
uv run pytest
```

### Profiling

#### CPU Profile

Run target application with profiler.

```sh
uv run python -m cProfile -o profile.pstats <target application>
```

Convert to image file from pstats file.

```sh
uv run gprof2dot -f pstats profile.pstats | dot -T png -o profile.png
```

#### Memory Profile

Run target application with profiler.

```sh
uv run python -m memray run -o profile.bin <target application>
```

Show summary.

```sh
uv run python -m memray summary profile.bin
```

### Benchmark

Run test with benchmark.

```sh
uv run pytest --benchmark-only
```

### Updating

TODO: [Upgrade dependencies in pyproject.toml (uv upgrade) #6794](https://github.com/astral-sh/uv/issues/6794)

### License Checking

Check dependency license.

```sh
uv run pip-licenses
```

### Documentation

Generate API document.

```sh
uv run sphinx-apidoc -F -f -a -H PROJECT -A AUTHOR -V VERSION -o doc src
cd doc
uv run make html
```

### Building Artifacts

Build `sdist` and `bdist`.

```sh
uv build
```
