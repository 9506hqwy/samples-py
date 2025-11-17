# SWIG Minimum Sample

## Build Step Manually

Move source directory.

```sh
cd src/swig_minimum
```

Generate module and wrapper code from interface file.

```sh
swig -python arithmetic.i
```

Build native wrapper code.

```sh
gcc -O2 -fPIC -c arithmetic.c arithmetic_wrap.c $(pkg-config --cflags python3)
```

Build python extension module.

```sh
gcc -shared arithmetic.o arithmetic_wrap.o -o _arithmetic.so
```

Execute.

```python
>>> import arithmetic
>>> arithmetic.add(1, 2)
3
```

## Build Step Using setuptools

Build python extension module.

```sh
uv run setup.py build_ext --inplace
```

Move source directory.

```sh
cd src/swig_minimum
```

Execute.

```python
>>> import arithmetic
>>> arithmetic.add(1, 2)
3
```

## Build Step Using uv

Build packages with extension module.

```sh
uv build .
```

## Execute Using uv

Execute directly (and build python extension module).

```sh
uv run swig-minimum
```
