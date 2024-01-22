# Counting duplicates in Pandas DataFrame

## TL;DR

Install dependencies:

```
# python -m venv venv   # (if you need a venv)
pip install -r requirements.txt
```


Import and run in interactive shell:

```
>>> from duplicates import count_duplicates
>>> df
  col_1 col_2 col_3  col_4
0     A     a     x      1
1     A     b     x      1
2     A     c     x      1
3     B     a     x      1
4     B     b     x      1
5     B     c     x      1
6     A     a     y      1
7     A   NaN     y      1
8     A   NaN     x      1
>>> result = count_duplicates(df, ["col_1"])
>>> result["count"]
9
>>> result["samples"]
  col_1  count
0     A      6
1     B      3
```

Run tests:

```
pytest
```



## Notes

- I consider all non-unique occurrences of the same element as duplicates (vs second and further occurrences). For example: in `[1, 1, 1, 2] duplicates are [1, 1, 1], not [1, 1]`
- I think the best approach to calculate number of occurrences per record would be to use groupby - I suppose it's a good use case for it and it should be well optimised
- To calculate the total number of duplicates I use `df.duplicated(keep=False).sum()`, alternatively we can sum numbers in the result of `groupby` - in case of a large dataset with lower cardinality it might be more effective
- I suppose that we need to deal with NaN-s, so I use the `dropna=False` option. Otherwise we need to remove this option and make sure that NaN-s are also dropped when we count total number of duplicates
- I suppose we might have duplicate columns in input - I remove duplicate columns at the beginning and restore them at the end of computation
