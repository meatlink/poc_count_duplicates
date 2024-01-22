import numpy as np
import pandas as pd  # type: ignore
import pytest

from duplicates import count_duplicates

TEST_DF = pd.DataFrame(
    data=[
        ["A", "a", "x", 1],
        ["A", "b", "x", 1],
        ["A", "c", "x", 1],
        ["B", "a", "x", 1],
        ["B", "b", "x", 1],
        ["B", "c", "x", 1],
        ["A", "a", "y", 1],
        ["A", np.nan, "y", 1],
        ["A", np.nan, "x", 1],
    ],
    columns=["col_1", "col_2", "col_3", "col_4"],
)


@pytest.mark.parametrize(
    "columns,expected_count,expected_samples",
    [
        (["col_1"], 9, [["A", 6], ["B", 3]]),
        (["col_1", "col_2"], 4, [["A", "a", 2], ["A", None, 2]]),
        (["col_1", "col_2", "col_3"], 0, []),
        (["col_1", "col_1", "col_2"], 4, [["A", "A", "a", 2], ["A", "A", None, 2]]),
    ],
)
def test_count(
    columns: list[str], expected_count: int, expected_samples: list[int | str | None]
) -> None:
    result = count_duplicates(TEST_DF, columns)
    samples = result["samples"].replace(np.nan, None).values.tolist()
    assert result["count"] == expected_count
    assert samples == expected_samples
