#!/usr/bin/env python3

import os
import sys

from argparse import ArgumentParser
from pathlib import Path

from .shortcuts import InptType
from .shortcuts import get_desc


def get_bytes(inpt: InptType) -> bytes:
    """
    Returns a bytes object from .'inpt', no matter what 'inpt' is.

    For ``ioBase`` classes, its contents is read.
    If the read input is ``bytes`` or ``bytearray``, it is returned as is.
    For string inputs, it is encoded using ``sys.getdefaultencoding``.
    If inpt is a string pointing to a file,
    a ``PathLike`` or ``PosixPath`` object,
    The bytes contained in that file are returned.

    Args:
        inpt: bytes, bytearray, str, os.PathLike, typing.io, object
            The object or file to convert to bytes.

    Returns: bytes
    """

    if hasattr(inpt, 'read'):
        inpt = inpt.read()
    if isinstance(inpt, (bytes, bytearray)):
        return inpt
    if os.path.isfile(inpt):
        return Path(inpt).read_bytes()
    if isinstance(inpt, str):
        return inpt.encode(sys.getdefaultencoding())
    else:
        print("unsupported input type")


def main():
    desc, help_msgs = get_desc('get_bytes')
    parser = ArgumentParser(prog='get_bytes',
                            usage=desc,
                            description=get_bytes.__doc__.splitlines()[0])
    parser.add_argument('inpt', type=InptType, nargs=1, help=help_msgs[0])
    args = parser.parse_args()
    get_bytes(args.inpt[0])


if __name__ == '__main__':
    main()
