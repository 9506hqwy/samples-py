"""pandas DataFrame Package."""

import numpy as np

import pandas as pd


def condition() -> None:
    """特定の条件に基づいてデータをフィルタリングする.

    Return sample DataFrame:
                     datetime category    value1    value2
    17    2025-11-01 00:17:00        A  0.815215 -0.832090
    31    2025-11-01 00:31:00        A  0.274118  0.887702
    38    2025-11-01 00:38:00        A  0.063223  0.376759
    40    2025-11-01 00:40:00        A  1.323383  0.936980
    50    2025-11-01 00:50:00        A  1.153686  1.060394
    ...                   ...      ...       ...       ...
    43161 2025-11-30 23:21:00        A  1.394108 -0.224175
    43174 2025-11-30 23:34:00        A  0.899497  0.443974
    43179 2025-11-30 23:39:00        A  0.023941 -1.186928
    43188 2025-11-30 23:48:00        A  1.212838  1.490604
    43191 2025-11-30 23:51:00        A  0.616130 -0.340151

    [5336 rows x 4 columns]
    """
    df = inputs()
    filtered = df[(df["category"] == "A") & (df["value1"] > 0)]
    print(filtered)


def groupby_datetime() -> None:
    """日時ごとに集計を行う.

    Return sample DataFrame:
                   datetime     value1     value2
    0   2025-11-01 00:00:00  -1.017131   3.519376
    1   2025-11-01 01:00:00  11.823839   1.760430
    2   2025-11-01 02:00:00   0.403248   0.239619
    3   2025-11-01 03:00:00  -2.133738  -8.382877
    4   2025-11-01 04:00:00   4.551705   2.998731
    ..                  ...        ...        ...
    715 2025-11-30 19:00:00 -14.119703  -6.776509
    716 2025-11-30 20:00:00  -5.409287  -2.240722
    717 2025-11-30 21:00:00  -5.698107  11.181374
    718 2025-11-30 22:00:00   4.204375  -5.193350
    719 2025-11-30 23:00:00   0.020799  12.671314

    [720 rows x 3 columns]
    """
    df = inputs()
    grouping = df.groupby(
        [
            df["datetime"].dt.year,
            df["datetime"].dt.month,
            df["datetime"].dt.day,
            df["datetime"].dt.hour,
        ]
    )[["value1", "value2"]].sum()

    datetimes = [f"{year}/{month}/{day} {hour}:00:00" for year, month, day, hour in grouping.index]

    grouping = grouping.reset_index(drop=True)
    grouping.insert(0, "datetime", pd.to_datetime(pd.DataFrame(datetimes)[0]))

    print(grouping)


def groupby_value() -> None:
    """カテゴリごとに集計を行う.

    Return sample DataFrame:
                  value1      value2
    category
    A         161.857994  120.044126
    B         -59.035254  101.225279
    C          32.201511 -117.890985
    D        -189.392834   72.520751
    """
    df = inputs()
    grouping = df.groupby("category")[["value1", "value2"]].sum()
    print(grouping)


def columns() -> None:
    """カラムを指定する.

    Return sample DataFrame:
          category    value2
    0            A -1.110512
    1            A  0.344464
    2            D  1.586278
    3            A  0.130620
    4            A -1.394326
    ...        ...       ...
    43195        B -0.262207
    43196        C  1.498853
    43197        D -0.290167
    43198        A  0.521701
    43199        D -1.126017

    [43200 rows x 2 columns]
    """
    df = inputs()
    columns = df[["category", "value2"]]
    print(columns)


def column_add() -> None:
    """カラムを追加する.

    Return sample DataFrame:
                     datetime category    value1    value2  value3
    0     2025-11-01 00:00:00        B  0.634172 -0.612656   False
    1     2025-11-01 00:01:00        C  0.681919 -0.790937   False
    2     2025-11-01 00:02:00        B  0.887935 -1.691256   False
    3     2025-11-01 00:03:00        C  0.697189 -0.959113   False
    4     2025-11-01 00:04:00        A -0.588945 -0.470328   False
    ...                   ...      ...       ...       ...     ...
    43195 2025-11-30 23:55:00        A  0.594103  1.086094    True
    43196 2025-11-30 23:56:00        D -1.483207 -0.013984   False
    43197 2025-11-30 23:57:00        D  0.504227  0.712584    True
    43198 2025-11-30 23:58:00        D  0.298363  1.015071    True
    43199 2025-11-30 23:59:00        B -0.577249  1.235580    True

    [43200 rows x 5 columns]
    """
    df = inputs()
    df["value3"] = df["value2"] > 0
    print(df)


