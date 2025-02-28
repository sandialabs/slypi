.. 
   Copyright (c) 2024 National Technology and Engineering Solutions of Sandia, LLC.  
   Under the terms of Contract DE-NA0003525 with National Technology and Engineering 
   Solutions of Sandia, LLC, the U.S. Government retains certain rights in this software.

Utilities
=========

The command line utilities making up the SlyPI package are listed here.  The available 
command line options for any utility can be seen using the ``--help`` flag.

These utilities can also be called from within python, where the arguments are passed
in a list.

Slycat Interaction
------------------

These utilities interact directly with Slycat, e.g. querying markings or uploading models.

List markings
^^^^^^^^^^^^^

.. program-output:: python -m slypi.util.list_markings --help

List Projects
^^^^^^^^^^^^^

.. program-output:: python -m slypi.util.list_projects --help
    
Parameter Space 
^^^^^^^^^^^^^^^

.. program-output:: python -m slypi.ps.upload_csv --help

CCA
^^^

.. program-output:: python -m slypi.cca.upload_csv --help

Dial-A-Cluster
^^^^^^^^^^^^^^

.. program-output:: python -m slypi.dac.upload_gen --help

VideoSwarm
^^^^^^^^^^

.. program-output:: python -m slypi.vs.upload_local --help


Ensemble Manipulation
---------------------

These utilities are used to read and manipulate the files making up ensemble data, typically
from numerical simulations.  They will accept various file formats and output various Slycat
file formats.  They can be extended to work with new file formats using plugins.

table.py
^^^^^^^^

.. program-output:: python -m slypi.ensemble.table --help

convert.py
^^^^^^^^^^

.. program-output:: python -m slypi.ensemble.convert --help

