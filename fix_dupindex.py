#!/usr/bin/env python3

import numpy as np
import pandas as pd
from argparse import ArgumentParser
from typing import Union

from .read_data import read_data
from .shortcuts import even_seq, get_desc, InptType, odd_seq


def fix_dupindex(inpt: Union[InptType, pd.DataFrame]
                 ) -> pd.DataFrame:
    """
    Fix data with duplicate values along the x (row) axis.
    
    First, splits data into even and odd rows and creates
    two separate DataFrames from .these.
    Second, checks if any columns is exactly the same in both tables.
    Returns the concatenation along the y-axis of one of the whole
    DataFrames to the columns which were different between
    the even-rows-only and the odd-rows-only DataFrames.
    
    Args:
        inpt: bytes, bytearray, str, os.PathLike, pd.DataFrame,
              typing.io or object
            The data object to repair. If it is a DataFrame, it is
            used as is. Otherwise, <read_table> is called on inpt
            to create a DataFrame.
    
    Returns: pd.DataFrame
        The data without duplicate rows or columns.
    """
    if isinstance(inpt, pd.DataFrame):
        inpt = pd.DataFrame(inpt.values)
    else:
        inpt = pd.DataFrame(read_data(inpt).values)
    even_rows = pd.DataFrame(even_seq(list(inpt.values))).fillna("NA")
    odd_rows = pd.DataFrame(odd_seq(list(inpt.values))).fillna("NA")
    even_rows.reset_index(drop=True, inplace=True)
    odd_rows.reset_index(drop=True, inplace=True)
    even_cols, odd_cols = even_rows.T.values.tolist(), odd_rows.T.values.tolist()
    test = [odd_col[0] for odd_col in enumerate(odd_cols)
            if not odd_col[1] in even_cols]
    rprd = pd.concat([even_rows, odd_rows.iloc[:, test]],
                     axis=1).replace('NA', np.nan)
    rprd = rprd.set_axis(list(range(rprd.shape[1])), axis=1, inplace=False)

    return rprd


def main():
    desc, help_msgs = get_desc(function_name='fix_dupindex')
    parser = ArgumentParser(prog='fix_dupindex', usage=desc,
                            description=desc.splitlines()[0])
    parser.add_argument('inpt', dest='inpt',
                        type=Union[InptType, pd.DataFrame],
                        help=help_msgs[0])

    args = parser.parse_args()
    fix_dupindex(args.inpt[0])


if __name__ == '__main__':
    main()
