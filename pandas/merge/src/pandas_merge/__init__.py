"""pandas Merge Package."""

import pandas as pd


def left() -> None:
    """左外部結合する.

    左の DataFrame を保持して、それに一致する右の DataFrame をマージする。

    Return sample DataFrame:
      category  value1  value2
    0        A       1     5.0
    1        A       2     5.0
    2        B       3     6.0
    3        C       4     NaN
    """
    left, right = inputs()
    merged = pd.merge(left, right, how="left", on="category")
    print(merged)


def right() -> None:
    """右外部結合する.

    右の DataFrame を保持して、それに一致する左の DataFrame をマージする。

    Return sample DataFrame:
      category  value1  value2
    0        A     1.0       5
    1        A     2.0       5
    2        B     3.0       6
    3        D     NaN       7
    """
    left, right = inputs()
    merged = pd.merge(left, right, how="right", on="category")
    print(merged)


def outer() -> None:
    """外部結合する.

    左右の DataFrame を保持して、それぞれに一致する行をマージする。

    Return sample DataFrame:
      category  value1  value2
    0        A     1.0     5.0
    1        A     2.0     5.0
    2        B     3.0     6.0
    3        C     4.0     NaN
    4        D     NaN     7.0
    """
    left, right = inputs()
    merged = pd.merge(left, right, how="outer", on="category")
    print(merged)


def inner() -> None:
    """内部結合する.

    左右の共通する行のみ保持して、それぞれに一致する行をマージする。

    Return sample DataFrame:
      category  value1  value2
    0        A       1       5
    1        A       2       5
    2        B       3       6
    """
    left, right = inputs()
    merged = pd.merge(left, right, how="inner", on="category")
    print(merged)


def cross() -> None:
    """交差結合する.

    左右のすべての組み合わせを生成する。

    Return sample DataFrame:
       category_x  value1 category_y  value2
    0           A       1          A       5
    1           A       1          B       6
    2           A       1          D       7
    3           A       2          A       5
    4           A       2          B       6
    5           A       2          D       7
    6           B       3          A       5
    7           B       3          B       6
    8           B       3          D       7
    9           C       4          A       5
    10          C       4          B       6
    11          C       4          D       7
    """
    left, right = inputs()
    merged = pd.merge(left, right, how="cross")
    print(merged)


def suffixes() -> None:
    """同じ名前のカラムにサフィックスを付与する.

    Return sample DataFrame:
      category  value1_l  value1_r
    0        A       1.0       5.0
    1        A       2.0       5.0
    2        B       3.0       6.0
    3        C       4.0       NaN
    4        D       NaN       7.0
    """
    left, right = inputs()
    right = right.rename(columns={"value2": "value1"})
    merged = pd.merge(left, right, how="outer", on="category", suffixes=("_l", "_r"))
    print(merged)


def indicator() -> None:
    """マージ方法の列を追加する.

    Return sample DataFrame:
      category  value1  value2      _merge
    0        A     1.0     5.0        both
    1        A     2.0     5.0        both
    2        B     3.0     6.0        both
    3        C     4.0     NaN   left_only
    4        D     NaN     7.0  right_only
    """
    left, right = inputs()
    merged = pd.merge(left, right, how="outer", indicator=True)
    print(merged)


def inputs() -> tuple[pd.DataFrame, pd.DataFrame]:
    """入力用の DataFrame を生成する.

    Return sample DataFrame:
      category  value1
    0        A       1
    1        A       2
    2        B       3
    3        C       4

      category  value1
    0        A       5
    1        B       6
    2        D       7
    """
    left = pd.DataFrame([("A", 1), ("A", 2), ("B", 3), ("C", 4)], columns=["category", "value1"])
    right = pd.DataFrame([("A", 5), ("B", 6), ("D", 7)], columns=["category", "value2"])

    return left, right
