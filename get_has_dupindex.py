#!/usr/bin/env python3

import sys
import pandas as pd

from argparse import ArgumentParser
from typing import Union
from unidecode import unidecode

from .get_bytes import get_bytes
from .get_encoding import get_encoding
from .get_has_header import get_has_header
from .shortcuts import even_seq, get_desc, InptType, odd_seq


def get_has_dupindex(inpt: Union[InptType, pd.DataFrame],
                     encoding: str = None
                     ) -> bool:
    """
    Returns True or False depending on if inpt has a duplicate index.

    Returns True if the first item of even and odd lines is repeated.
    Returns False otherwise or upon IndexError.
    As IndexError is raised when trying to access values by an index
    out of a sequence boundaries, IndexError indicates single-byte
    files. Being a single byte, it can't be a duplicate index.
    
    Args:
        inpt: bytes, bytearray, str, os.PathLike or pd.DataFrame
            Object to analyse.

        encoding: str, optional
            Character encoding of inpt.
    
    Returns: bool
        True if inpt has a duplicate index, otherwise False.
    """

    if isinstance(inpt, pd.DataFrame):
        enc = sys.getdefaultencoding()
        inpt = unidecode('\n'.join(['\t'.join([str(i) for i in line])
                                    for line in inpt.values])).encode(enc)
    inpt = get_bytes(inpt)
    enc = [encoding if encoding is not None
           else get_encoding(inpt)][0]
    file_header = get_has_header(inpt, encoding=enc)
    lines = [inpt.splitlines()[1:]
             if file_header else inpt.splitlines()][0]
    ev_items, od_items = even_seq(lines), odd_seq(lines)
    try:
        eve_index = [line.split()[0] for line in ev_items]
        odd_index = [line.split()[0] for line in od_items]
        val = eve_index == odd_index
    except IndexError:
        val = False

    return val


def main():
    desc, help_msgs = get_desc(get_has_dupindex.__doc__)
    parser_args = dict(usage=get_has_dupindex.__doc__,
                       description=desc)
    parser = ArgumentParser(prog='get_has_dupindex', **parser_args)

    parser.add_argument('inpt', nargs=1, type=Union[InptType, pd.DataFrame],
                        help=help_msgs[0])
    parser.add_argument('-e', '--encoding', dest='encoding',
                        nargs='?', help=help_msgs[1])

    args = parser.parse_args()
    get_has_header(args.inpt[0], args.encoding)


if __name__ == '__main__':
    main()
