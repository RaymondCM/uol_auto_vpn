Installation Instructions
=========================

Recommended install

.. parsed-literal::

    wget -qO install.sh https://raw.githubusercontent.com/RaymondKirk/uol_auto_vpn/main/install.sh && ((sleep 2 && rm install.sh)&) && bash install.sh


You can also install via `pip`

.. parsed-literal::

    $ pip install uol_auto_vpn
    # OR
    $ pip install git+https://github.com/RaymondKirk/uol_auto_vpn.git@\ |release|\

Once installed you can run with 'uol_auto_vpn'.



Documentation
~~~~~~~~~~~~~

Building
""""""""
Building the documentation for uol_auto_vpn is easy! From the root of the repository
run the provided bash script

.. code-block:: bash

    $ ./docs/create_docs.sh

You can then open the documentation locally or view them at https://raymondkirk.github.io/uol_auto_vpn/

.. code-block:: bash

    $ xdg-open docs/build/html/index.html

Tests
~~~~~

To run the tests clone the repository and install pytest.

.. code-block:: bash

    $ git clone https://github.com/RaymondKirk/uol_auto_vpn.git
    $ pip install pytest

Then run pytest in the root directory.

.. code-block:: bash

    $ cd raymond
    $ pytest -v

Flake8 linting tests.

.. code-block:: bash

    $ pip install flake8
    $ flake8 uol_auto_vpn --count --select=E9,F63,F7,F82 --show-source --statistics
    $ flake8 uol_auto_vpn --count --exit-zero --ignore=F401 --max-complexity=10 --max-line-length=127 --statistics
