.. 
   Copyright (c) 2024 National Technology and Engineering Solutions of Sandia, LLC.  
   Under the terms of Contract DE-NA0003525 with National Technology and Engineering 
   Solutions of Sandia, LLC, the U.S. Government retains certain rights in this software.

Plugins
=======

The SlyPI package uses plugins to provide functionality for different numerical simulations, or really any other outside software.  The plugins largely handle differences in file formats between different simulations and software.  The following plugins are available for SlyPI.

User interaction with plugins is handled by command line arguments passed through SlyPI and onto the plugin.  As a result, plugin authors must not use command line arguments with the same or even prefix matched names of the SlyPI, or SlyPI utility arguments.  Any such arguments will be interpreted incorrectly and will likely fail.

To see the availble options for a SlyPI plugin, call the plugin directly with ``--help`` option, as in:

.. code-block:: python

    python -m slypi.ensemble.plugins.ps --help

Parameter Space
---------------

The Parameter Space plugin supports output that can be used to create Parameter Space models in Slycat.  The plugin can be called from the table.py utility using the ``--expand`` option.  The command line options for the plugin are given below.

.. code-block:: bash

    python -m slypi.ensemble.plugins.ps --help

.. program-output:: python -m slypi.ensemble.plugins.ps --help

VideoSwarm
----------

The VideoSwarm plugin provides output support for the files required to create a VideoSwarm model in Slycat.  The plugin can be called from the table.py utlity.   The command line options for the VideoSwarm plugin are shown below.

.. code-block:: bash

    python -m slypi.ensemble.plugins.vs --help

.. program-output:: python -m slypi.ensemble.plugins.vs --help

Convert 
-------

The convert plugin provides support for converting between various file formats.  In particular, it supports creating .mp4 format movies readable by Slycat.

.. code-block:: bash

    python -m slypi.ensemble.plugins.convert --help
    
.. program-output:: python -m slypi.ensemble.plugins.convert --help

