# Copyright (c) 2021 National Technology and Engineering Solutions of Sandia, LLC.  
# Under the terms of Contract DE-NA0003525 with National Technology and Engineering 
# Solutions of Sandia, LLC, the U.S. Government retains certain rights in this software.

# This is a plugin that provides support for dakota output.  In particular
# it can convert a tabular.dat file to a csv file.

# S. Martin
# 5/20/2025


# standard library imports
import argparse
from os.path import basename
from os.path import join

# 3rd party imports
import pandas as pd

# local imports
import slypi


# functions for specific operations
# class must be named Plugin
class Plugin(slypi.ensemble.PluginTemplate):

    # initialize command line argument parser
    def __init__(self):

        # describe plugin
        description = "This plugin provides support for converting a Dakota " + \
            "tabular file to a CSV file."

        # set up parser
        super().__init__(description=description)

    # convert tabular.dat to csv file
    def convert_files(self, file_list, output_dir, output_type, input_type=None):

        # check that there is only one tabular.dat file
        if len(file_list) > 1:
            raise ValueError("expected a single tabular.dat file.")
        if basename(file_list[0]) != 'tabular.dat':
            raise ValueError("expected a single tabular.dat file.")

        # read tabular.dat file
        df = pd.read_csv(file_list[0], delim_whitespace=True)

        # save as tabular.csv file
        output_file = join(output_dir, 'tabular.csv')
        df.to_csv(output_file, index=False)

        return [output_file]

# if called from the command line display plugin specific command line arguments
if __name__ == "__main__":

    generic = Plugin()
    generic.parser.parse_args()
