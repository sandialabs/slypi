# This script does unit/integration testing on slycat-web-client.
#
# To run the tests, type:
# $ python -m unittest test_slypi_tdms
# $ python test_slypi_tdms
#
# To run a single test, type:
# $ python -m unittest test_slypi_tdms.TestSlycatWebClient.test_list_markings
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
import slypi.dac.upload_gen as dac_gen
import slypi.dac.tdms as tdms
import slypi.dac.tdms_batches as dac_tdms_batches
import slypi.dac.run_chart as run_chart

# slycat connection parameters for localhost
SLYCAT_CONNECTION = ['--host', 'https://localhost', 
                     '--user', 'slycat', '--password', 'slycat',
                     '--port', '9001', '--no-verify']

# test marking for localhost
# TEST_MARKING = ['--marking', 'faculty']

# qual server
# SLYCAT_CONNECTION = ['--host', 'https://slycat-qual2.sandia.gov/', '--kerberos', '--no-verify']

# marking for qual
TEST_MARKING = ['--marking', 'mna']

# testing project name
TEST_PROJECT = ['--project-name', 'Unit/Integration Testing']

# test landmakrs
TEST_LANDMARKS = ['--num-landmarks', '30', '--model-name', 'DAC Landmarks']

# test PCA
TEST_PCA_COMPS = ['--num-PCA-comps', '10', '--model-name', 'DAC PCA']

# DAC PCA weather file
DAC_PCA_FILE = ['../slycat-data/dial-a-cluster/weather-dac-gen-pca.zip']

# input for dac_tdms
DAC_TDMS_FILE = ['../dac-switchtubes/2A1828_07_000021_Data Package.zip']

# inputs for dac_tdms_batches
DAC_TDMS_BATCHES = ['--input-tdms-batches', '../dac-switchtubes', '2A1828_07', '21']

# different inputs to dac_run_chart
DAC_RUN_CHART_DIR_GLOB = ['--input-tdms-glob', '../dac-switchtubes', 
                          '2A1828_07*', 'test-dac-run-chart.zip']
DAC_RUN_CHART_DIR_BATCHES = ['--input-tdms-batches', '../dac-switchtubes',
                             '2A1828_07', '21', 'test-dac-run-chart.zip', '--model-name',
                             'Dir Batches']
DAC_RUN_CHART_DIR = ['--input-tdms-dir',  '../dac-switchtubes/2A1828_07_000021_Data Package', #'../dac-switchtubes/For Shawn',
                     'test-dac-run-chart.zip', '--model-name', 'Dir']
DAC_RUN_CHART_MISSING = ['--input-tdms-dir', '../dac-switchtubes/2A1828_07_000021_Data Package/',
                         '2A1828_07_run_chart.zip']
DAC_RUN_CHART_SINGLETON = ['--input-tdms-dir', '../dac-switchtubes/5A2026_99_990424_401',
                           '5A2026_99_9904024_401.zip']
DAC_RUN_CHART_UNSTRUCTURED = ['--input-tdms-dir', '../dac-switchtubes/4A2356_01',
                              '4A2356_01.zip']
DAC_RUN_CHART_ZIP = ['--input-tdms-zip', '../dac-switchtubes/2A1828_07_000021_Data Package.zip', 
                     'temp_out.zip']

# same options for dac_run_chart
DAC_RUN_CHART_OPTIONS = ['--exclude', 'VL1', 'VL2', 'VL3', 'VL4', 'VL5', 'VL6', 
                         'Hold-off test', '--infer-last-value', '--clean-up-output',
                         '--num-PCA-comps', '2', '--curve']

# scatter plot option for run chart
DAC_RUN_CHART_SCATTER_OPTIONS = ['--exclude', 'VL1', 'VL2', 'VL3', 'VL4', 'VL5', 'VL6', 
                                 'Hold-off test', '--infer-last-value', '--clean-up-output',
                                 '--num-PCA-comps', '2']

