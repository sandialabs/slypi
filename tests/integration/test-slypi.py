# Copyright (c) 2024 National Technology and Engineering Solutions of Sandia, LLC.  
# Under the terms of Contract DE-NA0003525 with National Technology and Engineering 
# Solutions of Sandia, LLC, the U.S. Government retains certain rights in this software.

# This script does unit/integration testing on slypi.
#
# To run the tests, type:
# $ python -m unittest test-slypi.py
#
# Modify SLYCAT_CONNECTION to use a different slycat server.
# 
# NOTE: Models are created but not destroyed.
#
# S. Martin
# 10/10/2023

import unittest
import warnings

# slycat web client code to test
import slypi
import slypi.util.list_markings as list_markings
import slypi.util.list_projects as list_projects
import slypi.cca.upload_random as cca_random
import slypi.cca.upload_csv as cca_csv
import slypi.ps.upload_csv as ps_csv
import slypi.dac.upload_gen as dac_gen

# slycat connection parameters for localhost
SLYCAT_CONNECTION = ['--host', 'https://localhost', '--user', 'slycat', 
                     '--password', 'slycat',
                     '--port', '9001', '--no-verify']

# test marking for localhost
TEST_MARKING = ['--marking', 'faculty']

# qual server
# SLYCAT_CONNECTION = ['--host', 'https://slycat-qual2.sandia.gov/', '--kerberos']

# marking for qual
# TEST_MARKING = ['--marking', 'mna']

# testing project name
TEST_PROJECT = ['--project-name', 'Unit/Integration Testing']

# test landmakrs
TEST_LANDMARKS = ['--num-landmarks', '30', '--model-name', 'DAC Landmarks']

# test PCA
TEST_PCA_COMPS = ['--num-PCA-comps', '10', '--model-name', 'DAC PCA']

# parameter space files
CARS_FILE = ['example-data/cars.csv']

# DAC PCA weather file
DAC_PCA_FILE = ['example-data/weather-dac-gen-pca.zip']

# input/output columns for cars data file
PS_CARS_INPUT = ['--input-columns', 'Model', 'Cylinders', 'Displacement', 'Weight',
              'Year', 'Origin']
PS_CARS_OUTPUT = ['--output-columns', 'MPG', 'Horsepower', 'Acceleration']
PS_CARS_CATEGORICAL = ['--categorical-columns', 'Cylinders']

CCA_CARS_INPUT = ['--input-columns', 'Cylinders', 'Displacement', 'Weight',
              'Year']
CCA_CARS_OUTPUT = ['--output-columns', 'MPG', 'Horsepower', 'Acceleration']

# turn off warnings for all tests
def ignore_warnings(test_func):
    def do_test(self, *args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            test_func(self, *args, **kwargs)
    return do_test

# tests a few of the different pieces of slycat.web.client, 
# set connection information in paramters above
class TestSlypi(unittest.TestCase):

    # connect to local host
    def connect_to_server(self, arguments=None):

        # call parser with Slycat docker arguments
        parser = slypi.ArgumentParser()
        if not arguments:
            arguments = parser.parse_args(SLYCAT_CONNECTION)

        # connect to Slycat
        connection = slypi.connect(arguments)

        return arguments, connection

    @ignore_warnings
    def test_connection(self):
        """
        Test that we can connect to Slycat.
        """

        self.connect_to_server()

    @ignore_warnings
    def test_list_markings(self):
        """
        Test list markings on localhost.
        """

        # list markings
        arguments, connection = self.connect_to_server()
        list_markings.main(connection)

    @ignore_warnings
    def test_list_projects(self):
        """
        Test list projects on localhost.
        """

        # list projects
        arguments, connection = self.connect_to_server()
        list_projects.main(arguments, connection)

    @ignore_warnings
    def test_random_cca(self):
        """
        Test random CCA model creation.
        """

        # create random CCA model
        arguments = cca_random.parse_arguments(SLYCAT_CONNECTION + TEST_MARKING +
                                               TEST_PROJECT)
        arguments, connection = self.connect_to_server(arguments)
        mid = cca_random.main(arguments, connection)

    @ignore_warnings
    def test_cca_csv(self):
        """
        Test CCA with cars.csv file.
        """
    
        # create CCA model
        cca_parser = cca_csv.parser()
        arguments = cca_parser.parse_args(SLYCAT_CONNECTION + CARS_FILE + CCA_CARS_INPUT + 
                                          CCA_CARS_OUTPUT + TEST_MARKING + TEST_PROJECT)
        arguments, connection = self.connect_to_server(arguments)
        cca_csv.create_model(arguments, cca_csv.log)

    @ignore_warnings
    def test_ps_cars(self):
        """
        Test Parameter Space loader with cars.csv file.
        """

        # create PS model from cars.csv
        ps_parser = ps_csv.parser()
        arguments = ps_parser.parse_args(SLYCAT_CONNECTION + CARS_FILE + PS_CARS_INPUT + 
                                         PS_CARS_OUTPUT + PS_CARS_CATEGORICAL + 
                                         TEST_MARKING + TEST_PROJECT)
        ps_csv.create_model(arguments, ps_csv.log)

    @ignore_warnings
    def test_dac_gen(self):
        """
        Test Dial-A-Cluster generic .zip loader with weather data.
        """

        # create DAC model from weather data using PCA
        dac_parser = dac_gen.parser()
        arguments = dac_parser.parse_args(SLYCAT_CONNECTION + DAC_PCA_FILE + 
                                          TEST_MARKING + TEST_PROJECT)
        dac_gen.create_model(arguments, dac_gen.log)

if __name__ == '__main__':
    unittest.main()