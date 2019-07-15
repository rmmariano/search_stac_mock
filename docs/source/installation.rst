.. _installation:

Installation
============

Python Version
--------------

You must use `bdc_search_stac` with Python 3+ and PyPy or Docker.

Dependencies
------------

These distributions will be installed automatically when installing wtss.

* `Flask <http://flask.pocoo.org/>`_ microframework for Python based on Wekzeug.
* `Flask-Cors <https://flask-cors.readthedocs.io/en/latest/>`_ Flask extension for handling Cross Origin Resource Sharing (CORS)
* `flask-restplus <https://flask-restplus.readthedocs.io/en/stable/>`_ an extension for Flask that adds support for quickly building REST APIs.
* `SQLAlchemy <https://docs.sqlalchemy.org/en/13/>`_ SQLAlchemy is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL.
* `Flask-SQLAlchemy <https://flask-sqlalchemy.palletsprojects.com/en/2.x/>`_  an extension for Flask that adds support for SQLAlchemy to your application.
* `Flask-Script <https://flask-script.readthedocs.io/en/latest/>`_ an extension provides support for writing external scripts in Flask. 
* `Werkzeug <https://werkzeug.palletsprojects.com/en/0.15.x/>`_ Werkzeug is a comprehensive WSGI web application library.
* `cerberus <https://docs.python-cerberus.org/en/stable/>`_ Cerberus provides powerful yet simple and lightweight data validation functionality out of the box and is designed to be easily extensible, allowing for custom validation.
* `psycopg2 <http://initd.org/psycopg/docs/>`_ Psycopg is the most popular PostgreSQL database adapter for the Python programming language.

Install BDC-Search-STAC
---------------------

Within the activated environment, use the following command to install Flask:

    $ pip install bdc-search-stac

or with REST API and Docker => `Github <https://github.com/betonr/search_stac>`_ 