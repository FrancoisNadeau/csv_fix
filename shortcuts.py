#!/usr/bin/env python3

from io import IOBase
from os import PathLike
from typing import Iterable, NewType, Union


InptType = NewType('InptType', Union[bytes, bytearray, str, IOBase, PathLike])
SepType = NewType('SepType', Union[str, bytes, bytearray])


def even_seq(it: Iterable) -> tuple:
    return tuple(i[1] for i in enumerate(it) if i[0] % 2 == 0)


def odd_seq(it: Iterable) -> tuple:
    return tuple(i[1] for i in enumerate(it) if i[0] % 2 != 0)


def get_desc(function_name: str) -> tuple:
    """
    Parse a function's docstring automatically

    Args:
        function_name: str
            Name of the function for which to get documentation from.

    Returns: tuple(desc, help_msgs)
        desc: str
            Concatenation of short and long function descriptions
        help_msgs: tuple(str)
            Tuple of strings representing each parameter's help message
    """

    from docstring_parser import parse as ds_parse

    parsed = ds_parse(function_name.__doc__)
    help_msgs = tuple(prm.description for prm
                      in parsed.params)
    desc = '\n'.join([parsed.short_description,
                      parsed.long_description])
    return desc, help_msgs
