.. _running:

Running
=======
In order to run BDC_SEARCH_STAC, you must define variable `ENVIRONMENT`. By default, the application runs on development mode. You can change to
`ProductionConfig` or `TestingConfig` with the following command:

.. code-block:: sh

    $ export ENVIRONMENT=ProductionConfig
    $ python manager.py run

It will runs on host `0.0.0.0` with port `5000`. You can access directly through `http://127.0.0.1:5000/stac/status`
