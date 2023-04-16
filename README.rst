Introduction
------------

This Python package provides a convenient way to display data in a tabular format within a terminal. It is specifically designed for easy customization through the use of string parameters, which can be set by terminal applications.

Features:

* Table rows can be filtered using an expression provided as a string.
* The table can be sorted based on an expression provided as a string.
* Columns in the table can be removed by specifying a list.

Example
-------
This package is designed to be imported into your CLI application. To demonstrate the capabilities of this package, a sample CLI application is included for your convenience.

To run the sample application, use:

.. code:: shell

  python -m clitable

Most of the command line options for this application are self-explanatory. Use :code:`--help` to view a complete list of available options.

The most interesting aspect is how to specify filters, for example. This can be done as follows:

.. code:: shell

  python -m clitable -f="class==1 and id !=3"

The :code:`-f` option filters out rows in the table according to the given predicate. As you can see, the predicate is provided as a string. This string is processed by a custom interpreter implemented using Lark. For security reasons, 'eval' is not used. The predicate can include a combination of logical and comparison operators, as well as column names and values. The supported operators are:

* Logical operators: and, or
* Comparison operators: ==, !=, <, <=, >, >=
    
To use the :code:`-f` option, you need to construct a valid expression using these operators and the column names in the table. The column names should be written without any special characters or spaces, and the values should be of the appropriate type (e.g., strings should be in quotes, numbers without quotes).

Try it out!

Credits
-------
* This package uses lark_ (H/T)
* This repo was derived from python-cli-template_ (H/T)

..  _lark: https://github.com/lark-parser/lark
..  _python-cli-template: https://github.com/AnthonyBloomer/python-cli-template/