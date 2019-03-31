#!/usr/bin/env python
"""
Main function: get_struct
Usage:
echo '{"some_json": "string"}' | describe_json.py



"""
from __future__ import print_function
import json
import sys
import argparse
import random


def get_struct(o, max_array_size, key, randomize):
    if not isinstance(o, (dict, list, tuple, set)):
        return get_scalar_struct(o)
    elif isinstance(o, (list, tuple, set)):
        return get_array_struct(o, max_array_size, key, randomize)
    elif isinstance(o, dict):
        return get_object_struct(o, max_array_size, key, randomize)


def get_scalar_struct(o):
    return o


def get_array_struct(o, max_array_size, key, randomize):
    if len(o) > max_array_size:
        return {
            "length": len(o),
            key: get_struct(
                random.choice(o) if randomize else o[0],
                max_array_size, key, randomize
            ) if o else None
        }
    else:
        return o


def get_object_struct(o, max_array_size, array_key, randomize):
    """Transforms data deep data structures recursively, replacing lists/tuples
    with a dict describing how many elements the collection had, and outputting
    the first elem, as an example

    >>> get_struct(0, max_array_size=1, array_key='XXX')
    ... 0

    >>> get_struct([1, 2, 3])
    ... {'length': 3, 'XXX': 1}

    >>> get_struct({'a': 'b'})
    ... {'a': 'b'}

    >>> get_struct({'a': 'b', 'c': 'd'})
    ... {'a': 'b', 'c': 'd'}

    >>> get_struct({'a': 'b', 'c': 'd', 'e': [1, 2, 3]})
    ... {'a': 'b', 'c': 'd', 'e': {'length': 3, 'XXX': 1}}

    >>> get_struct({'a': 'b', 'c': 'd', 'e': [{'a': 'b', 'c': 'd', 'e': 'f',
    ... 'g': 'g', 'h': 'hasdfadfafd'}]}, max_array_size=1, array_key='XXX')
    ... {'a': 'b', 'c': 'd', 'e': {'length': 1, 'XXX': {'a': 'b', 'c': 'd', 'e': 'f', 'g': 'g', 'h': 'hasdfadfafd'}}}

    :param o:
    :return:
    """
    result = {}
    for key, value in o.items():
        result[key] = get_struct(value, max_array_size, array_key, randomize)

    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-f', '--file',
        help="The path to a file to use instead of reading 1-line JSON strings"
             " from stdin",
        default=None,
        type=str,
    )
    parser.add_argument(
        '-m', '--max-array-size',
        help="The maximum array size that we can allow to be outputted before "
             "transforming the array to an object that just describes it",
        default=1,
        type=int,
    )
    parser.add_argument(
        '-k', '--key-for-description',
        help="When an array is transformed into an object that describes it, "
             "this will be the key used for providing an example of an "
             "element present in the former array",
        default='!!!ArrayExample',
        type=str,
    )
    parser.add_argument(
        '-r', '--randomize-array-member',
        help='By default, the library will display only the first member of '
             'arrays as an example. Setting this flag, will make it so a '
             'random array member is chosen',
        action='store_true',
    )
    parser.add_argument(
        'json_string',
        help='A JSON string to parse. You can either provide this, or pipe '
             'the JSON through.',
        nargs='?'
    )

    args = parser.parse_args()

    def get_output(json_string):  # using this instead of functools.partial
        return get_struct(
            json_string,
            key=args.key_for_description,
            max_array_size=args.max_array_size,
            randomize=args.randomize_array_member,
        )

    if not args.file:
        if sys.stdin.isatty() and not args.json_string:
            parser.print_help()
        elif args.json_string:
            print(json.dumps(
                get_output(
                    json.loads(args.json_string))))
        else:
            for line in sys.stdin:
                print(json.dumps(
                    get_output(
                        json.loads(line))))
    else:
        with open(args.file) as json_file:
            print(json.dumps(
                get_output(
                    json.load(json_file))))


if __name__ == '__main__':
    main()
