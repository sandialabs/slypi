.. 
   Copyright (c) 2024 National Technology and Engineering Solutions of Sandia, LLC.  
   Under the terms of Contract DE-NA0003525 with National Technology and Engineering 
   Solutions of Sandia, LLC, the U.S. Government retains certain rights in this software.

Development 
===========

In addition to extending the toolbox, development of additional core features is also
possible.  The easiest way to further develop SlyPI  is to use the drivers in the ``test``
directory.  

The general approach taken to date is to write a utility code that interfaces between 
the command line and the actual SlyPI classes and plugins.  To test these utility codes, 
we have written a variety of drivers which set up the parameters and call the utilites 
from Python.  We use the example data to test the codes, and pointers to
the data is coded directly in the test scripts.

The tests are usually run from the root directory.

Slycat Interaction
------------------

The script ``test-slypi.py`` is used to test the upload sripts.  In order to use this script
you must have a running Slycat server and may have to modify the code to connect.  The current
setup uses a docker container.

.. code-block:: bash

   $ python tests/integration/test-slypi.py

The results of this script are uploads of various models to the Slycat server.  The VideoSwarm
upload script is not tested because it requires file links that generally do not work with a 
docker container.

Ensemble Utilities
------------------

The remaining tests are for the ensemble utilities.  The parsing funtionality is tested
using ``test-ensemble.py``.

.. code-block:: bash

   $ python tests/unit/test-ensemble.py

Other tests for the ensemble are ``test-ensemble-convert.py``, ``test-ensemble-reduce.py``
and ``test-ensemble-table.py``.  Some of the tests can be slow, so there are options to execute 
only certain tests.

There is a certain amount of inter-dependence between the tests.  For example, 
``test-ensemble-reduce.py`` and ``test-ensemble-convert.py`` must precede 
``test-ensemble-table.py`` to provide files for creating tables.  After running the first two tests,
use

.. code-block:: bash

   $ python tests/integration/test-ensemble-table.py

To run the parallel tests, you need to have ipyparallel running.  The necessary procedure will
vary depending on your environment.  If you are running the tests locally, you can use

.. code-block:: bash

   $ ipcluster start --n=4

from the slypi directory.

test-ensemble-convert.py
------------------------

.. program-output:: python ../../tests/integration/test-ensemble-convert.py --help

test-ensemble-reduce.py
-----------------------

.. program-output:: python ../../tests/integration/test-ensemble-reduce.py --help
