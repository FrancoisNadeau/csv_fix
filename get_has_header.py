#!/usr/bin/env python3

from io import BytesIO
from typing import Union

import pandas as pd
from argparse import ArgumentParser
from unidecode import unidecode

from shortcuts import get_desc, InptType
from get_bytes import get_bytes
from get_encoding import get_encoding


def get_has_header(inpt: Union[InptType, pd.DataFrame],
                   encoding: str = None
                   ) -> bool:
    """
    Returns True if 1st line of inpt is a header line.

    Args:
        inpt: Bytes, string, file path, in-memory buffer
              Object to inspect
            - See help(get_bytes)
        encoding: bool, optional
                  Character encoding of the object to inspect

    Returns: bool
             True if the object's first row is a header, otherwise False
    """

    if isinstance(inpt, pd.DataFrame):
        inpt = unidecode(inpt.to_csv(encoding='UTF-8-SIG', sep='\t')).encode()
    inpt = get_bytes(inpt)
    encoding = encoding if encoding is not None else get_encoding(inpt)
    got_hdr = [bool(BytesIO(inpt).read(1)
               not in bytes(".-0123456789", encoding))
               if len(inpt.splitlines()) > 1 else False][0]

    return got_hdr


def main():
    desc, help_msgs = get_desc(function_name=get_has_header)

    parser = ArgumentParser(prog='get_has_header', usage=desc,
                            description=desc.splitlines()[0])
    parser.add_argument('inpt', nargs=1, type=Union[InptType, pd.DataFrame],
                        help=help_msgs[0])
    parser.add_argument('-e', '--encoding', dest='encoding',
                        nargs='?', help=help_msgs[1])

    args = parser.parse_args()
    get_has_header(args.inpt[0], args.encoding)


if __name__ == '__main__':
    main()
