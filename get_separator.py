#!/usr/bin/env python3

import re

import pandas as pd
from argparse import ArgumentParser

from shortcuts import InptType
from get_bytes import get_bytes
from get_encoding import get_encoding


POSSIBLES = [' ', '\t', '\x0b', '\x0c', r'\|', r'\\t', ',', ';', ':']


def get_separator(inpt: InptType,
                  encoding: str = None):
    """
    Returns field delimiter used in a tabulated data file.

    """

    datatype = type(inpt)
    inpt = get_bytes(inpt)
    encoding = [encoding if encoding is not None
                else get_encoding(inpt)][0]

    possibles = [itm.encode(encoding) for itm in POSSIBLES]
    pats = tuple(map(re.compile, possibles))
    matches = pd.DataFrame(tuple((pat.pattern, len(pat.findall(inpt)))
                                 for pat in pats),
                           dtype=bytes)
    delimiter = matches[0].where(matches[1] == matches[1].max()).dropna().tolist()[0]
    if delimiter in (' ', b' '):
        delimiter = ('\s+' if isinstance(inpt, str) and
                     len(inpt.split()) != len(inpt.split(delimiter))
                     else b'\s+')
    delimiter = (delimiter.decode(encoding) if not
                 isinstance(delimiter, datatype) else delimiter)

    return delimiter


def main():
    parser = ArgumentParser(prog='get_separator',
                            usage=get_separator.__doc__,
                            description=get_separator.__doc__.splitlines()[0])
    parser.add_argument('inpt', nargs=1,
                        type=InptType)
    parser.add_argument('-e', '--encoding', dest='encoding', nargs='?',
                        help='Character encoding of the file.')

    args = parser.parse_args()
    get_separator(args.inpt[0], args.encoding)


if __name__ == '__main__':
    main()
