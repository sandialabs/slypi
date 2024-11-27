.. 
   Copyright (c) 2024 National Technology and Engineering Solutions of Sandia, LLC.  
   Under the terms of Contract DE-NA0003525 with National Technology and Engineering 
   Solutions of Sandia, LLC, the U.S. Government retains certain rights in this software.

Extension
=========

The SlyPI package is designed to be extensible and adaptable for use in different 
situations, which are desribed below.

Slycat Interaction
------------------

The core functionality of SlyPI allows interaction with the Slycat server
through it's REST API.  This functionality is provided in the base slypi module 
(e.g. using ``import slypi``).

The core SlyPI functionality is exposed via the various utilities previously describing, consisting
mainly of the command line sripts available to upload models to Slycat.  These scripts can be 
be used as is or can be called from within other python scripts.

Here is an example of uploading a Parameter Space model from within a python script.

.. code-block:: python

   import slypi.ps.upload_csv as ps_csv

   # parameter space file
   CARS_FILE = ['example-data/cars.csv']

   # input/output columns for cars data file
   CARS_INPUT = ['--input-columns', 'Model', 'Cylinders', 'Displacement', 'Weight', 'Year']
   CARS_OUTPUT = ['--output-columns', 'MPG', 'Horsepower', 'Acceleration']

   # create PS model from cars file
   ps_parser = ps_csv.parser()
   arguments = ps_parser.parse_args(CARS_FILE + CARS_INPUT + CARS_OUTPUT)
   ps_csv.create_model(arguments, ps_csv.log)

Ensemble Utilities
------------------

A secondary SlyPI functionality serves to manipulate numerical simulation output for the 
purpose of creating Slycat models.  This functionality is exposed in the ensemble utilities
submodule (e.g. using ``import slypi.ensemble``).  As with the core SlyPI functionality, these
utilities can be used from the command line, but are also available from within python.

These utilities can be used to pull data from particular simulation outputs and
manipulate tables used for Slycat imports.  They also supply algorithms for data analysis
outside of Slycat, and simultaneously expose algorithms that Slycat uses for some of it's model
creation (for example the VideoSwarm time-aligned PCA algorithm).

Here is an example of using the SlyPI ensemble table utility to join analysis results for a later
import to a Parameter Space model.

.. code-block:: python

    import os

    # table command line ensemble table utility
    import slypi.ensemble.table as table

    # create Parameter Space table by joining tables createed during analysis
    arg_list = ['--join',
                'example-data/spinodal-out/movies.csv',
                'example-data/spinodal-out/end-state.csv',
                'example-data/spinodal-out/auto-PCA-end-state.csv',
                'example-data/spinodal-out/auto-Isomap-end-state.csv',
                '--output-dir', 'example-data/spinodal-out',
                '--ignore-index',
                '--csv-out ps-PCA-Isomap.csv',
                '--csv-no-index',
                '--over-write']
    table.main(arg_list)

Plugins
-------

Finally, within the SlyPI ensemble submodule, plugins exist for interating with particular file
format or particular simulation codes.  These routines include code that reads specific file 
formats, file-conversion, and any particular pre-processing requirements.

The routines are provided to SlyPI by over-riding functions in the ``PluginTemplate`` class.  
The ``PluginTemplate`` class provides very basic functionality, such as converting images to movies.
Generally speaking, however, the basic template won't work for a particular simulation.

Plugins can be found in the slypi/ensemble/plugins source directory, but as an example, 
here a subroutine which over-rides the standard mesh reader in ``PluginTemplate``:

.. code-block:: python

    # read npy and sim.npy (also npy) formats
    def read_file(self, file_in, file_type=None):

        # check file extension, if not provided
        if file_type is None:

            # npy file type
            if file_in.endswith('.npy'):
                file_type = 'npy'

        # check if we have npy or sim.npy
        if file_type == 'npy':
            
            # read npy file
            try:
                data = np.load(file_in)
            except ValueError:
                self.log.error("Could not read " + file_in + " as a .npy file.")
                raise ValueError("Could not read " + file_in + " as a .npy file.")

        # otherwise default to mesh
        else:
            data = super().read_file(file_in, file_type)

        return data

Plugin API
----------

This section provides an API for the slypi.ensemble utilities in case you want to create your own plugin.

.. autoclass:: slypi.ensemble.ArgumentParser
    :members:

----

.. autofunction:: slypi.ensemble.init_logger

----

.. autoclass:: slypi.ensemble.utilities.Table
    :members:

----

.. autoclass:: slypi.ensemble.utilities.EnsembleSpecifierError

----

.. autoclass:: slypi.ensemble.PluginTemplate
    :members:

----

.. autofunction:: slypi.ensemble.plugin

----

.. autoclass:: slypi.ensemble.algorithms.reduction.DimensionReduction
    :members:
