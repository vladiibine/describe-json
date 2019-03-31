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
describe_json basically displays your JSON, replacing any arrays with a dictionary that just describes the array.



* Free software: MIT license
* Documentation: https://describe-json.readthedocs.io.


Installation
------------
$ pip install describe_json


Usage
-----
echo '{"a": [1, 2, 3, 4]}' | describe_json

...or
describe_json '{"a": [1, 2, 3, 4]}'

...or
describe_json -f some_file.json


Features
--------

* TODO

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
