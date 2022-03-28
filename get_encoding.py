#!/usr/bin/env python3

import sys
from collections import Counter

import chardet
from argparse import ArgumentParser

from shortcuts import get_desc, InptType
from get_bytes import get_bytes


def get_most_common_enc(inpt: InptType) -> str:
    """
    Returns most common line-wise character encoding.
    """

    inpt = get_bytes(inpt)
    encodings = tuple(chardet.detect(line)['encoding']
                      for line in inpt.splitlines(keepends=True))
    result = tuple(dict(Counter(encodings).most_common(1)).keys())[0]
    if result == 'ascii':
        result = 'UTF-8'
    return result


def get_inc_enc(inpt: InptType) -> str:
    """
    Returns char encoding using chardet.UniversalDetector.
    """

    inpt = get_bytes(inpt)
    detector = chardet.UniversalDetector()
    checkups = (bool(vars(detector)['done'] is True),
                detector.result is not None)
    for line in inpt.splitlines():
        detector.feed(line)
        if all(checkups):
            break
        detector.close()
        results = detector.result
        if results['encoding'] == 'ascii':
            results.update({'encoding': 'UTF-8'})
        return results['encoding']


def get_encoding(inpt: InptType) -> str:
    """
    Tries several times to detect char encoding.
    """

    inpt = get_bytes(inpt)
    try:
        result = sys.getdefaultencoding()
        inpt.decode(result)
    except (UnicodeDecodeError, TypeError):
        result = get_most_common_enc(inpt)
        try:
            inpt.decode(result)
        except (UnicodeDecodeError, TypeError):
            result = chardet.detect(inpt)['encoding']
            try:
                inpt.decode(result)
            except (UnicodeDecodeError, TypeError):
                result = get_inc_enc(inpt)

    return result


def main():
    desc, help_msgs = get_desc('get_encoding')
    parser = ArgumentParser(prog='get_encoding',
                            usage=desc,
                            description=desc.splitlines()[0])
    parser.add_argument('inpt', nargs=1, type=InptType)

    args = parser.parse_args()
    get_encoding(args.inpt[0])


if __name__ == '__main__':
    main()