def select_name() -> None:
    """条件に一致するカラムを名前を使って取得する.

    Return sample DataFrame:
          category    value2
    26           D  2.210446
    53           C  2.306452
    56           C  3.026087
    85           B  2.393368
    96           C  2.144309
    ...        ...       ...
    42874        A  3.037504
    42949        C  2.028980
    42950        D  2.936587
    43068        C  2.380070
    43100        C  2.185119

    [1006 rows x 2 columns]
    """
    min_alue = 2
    df = inputs()
    selected = df.loc[df["value2"] > min_alue, ["category", "value2"]]
    print(selected)


def select_index() -> None:
    """行列をインデックスで指定して取得する.

    Return sample DataFrame:
      category    value1
    2        A -0.143819
    3        C -1.038361
    4        B -0.207124
    """
    df = inputs()
    selected = df.iloc[2:5, 1:3]
    print(selected)


def statistics() -> None:
    """統計を計算する.

    Return sample DataFrame:
    mean  : -0.00036254709054968245
    median: -0.0054946104799773006
                value1
    category
    A         0.001326
    B         0.005234
    C        -0.004854
    D        -0.003143
              value1
    category
    A          10839
    B          10758
    C          10789
    D          10814
    """
    df = inputs()
    print(f"mean  : {df['value1'].mean()}")
    print(f"median: {df['value1'].median()}")

    # カテゴリごと
    print(df[["category", "value1"]].groupby("category").mean())
    print(df[["category", "value1"]].groupby("category").count())


def pivot() -> None:
    """ピボットテーブルを作成する.

    Return sample DataFrame:
    category         A         B         C         D
    0              NaN       NaN  0.408456       NaN
    1              NaN -1.585959       NaN       NaN
    2              NaN -1.358051       NaN       NaN
    3              NaN       NaN -1.036442       NaN
    4              NaN       NaN  1.185330       NaN
    ...            ...       ...       ...       ...
    43195          NaN       NaN -0.074054       NaN
    43196          NaN  1.894353       NaN       NaN
    43197          NaN       NaN       NaN -1.253722
    43198     0.329036       NaN       NaN       NaN
    43199          NaN       NaN       NaN -1.648799

    [43200 rows x 4 columns]
       category    value1
    0             A       NaN
    1             A       NaN
    2             A       NaN
    3             A       NaN
    4             A       NaN
    ...         ...       ...
    172795        D       NaN
    172796        D       NaN
    172797        D -1.253722
    172798        D       NaN
    172799        D -1.648799

    [172800 rows x 2 columns]
    category          A           B           C           D
    value1   -54.867172  231.699061 -142.852596  159.383719
    category       value
    0        A  -54.867172
    1        B  231.699061
    2        C -142.852596
    3        D  159.383719
    """
    df = inputs()

    pivot = df.pivot(columns="category", values="value1")
    print(pivot)

    # pivot を元に戻す。
    print(pivot.melt(value_name="value1"))

    pivot = df.pivot_table(columns="category", values="value1", aggfunc="sum")
    print(pivot)

    # pivot を元に戻す。
    print(pivot.melt())


def inputs() -> pd.DataFrame:
    """入力用の DataFrame を生成する.

    Return sample DataFrame:
                     datetime category    value1    value2
    0     2025-11-01 00:00:00        C -0.752012 -0.329515
    1     2025-11-01 00:01:00        A -0.465088  0.790501
    2     2025-11-01 00:02:00        D -1.570195  0.372457
    3     2025-11-01 00:03:00        D -0.694230  1.261688
    4     2025-11-01 00:04:00        B  1.108603  1.565602
    ...                   ...      ...       ...       ...
    43195 2025-11-30 23:55:00        B  0.870725  0.365528
    43196 2025-11-30 23:56:00        A  0.963128  1.530863
    43197 2025-11-30 23:57:00        C  2.080614  0.631646
    43198 2025-11-30 23:58:00        A -0.113444  1.080868
    43199 2025-11-30 23:59:00        B -0.066486  1.300518

    [43200 rows x 4 columns]
    """
    datetimes = pd.date_range(
        start="2025/11/1 00:00:00",
        end="2025/11/30 23:59:00",
        freq="min",
    )

    categories = np.random.choice(["A", "B", "C", "D"], size=len(datetimes))

    values = pd.DataFrame(np.random.randn(len(datetimes), 2), columns=["value1", "value2"])

    df = pd.DataFrame(datetimes, columns=["datetime"])
    df["category"] = categories
    df = pd.concat([df, values], axis=1)

    return df
