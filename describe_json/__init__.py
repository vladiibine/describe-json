#!/usr/bin/env python
"""
Main function: get_struct
Usage:
echo '{"some_json": "string"}' | describe_json.py



"""
from __future__ import print_function, unicode_literals
import json
import sys
import argparse
import random
from hashlib import md5


MAX_STRING_DEFAULT = 10
MAX_ARRAY_DEFAULT = 1
RANDOMIZE_DEFAULT = False


def is_basestring(obj):
    """Provides py2/3 compat"""
    try:
        return isinstance(obj, basestring)
    except NameError:
        return isinstance(obj, str)


class JSONDescriber(object):
    def __init__(
            self,
            max_array_size=MAX_ARRAY_DEFAULT,
            max_string_size=MAX_STRING_DEFAULT,
            randomize=RANDOMIZE_DEFAULT
    ):
        self.max_array_size = max_array_size
        self.max_string_size = max_string_size
        self.randomize = randomize

    def get_struct(self, obj):
        """Entrypoint. Use this function with any object that was json.load-ed

        >>> JSONDescriber().get_struct(0)
        0

        >>> JSONDescriber().get_struct([1, 2, 3])
        ['length: 3; example:', 1]

        >>> JSONDescriber().get_struct({'a': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'})
        {'a': 'aaaaaaaaaa... len: 44, md5: 4c3c7c067634daec9716a80ea886d123'}

        >>> JSONDescriber().get_struct({'a':['aaaaaaaaaaaa0000000000000000']})
        {'a': ['aaaaaaaaaa... len: 28, md5: 27612b87a33aa5280b0cd000b3e75e4d']}

        The "== {}" syntax is because dict keys are not necessarily ordered.
        This makes the test pass on all 2.7+/3+ versions of python
        >>> JSONDescriber().get_struct({'a': 'b', 'c': 'd'}) == \
        {'a': 'b', 'c': 'd'}
        True

        The "== {}" syntax is because dict keys are not necessarily ordered.
        This makes the test pass on all 2.7+/3+ versions of python
        >>> JSONDescriber().get_struct({'c': 'd', 'e': [1, 2, 3]}) == \
        {'c': 'd', 'e': ['length: 3; example:', 1]}
        True

        The "== {}" syntax is because dict keys are not necessarily ordered.
        This makes the test pass on all 2.7+/3+ versions of python
        >>> JSONDescriber().get_struct({'e': [{'e': 'f', 'g': 'g', 'h': 'aaaaaaaaaaaa'}]}) == \
        {'e': [{'e': 'f', 'g': 'g', 'h': 'aaaaaaaaaa... len: 12, md5: 45e4812014d83dde5666ebdf5a8ed1ed'}]}
        True

        :param obj:
        :return:
        """
        if not isinstance(obj, (dict, list, tuple, set)):
            return self.get_scalar_struct(obj)
        elif isinstance(obj, (list, tuple, set)):
            return self.get_array_struct(obj)
        elif isinstance(obj, dict):
            return self.get_object_struct(obj)

    def get_scalar_struct(self, value):
        if is_basestring(value) and len(value) > self.max_string_size:
            return "{}... len: {}, md5: {}".format(
                value[:self.max_string_size],
                len(value),
                md5(value.encode('utf-8')).hexdigest()
            )
        return value

    def get_array_struct(self, array):
        if len(array) > self.max_array_size:
            return [
                'length: {}; example:'.format(len(array)),
                self.get_struct(random.choice(array) if self.randomize else array[0])
            ]
        else:
            return [self.get_struct(elem) for elem in array]

    def get_object_struct(self, dict_obj):
        """Transforms data deep data structures recursively, replacing lists/tuples
        with a dict describing how many elements the collection had, and outputting
        the first elem, as an example

        :param dict dict_obj:
        :return:
        """
        result = {}
        for key, value in dict_obj.items():
            result[key] = self.get_struct(value)

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
        '-a', '--max-array-size',
        help="The maximum array size that we can allow to be outputted. "
             "If the array is longer, it will be displayed as containing 2 "
             "elements: a string which displays its size, and just one of "
             "the original elements in the array",
        default=MAX_ARRAY_DEFAULT,
        type=int,
        dest='max_array_size',
    )
    parser.add_argument(
        '-s', '--max-string-size',
        help="The maximum string length that we can allow to be outputted. "
             "If the string is longer, it will be displayed shortened.",
        default=MAX_STRING_DEFAULT,
        type=int,
        dest='max_string_size',
    )
    parser.add_argument(
        '-r', '--randomize-array-member',
        help='By default, the library will display only the first member of '
             'arrays as an example. Setting this flag, will make it so a '
             'random array member is chosen',
        action='store_true',
        dest='randomize',
    )
    parser.add_argument(
        'json_string',
        help='A JSON string to parse. You can either provide this, or pipe '
             'the JSON through.',
        nargs='?'
    )

    args = parser.parse_args()

    json_describer = JSONDescriber(
        max_array_size=args.max_array_size,
        max_string_size=args.max_string_size,
        randomize=args.randomize,
    )

    if not args.file:
        if sys.stdin.isatty() and not args.json_string:
            parser.print_help()
        elif args.json_string:
            print(json.dumps(
                json_describer.get_struct(json.loads(args.json_string))))
        else:
            for line in sys.stdin:
                print(json.dumps(
                    json_describer.get_struct(json.loads(line))))
    else:
        with open(args.file) as json_file:
            print(json.dumps(
                json_describer.get_struct(json.load(json_file))))


if __name__ == '__main__':
    main()