# scatter plot option with missing run charts
DAC_RUN_CHART_MISSING_OPTIONS = ['--exclude', 'VL1', 'VL2', 'VL3', 'VL4', 'VL5', 'VL6', 
                                 'Hold-off test', '--infer-last-value', '--clean-up-output',
                                 '--use-shot-numbers', '--min-tdms-files', '1',
                                 '--use-const-value', '0']

# singleton options
DAC_RUN_CHART_SINGLETON_OPTIONS = ['--infer-last-value', '--clean-up-output']

# unstructured options
DAC_RUN_CHART_UNSTRUCTURED_OPTIONS = ['--infer-last-value', '--clean-up-output', '--unstructured']

# turn off warnings for all tests
def ignore_warnings(test_func):
    def do_test(self, *args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            test_func(self, *args, **kwargs)
    return do_test

# tests a few of the different pieces of slypi, 
# set connection information in paramters above
class TestSlyPITDMS(unittest.TestCase):

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
    def test_dac_gen(self):
        """
        Test Dial-A-Cluster generic .zip loader with weather data.
        """

        # create DAC model from weather data using PCA
        dac_parser = dac_gen.parser()
        arguments = dac_parser.parse_args(SLYCAT_CONNECTION + DAC_PCA_FILE + 
                                          TEST_MARKING + TEST_PROJECT)
        dac_gen.create_model(arguments, dac_gen.log)

    @ignore_warnings
    def test_tdms(self):
        """
        Test dac_tdms loader.
        """

        # create DAC model from switchtube data using PCA
        dac_parser = tdms.parser()
        arguments = dac_parser.parse_args(SLYCAT_CONNECTION + DAC_TDMS_FILE + 
                                          TEST_MARKING + TEST_PROJECT)
        tdms.create_model(arguments, tdms.log)

    @ignore_warnings
    def test_tdms_batches(self):
        """
        Test dac_tdms_batches loader.
        """

        # create DAC model batches from switchtube data using PCA
        dac_parser = dac_tdms_batches.parser()
        arguments = dac_parser.parse_args(SLYCAT_CONNECTION + DAC_TDMS_BATCHES + 
                                          TEST_MARKING + TEST_PROJECT)
        dac_tdms_batches.create_models(arguments)

    @ignore_warnings
    def test_tdms_run_chart_dir_glob(self):
        """
        Test dac_tdms_run_chart dir glob creation.
        """

        # DAC run chart with glob input option
        dac_parser = run_chart.parser()
        arguments = dac_parser.parse_args(SLYCAT_CONNECTION + DAC_RUN_CHART_DIR_GLOB + 
                                          ['--model-name', 'Dir Glob'] +
                                          DAC_RUN_CHART_OPTIONS +
                                          TEST_MARKING + TEST_PROJECT)
        run_chart.create_model(arguments, run_chart.log)

    @ignore_warnings
    def test_tdms_run_chart_dir_batches(self):
        """
        Test dac_tdms_run_chart dir batches creation.
        """

        # DAC run chart with batches option
        dac_parser = run_chart.parser()
        arguments = dac_parser.parse_args(SLYCAT_CONNECTION + DAC_RUN_CHART_DIR_BATCHES + 
                                          DAC_RUN_CHART_OPTIONS +
                                          TEST_MARKING + TEST_PROJECT)
        run_chart.create_model(arguments, run_chart.log)

    @ignore_warnings
    def test_tdms_run_chart_dir(self):
        """
        Test dac_tdms_run_chart dir creation.
        """

        # run chart with dir option
        dac_parser = run_chart.parser()
        arguments = dac_parser.parse_args(SLYCAT_CONNECTION + DAC_RUN_CHART_DIR + 
                                          DAC_RUN_CHART_OPTIONS +
                                          TEST_MARKING + TEST_PROJECT)
        run_chart.create_model(arguments, run_chart.log)

    @ignore_warnings
    def test_tdms_run_chart_scatter(self):
        """
        Test dac_tdms_run_chart with scatter plot option
        """

        # run chart with scatter plot option
        dac_parser = run_chart.parser()
        arguments = dac_parser.parse_args(SLYCAT_CONNECTION + DAC_RUN_CHART_DIR_GLOB + 
                                          ['--model-name', 'Scatter'] +
                                          DAC_RUN_CHART_SCATTER_OPTIONS +
                                          TEST_MARKING + TEST_PROJECT)
        run_chart.create_model(arguments, run_chart.log)

    @ignore_warnings
    def test_tdms_run_chart_scatter_shot_numbers(self):
        """
        Test dac_tdms_run_chart with scatter plot option
        """

        # run chart with scatter plot option
        dac_parser = run_chart.parser()
        arguments = dac_parser.parse_args(SLYCAT_CONNECTION + DAC_RUN_CHART_DIR_GLOB + 
                                          ['--model-name', 'Scatter Shot Numbers'] +
                                          DAC_RUN_CHART_SCATTER_OPTIONS +
                                          ['--use-shot-numbers'] + 
                                          TEST_MARKING + TEST_PROJECT)
        run_chart.create_model(arguments, run_chart.log)

    @ignore_warnings
    def test_tdms_run_chart_scatter_shot_numbers_highlight(self):
        """
        Test dac_tdms_run_chart with scatter plot option/highlights
        """

        # run chart with scatter plot option/highlights
        dac_parser = run_chart.parser()
        arguments = dac_parser.parse_args(SLYCAT_CONNECTION + DAC_RUN_CHART_DIR_GLOB + 
                                          ['--model-name', 'Scatter Shot Numbers Highlight'] +
                                          DAC_RUN_CHART_SCATTER_OPTIONS +
                                          ['--use-shot-numbers', '--highlight-shot-numbers'] + 
                                          TEST_MARKING + TEST_PROJECT)
        run_chart.create_model(arguments, run_chart.log)

    @ignore_warnings
    def test_tdms_run_chart_nans(self):
        """
        Test dac_tdms_run_chart with a missing run charts.
        """

        # run chart with missing chart options
        dac_parser = run_chart.parser()
        arguments = dac_parser.parse_args(SLYCAT_CONNECTION + DAC_RUN_CHART_MISSING + 
                                          ['--model-name', 'Missing Run Charts'] +
                                          DAC_RUN_CHART_MISSING_OPTIONS + 
                                          TEST_MARKING + TEST_PROJECT)
        run_chart.create_model(arguments, run_chart.log)

    @ignore_warnings
    def test_tdms_run_chart_singleton(self):
        """
        Test dac_tdms_run_chart with a single file.
        """

        # run chart with single file options
        dac_parser = run_chart.parser()
        arguments = dac_parser.parse_args(SLYCAT_CONNECTION + DAC_RUN_CHART_SINGLETON + 
                                          ['--model-name', 'Singleton Run Chart'] +
                                          DAC_RUN_CHART_SINGLETON_OPTIONS + 
                                          TEST_MARKING + TEST_PROJECT)
        run_chart.create_model(arguments, run_chart.log)

    @ignore_warnings
    def test_tdms_run_chart_unstructured(self):
        """
        Test dac_tdms_run_chart with an unstructred run chart directory.
        """

        # run chart with unstructured options
        dac_parser = run_chart.parser()
        arguments = dac_parser.parse_args(SLYCAT_CONNECTION + DAC_RUN_CHART_UNSTRUCTURED + 
                                          ['--model-name', 'Unstructured Run Chart'] +
                                          DAC_RUN_CHART_UNSTRUCTURED_OPTIONS + 
                                          TEST_MARKING + TEST_PROJECT)
        run_chart.create_model(arguments, run_chart.log)

    @ignore_warnings
    def test_tdms_run_chart_zip(self):
        """
        Test dac_tdms_run_chart with a zip archive input.
        """

        # run chart with zip archive
        dac_parser = run_chart.parser()
        arguments = dac_parser.parse_args(SLYCAT_CONNECTION + DAC_RUN_CHART_ZIP +
                                          ['--model-name', 'Zip Run Chart'] +
                                           DAC_RUN_CHART_OPTIONS +
                                           TEST_MARKING + TEST_PROJECT)
        run_chart.create_model(arguments, run_chart.log)

if __name__ == '__main__':
    unittest.main()