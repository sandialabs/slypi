# Copyright (c) 2024 National Technology and Engineering Solutions of Sandia, LLC.  
# Under the terms of Contract DE-NA0003525 with National Technology and Engineering 
# Solutions of Sandia, LLC, the U.S. Government retains certain rights in this software.

# This script tests the convert.py using the phase-field example
# dataset.  Tests are done on the user interface to check
# the options.
#
# WARNING: When this script is run, the output_dir is
# deleted, unless delete_output_dir is False.
#
# Different tests can be run by setting the below flags.

# S. Martin
# 3/19/2024

# file/path manipulation
import os
import shutil
from pathlib import Path

# arguments
import argparse

# slypi convert utility
from slypi.ensemble.convert import convert

# file paths

# directory containing the phase-field example dataset
test_data_dir = os.path.join('example-data', 'spinodal')

# dimension reduction test directory
reduce_dir = os.path.join('example-data', 'spinodal-out','test-reduce')

# output directory to use for testing
output_dir = os.path.join('example-data', 'spinodal-out', 'test-convert')

# sampled directory
sampled_dir = os.path.join('example-data', 'spinodal-out', 'test-sampled-data')

# set up argument parser
def init_parser():

    # define our own version of the romans parser
    description = "Generate various test .csv files from phase-field ensemble data."
    parser = argparse.ArgumentParser (description = description)

    # delete output directory (defaults to False)
    parser.add_argument('--delete-output-dir', action="store_true", default=False, 
        help="Delete output directory before starting tests.")

    # available tests
    parser.add_argument('--test-UI', action="store_true", default=False,
        help="Test command line UI for convert.py.")
    parser.add_argument('--test-conversions', action="store_true", default=False,
        help="Test conversions.")
    parser.add_argument('--test-end-state', action="store_true", default=False,
        help="Do end-state conversions (e.g. images and movies).")
    parser.add_argument('--test-parallel', action="store_true", default=False,
        help="Run parallel tests using ipyparallel (must have ipengine running).")
    parser.add_argument('--test-all', action="store_true", default=False,
        help="Run every test.")

    return parser

# delete output_dir, if present
def delete_output_dir(args):

    if os.path.isdir(output_dir):
        if args.delete_output_dir:
            shutil.rmtree(output_dir)
    
    else:
        Path(output_dir).mkdir(parents=True)

# argument parser testing
#########################

def test_UI(args):

    if args.test_UI or args.test_all:

        # no arguments
        arg_list = []
        try:
            convert(arg_list)
        except SystemExit:
            print("Passed no argument check.\n")

        # ensemble only
        arg_list = ['--ensemble', os.path.join(test_data_dir, 'workdir.%d')]
        try:
            convert(arg_list)
        except SystemExit:
            print("Passed --ensemble only check.\n")

        # ensemble and input files
        arg_list = ['--ensemble', os.path.join(test_data_dir, 'workdir.1'),
                    '--input-files', 'out.cahn_hilliard_0.vtk']
        try:
            convert(arg_list)
        except SystemExit:
            print("Passed --ensemble and --input-files check.\n")

        # ensemble, input files, and output directory
        arg_list = ['--ensemble', os.path.join(test_data_dir, 'workdir.1'),
                    '--input-files', 'out.cahn_hilliard_0.vtk',
                    '--output-dir', os.path.join(output_dir, 'workdir.1')]
        try:
            convert(arg_list)
        except SystemExit:
            print("Passed --ensemble, --input-files, and --output-dir check.\n")

        # ensemble, input files, output directory, and output format
        arg_list = ['--ensemble', os.path.join(test_data_dir, 'workdir.1'),
                    '--input-files', 'out.cahn_hilliard_0.vtk',
                    '--output-dir', os.path.join(output_dir, 'workdir.1'),
                    '--output-format', 'vtk']
        try:
            convert(arg_list)
        except SystemExit:
            print("Passed --over-write check.\n")

        # check for unrecognized argument
        arg_list = ['--ensemble', os.path.join(test_data_dir, 'workdir.1'),
                    '--input-files', 'out.cahn_hilliard_0.vtk',
                    '--output-dir', os.path.join(output_dir, 'workdir.1'),
                    '--output-format', 'npy',
                    '--foo', 'bar']
        try:
            convert(arg_list)
        except SystemExit:
            print("Passed --foo bar check.\n")

        # check for --csv file conflict
        arg_list = ['--ensemble', os.path.join(test_data_dir, 'workdir.1'),
                    '--input-files', 'out.cahn_hilliard_0.vtk',
                    '--output-dir', os.path.join(output_dir, 'workdir.1'),
                    '--output-format', 'npy',
                    '--csv-file', 'foo-bar.csv']
        try:
            convert(arg_list)
        except SystemExit:
            print("Passed --csv-file check.\n")

        # check --csv-col when using --csv-file
        arg_list = ['--csv-file', os.path.join(test_data_dir, 'metadata.csv')]
        try:
            convert(arg_list)
        except SystemExit:
            print("Passed --csv-col check.\n")

        # check --csv-header
        arg_list = ['--ensemble', os.path.join(test_data_dir, 'workdir.7'),
                    '--input-files', 'out.cahn_hilliard_0.npz',
                    '--output-dir', os.path.join(output_dir, 'workdir.7'),
                    '--output-format', 'npy',
                    '--csv-out', 'foo-bar.csv']
        try:
            convert(arg_list)
        except SystemExit:
            print("Passed --csv-header check.\n")

