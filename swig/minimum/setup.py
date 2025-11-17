#!/usr/bin/env python3
# /// script
# dependencies = ["setuptools>=61"]
# requires-python = ">=3.12"
# ///
"""セットアップスクリプト."""

from setuptools import Extension, setup  # type: ignore[import-untyped]

setup(
    ext_modules=[
        Extension(
            name="swig_minimum._arithmetic",
            sources=[
                "src/swig_minimum/arithmetic.c",
                "src/swig_minimum/arithmetic.i",
            ],
            depends=["src/swig_minimum/arithmetic.h"],
        ),
    ]
)
