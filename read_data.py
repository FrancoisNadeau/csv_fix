#!/usr/bin/env python3

import pandas as pd
from argparse import ArgumentParser
from docstring_parser import parse as ds_parse
from io import StringIO
from typing import Union
from unidecode import unidecode

from shortcuts import InptType, SepType
from get_bytes import get_bytes
from get_encoding import get_encoding
from get_has_header import get_has_header
from get_separator import get_separator


def header_type(has_hdr: bool
                ) -> Union[int, type(None)]:
    return [None if has_hdr is False else 0][0]


def read_data(inpt: InptType,
              encoding: str = None,
              sep: SepType = None,
              **kwargs
              ) -> pd.DataFrame:
    """
    Returns a DataFrame with contents from file, string or bytes.

    This function is useful when the data to be converted to a DataFrame
    is of unknown nature, possibly inhomogeneous or made using
    various (possibly unknown a priori) character encoding.
    The data is examined to determine it's encoding, delimiter and
    if it has a file_header. The results are passed to pandas read_fwf or
    read_csv functions according to what delimiter it has.

    Args:
        inpt : bytes, bytearray, str, os.PathLike
            The data to be read.

        encoding : str, optional
            Character encoding of the file.
            Automatically detected if not provided.

        sep : str, bytes, bytearray, optional
            Delimiter used to divide the file sections.
            Automatically detected if not provided.

    Returns: ``pandas.DataFrame``
        The data, read and parsed properly.
    """

    if kwargs is not None:
        encoding = kwargs.get('encoding', None)
        sep = kwargs.get('sep', None)
    inpt = get_bytes(inpt)
    enc = [encoding if encoding is not None else get_encoding(inpt)][0]
    sep = [sep if sep is not None else get_separator(inpt).decode(enc)][0]
    header = header_type(get_has_header(inpt))
    buff = StringIO(unidecode(inpt.decode(enc)))
    table_params = dict(filepath_or_buffer=buff, sep=sep,
                        header=header, engine='python')
    table = [pd.read_fwf(**table_params) if
             table_params['sep'] == '\s+' else
             pd.read_csv(**table_params)][0]
    table = table.dropna(axis=1, how='all')

    return table


def main():
    help_messages = [vars(param)['description'] for param in
                     vars(ds_parse(read_data.__doc__))['meta']]

    parser = ArgumentParser(prog='read_data',
                            usage=read_data.__doc__,
                            description=read_data.__doc__.splitlines()[0])

    parser.add_argument('inpt', nargs=1, type=InptType,
                        help=help_messages[0])
    parser.add_argument('-e', '--encoding', dest='encoding',
                        nargs='?', help=help_messages[1])
    parser.add_argument('-s', '--sep', dest='sep',
                        type=SepType, nargs='?',
                        help=help_messages[2])

    args = parser.parse_args()
    read_data(args.inpt[0], args.encoding, args.sep)


if __name__ == '__main__':
    main()
