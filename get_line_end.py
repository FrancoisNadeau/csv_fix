#!/usr/bin/env python3

from argparse import ArgumentParser
from collections import Counter
from typing import Union

from .get_bytes import get_bytes
from .get_encoding import get_encoding
from .shortcuts import get_desc, InptType


def get_line_end(inpt: InptType,
                 encoding: str = None
                 ) -> Union[str, bytes]:
    """
    Returns the  end-of-line indicator of a file.
    """

    datatype = type(inpt)
    inpt = get_bytes(inpt)
    encoding = [encoding if encoding is not None
                else get_encoding(inpt)][0]
    lterm = Counter(tuple(itm[0].strip(itm[1]) for itm in
                          tuple(zip(inpt.splitlines(keepends=True),
                                    inpt.splitlines())))).most_common(1)[0][0]
    if not isinstance(datatype, type(inpt)):
        lterm = lterm.decode(encoding)

    return lterm


def main():
    desc, help_msgs = get_desc('get_line_end')
    parser = ArgumentParser(prog='get_line_end',
                            usage=desc,
                            description=desc.splitlines()[0])
    parser.add_argument('inpt', nargs=1,
                        type=InptType)
    parser.add_argument(*('-e', '--encoding'), dest='encoding',
                        default=None, required=False, nargs='?',
                        help='Character encoding of the file.')

    args = parser.parse_args()
    get_line_end(args.inpt[0], args.encoding)


if __name__ == '__main__':
    main()
