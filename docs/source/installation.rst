.. 
   Copyright (c) 2024 National Technology and Engineering Solutions of Sandia, LLC.  
   Under the terms of Contract DE-NA0003525 with National Technology and Engineering 
   Solutions of Sandia, LLC, the U.S. Government retains certain rights in this software.

.. _installation:

Installation
============

This is a Python package.  You can use the source code directly, or install it as a package using pip install.

Pip Install
-----------

If you pip install, the code will be downloaded from https://pypi.org/projects/slypi when you type

.. code-block:: bash

  pip install slypi

If you are working behind a proxy, you might also need, e.g.

.. code-block:: bash

  pip install slypi --proxy your-proxy:your-port

If you are getting SSL certificate errors, you can use:

.. code-block:: bash

  pip install slypi --trusted-host pypi.org --trusted-host files.pythonhosted.org

Be aware that the last option is insecure.  The better approach is to 
fix your SSL certificate and/or point Python to a copy of the certificate.
This can be done using:

.. code-block:: bash

  pip config set global.cert path-to-your-certificate

You can also install locally (from the slypi directory) with pip from source using:

.. code-block:: bash

  pip install -e .

Note: that for slypi to work, you must have a Slycat server running.  This will 
probably be an institutional server, but you can also use Docker to run a local 
instance of Slycat.  See https://slycat.readthedocs.io/en/latest/ for details on 
setting up a server.

Requirements
------------

SlyPI uses Python 3.11.8 (as of this writing), and in addition requires various packages.  These packages should be automatically included when you install via pip.  The packages include numpy, scikit-learn, and pandas, as well as requests and requests-kerberos for authentication.  Dimension reduction related packages including torch and umap-learn.  Slypi U=uses pyMKS to compute autocorrelation for images, although pyMKS is now optional, and can be installed using

.. code-block:: bash

  pip install slypi[auto]

Some SlyPI operations can be run in parallel with the  ipyparallel package.