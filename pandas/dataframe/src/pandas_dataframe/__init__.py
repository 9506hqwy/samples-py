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
