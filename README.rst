=============
Describe JSON
=============


.. image:: https://img.shields.io/pypi/v/describe_json.svg
        :target: https://pypi.python.org/pypi/describe_json

.. image:: https://img.shields.io/travis/vladiibine/describe_json.svg
        :target: https://travis-ci.org/vladiibine/describe_json

.. image:: https://readthedocs.org/projects/describe-json/badge/?version=latest
        :target: https://describe-json.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


Tired of looking at JSON objects that contain long arrays? Fear no more!
describe_json displays your JSON, shortening strings and arrays. It can also produce jq paths for you, so you know what part of the JSON object you're looking at. Check out the examples for the full set of features!



* Free software: MIT license
* Documentation: https://describe-json.readthedocs.io.


Installation
------------
$ pip install describe_json


Features
--------
This library does 2 things

* Shortens strings. It also displays their length and a md5 hash, so you can know whether multiple strings are equal
* Displays the length of arrays, and only 1 element, as an example. If arrays have differing elements, too bad, it only displays one element, so you'll never know what the others look like. You can use the `-r` flag, to get a random array element though.

Usage
-----
First of all, the tool plays really nicely with `jq`. Use `jq` to format the output of describe_json

::

  $ describe_json '{"my": ["json", "object"]}'|jq .
  {
    "my": [
      "length: 2; example:",
      "json"
    ]
  }

Outputting jq full paths for later inspection
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If you took a look at your JSON, and found the data you were looking for, 
but getting to it with jq will now require a lot of incremental approaches such as 
the following, you might as well just make `describe_json` help you with that.
It can automatically calculate the `jq` path, so you don't have to scroll up anymore!

::

    $ echo '{"a": {"b": [{"c": 1}]}}' | jq '.a'
    $ echo '{"a": {"b": [{"c": 1}]}}' | jq '.a.b'
    $ echo '{"a": {"b": [{"c": 1}]}}' | jq '.a.b[0]'
    $ echo '{"a": {"b": [{"c": 1}]}}' | jq '.a.b[0].c'


Instead of the above, just use the -j flag, and you'll see full paths for all dict keys

::

    $ describe_json '{"a": {"b": [{"c": 1}]}}' -j
    {'.a': {'.a.b': [{'.a.b[0].c': 1}]}}



Basic piping
^^^^^^^^^^^^

::

  $ echo '{"a": [1, 2, 3, 4]}' | describe_json
  {"a": ["length: 4; example:", 1]}

Basic array shortening
^^^^^^^^^^^^^^^^^^^^^^

::

  $ describe_json '{"a": [1, 2, 3, 4]}'
  {"a": ["length: 4; example:", 1]}


Do you have some super long strings?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    $ describe_json '{"key": "suuuuuuuuuuuuuper long string"}'
    {"key": "suuuuuuuuu... len: 29, md5: b7d562a2bcec0a8a346b5f32c59f257f"}

...ok, in this case the output is longer than the string. But you'll be happier when the string is 50K long

Use a .json file
^^^^^^^^^^^^^^^^^^^^^
::

  $ cat example.json 
  {"key1": ["a", "b", "c"]}
  $ describe_json -f example.json 
  {"key1": ["length: 3; example:", "a"]}


Use a random array element
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
By default, the first element of an array is displayed. Use a random one?

::

  $ describe_json -r {"key1": ["a", "b", "c"]}
  {"key1": ["length: 3; example:", "b"]}

Specify a maximum array length
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
By default, only one element is displayed from an array. Specify the maximum size of arrays, after which, they are displayed as shortened

::

  $ describe_json -a 3 '{"key1": ["a", "b", "c"]}'
  {"key1": ["a", "b", "c"]}

Specify a maximum string length
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
By default, strings longer than 10 characters are truncated, and their md5 hash is shown (so you can see whether multiple strings that begin with the same characters are equal or not). Specify a maximum length for strings

::

  $ describe_json -s 30 '{"key": "qwertyuiopasdfghjklzxcvbnm"}
  {"key": "qwertyuiopasdfghjklzxcvbnm"}


and that's about it! :)

Testing it in development mode
------------------------------
There are only doctests for the moment. They will be ran as 1 unit test, but don't worry, there are more than just 1 test.

::

  $ python setup.py test



Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