# file conversion testing
#########################

def test_conversions(args):

    if args.test_conversions or args.test_all:

        # copy three npz to npz and create csv with links
        print("Converting .npz files in workdir.%d[0:20] to .npz files ...")
        arg_list = ['--ensemble', os.path.join(test_data_dir, 'workdir.%d[0:20]'),
                    '--input-files', 'out.cahn_hilliard_50000000.npz',
                    '--output-dir', output_dir,
                    '--output-format', 'npz',
                    '--over-write',
                    '--csv-out', 'three-npz.csv',
                    '--csv-header', 'Three NPZ']
        convert(arg_list)

        # test csv as input, convert .vtk to .npy
        print("Converting .npz to .npy ...")
        arg_list = ['--csv-file', os.path.join(output_dir, 'three-npz.csv'),
                    '--csv-col', 'Three NPZ',
                    '--output-dir', output_dir,
                    '--output-format', 'npy',
                    '--over-write']
        convert(arg_list)

        # test .npy to .npy
        print("Converting .npy to .npy ...")
        arg_list = ['--ensemble', os.path.join(output_dir, 'workdir.%d[0:20]'),
                    '--input-files', 'out.cahn_hilliard_50000000.npy',
                    '--output-dir', output_dir,
                    '--output-format', 'npy',
                    '--over-write']
        convert(arg_list)

        # convert .npy to .jpg
        print("Converting .npy to .jpg ...")
        arg_list = ['--ensemble', os.path.join(output_dir, 'workdir.%d[0:20]'),
                    '--input-files', 'out.cahn_hilliard_50000000.npy',
                    '--output-dir', output_dir,
                    '--output-format', 'jpg',
                    '--over-write',
                    '--plugin', 'convert',
                    '--suffix', 'phase_field']
        convert(arg_list)

# create end state images and movies
#################################### 

def test_end_state(args):

    if args.test_end_state or args.test_all:

        # create end state images
        print("Creating End State image files ...")
        arg_list = ['--ensemble', os.path.join(test_data_dir, 'workdir.%d'),
                    '--input-files', 'out.cahn_hilliard_50000000.npz',
                    '--output-dir', output_dir,
                    '--output-format', 'jpg',
                    '--over-write',
                    '--suffix', 'phase_field',
                    '--csv-out', 'end-state.csv',
                    '--csv-header', 'End State',
                    '--plugin', 'convert']
        convert(arg_list)

        # create simulation movies
        print("Creating simulation movie files ...")
        arg_list = ['--ensemble', os.path.join(test_data_dir, 'workdir.%d'),
                    '--input-files', 'out.cahn_hilliard_%d.npz',
                    '--output-dir', output_dir,
                    '--output-format', 'mp4',
                    '--over-write',
                    '--suffix', 'phase_field',
                    '--csv-out', 'movies.csv',
                    '--csv-header', 'Movie',
                    '--plugin', 'convert']
        convert(arg_list)

# parallel testing
##################

def test_parallel(args):

    if args.test_parallel or args.test_all:

        # create end state images in parallel
        print("Creating End State image files ...")
        arg_list = ['--ensemble', os.path.join(test_data_dir, 'workdir.%d'),
                    '--input-files', 'out.cahn_hilliard_50000000.npz',
                    '--output-dir', output_dir,
                    '--output-format', 'jpg',
                    '--over-write',
                    '--suffix', 'phase_field',
                    '--csv-out', 'end-state.csv',
                    '--csv-header', 'End State',
                    '--parallel',
                    '--plugin', 'convert']
        convert(arg_list)

        # create simulation movies
        print("Creating simulation movie files ...")
        arg_list = ['--ensemble', os.path.join(test_data_dir, 'workdir.%d'),
                    '--input-files', 'out.cahn_hilliard_%d.npz',
                    '--output-dir', output_dir,
                    '--output-format', 'mp4',
                    '--over-write',
                    '--csv-out', 'movies.csv',
                    '--csv-header', 'Movie',
                    '--parallel',
                    '--plugin', 'convert',
                    '--suffix', 'phase_field']
        convert(arg_list)

if __name__ == "__main__":

    # get command line flags
    parser = init_parser()
    args = parser.parse_args()

    # delete output directory, if requested
    delete_output_dir(args)

    # check if there are any tests
    if not (args.test_UI or \
            args.test_conversions or \
            args.test_end_state or \
            args.test_parallel or \
            args.test_all):
        print("No tests were selected.")

    # run tests
    test_UI(args)
    test_conversions(args)
    test_end_state(args)
    test_parallel(args)
