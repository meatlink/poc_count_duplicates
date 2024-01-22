from functools import cached_property
from typing import TypedDict, cast

import pandas as pd  # type: ignore


class DuplicatesResult(TypedDict):
    """
    Result of duplicates search
    - count - total number of non-unique records
    - samples - Dataframe containing non-unique records
                and the number of occurrences
    """

    count: int
    samples: pd.DataFrame


class Counter:
    """A helper class to calculate duplicates in a DataFrame"""

    def __init__(self, df: pd.DataFrame, columns: list[str]) -> None:
        self._original_df = df
        self._columns = columns

    def count_duplicates(self) -> DuplicatesResult:
        """Count duplicates per entry and total"""
        return {
            "count": self._count,
            "samples": self._samples,
        }

    @cached_property
    def _count(self) -> int:
        """Count total number of duplicates"""
        # We can use self._samples to calculate the sum as well
        # Probably it would be a good choice in case of a larger dataset with
        # lower cardinality
        return cast(int, self._df.duplicated(keep=False).sum())

    @cached_property
    def _samples(self) -> pd.DataFrame:
        """Count duplicates and preset results in a proper form"""
        return self._counted_duplicates[self._columns + ["size"]].rename(
            columns={"size": "count"}
        )

    @cached_property
    def _counted_duplicates(self) -> pd.DataFrame:
        """Group and count non-unique entries"""
        return self._non_unique_entries.groupby(
            self._uniq_columns, dropna=False, as_index=False
        ).size()

    @cached_property
    def _non_unique_entries(self) -> pd.DataFrame:
        return self._df.loc[self._df.duplicated(keep=False)]

    @cached_property
    def _df(self) -> pd.DataFrame:
        """DataFrame with only considered columns"""
        return self._original_df[self._uniq_columns]

    @cached_property
    def _uniq_columns(self) -> list[str]:
        """List uniq columns preserving ordering"""
        # list(set(...)) might not guarantee consistent ordering, but as soon
        # as we compute it only once and then cache, it's fine - the ordering
        # will be restored later
        return list(set(self._columns))


def count_duplicates(df: pd.DataFrame, columns: list[str]) -> DuplicatesResult:
    """Count duplicates per record and total"""
    counter = Counter(df=df, columns=columns)
    return counter.count_duplicates()
