# Copyright (c) 2021 National Technology and Engineering Solutions of Sandia, LLC.  
# Under the terms of Contract DE-NA0003525 with National Technology and Engineering 
# Solutions of Sandia, LLC, the U.S. Government retains certain rights in this software.

# This script tests the reduce.py script using the phase-field
# test data and various dimension reduction algorithms.  Tests
# are done on the UI and on the MEMPHIS test data.  The reduction
# algorithms, to a lesser degree, are also tested.
#
# NOTE: Different tests can be performed depending on the
# test_* flags set below.

# S. Martin
# 3/22/2021

# file/path manipulation
import os
import shutil
import filecmp
from pathlib import Path

# flags for tests to run
import argparse

# reduction command line code
from slypi.ensemble.reduce import reduce

# file paths

# directory containing the phase-field test dataset
test_data_dir = os.path.join('example-data', 'spinodal')

# output directory to use for testing
output_dir = os.path.join('example-data', 'spinodal-out', 'test_reduce')

# output directory to use for testing
table_dir = os.path.join('example-data', 'spinodal-out', 'test_table')

# convert directory containing end state images and movies
convert_dir = os.path.join('example-data', 'spinodal-out', 'test_convert')

# uri-root-out conversion (location of files on cluster)
uri_root_out = 'file://test/spinodal_out'

# inc-PCA from cluster
inc_PCA = os.path.join('example-data','spinodal-out', 'inc-PCA')

# inc-whiten-PCA from cluster
inc_whiten_PCA = os.path.join('example-data', 'spinodal-out', 'inc-whiten-PCA')

# inc-auto-PCA from cluster
inc_auto_PCA = os.path.join('example-data', 'spinodal-out', 'inc-auto-PCA-100')

# reduced dataset by sampling
sampled_dir = os.path.join('example-data', 'spinodal-out', 'test_sampled_data')


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
        help="Test command line UI for reduce.py.")
    parser.add_argument('--test-save-load', action="store_true", default=False,
        help="Test save and load capability in reduce.py.")
    parser.add_argument('--test-end-state', action="store_true", default=False,
        help="Do end-state dimension reductions.")
    parser.add_argument('--test-time-aligned', action="store_true", default=False,
        help="Do time-aligned dimension reductions.")
    parser.add_argument('--test-all-time', action="store_true", default=False,
        help="Do dimension reductions with all time steps simultaneously.")
    # parser.add_argument('--test-betti', action="store_true", default=False,
    #     help="Do Betti number calculations.")
    parser.add_argument('--test-umap', action="store_true", default=False,
        help="Perform umap reduction on test set.")
    # parser.add_argument('--test-auto-encoder', action="store_true", default=False,
    #     help="Do auto-encoder dimension reductions.")
    parser.add_argument('--test-parallel', action="store_true", default=False,
        help="Run parallel tests.")
    parser.add_argument('--test-restart', action="store_true", default=False,
        help="Run restart testing.")
    parser.add_argument('--test-rd-npy', action="store_true", default=False,
        help="Test dimension reduction loaded from rd.npy file.")
    parser.add_argument('--test-all', action="store_true", default=False,
        help="Run every test.")

    return parser

# delete output_dir, if present
# create if not present
def delete_output_dir(args):

    # create output directory, if necessary
    if os.path.isdir(output_dir):
        if args.delete_output_dir:
            shutil.rmtree(output_dir)
            
    
    else:
        Path.mkdir(output_dir)

# argument parser testing
#########################

def test_UI(args):

    if args.test_UI or args.test_all:

        # no arguments
        arg_list = []
        try:
            reduce(arg_list)
        except SystemExit:
            print("Passed no argument check.\n")

        # missing --input-files
        arg_list = ['--ensemble', os.path.join(test_data_dir, 'workdir.%d')]
        try:
            reduce(arg_list)
        except SystemExit:
            print("Passed --input-files check.\n")

        # missing --output-dir
        arg_list = ['--ensemble', os.path.join(test_data_dir, 'workdir.%d'),
                    '--input-files', 'out.cahn_hilliard_0.vtk']
        try:
            reduce(arg_list)
        except SystemExit:
            print("Passed --output-dir check.\n")

        # missing --output-file
        arg_list = ['--ensemble', os.path.join(test_data_dir, 'workdir.%d'),
                    '--input-files', 'out.cahn_hilliard_0.vtk',
                    '--output-dir', output_dir]
        try:
            reduce(arg_list)
        except SystemExit:
            print("Passed --output-file check.\n")

        # --output-file extension
        arg_list = ['--ensemble', os.path.join(test_data_dir, 'workdir.%d'),
                    '--input-files', 'out.cahn_hilliard_50000000.vtk',
                    '--output-dir', output_dir,
                    '--output-file', 'out.cahn_hilliard_end_state_PCA']
        try:
            reduce(arg_list)
        except SystemExit:
            print("Passed --output-file extension check.\n")

        # test missing --algorithm
        arg_list = ['--ensemble', os.path.join(test_data_dir, 'workdir.%d'),
                    '--input-files', 'out.cahn_hilliard_50000000.vtk',
                    '--output-dir', output_dir,
                    '--output-file', 'out.cahn_hilliard_end_state_PCA.rd.npy',
                    '--over-write']
        try:
            reduce(arg_list)
        except ValueError:
            print("Passed --algorithm missing check.\n")
        
        # test algorithm incorrect
        arg_list = ['--ensemble', os.path.join(test_data_dir, 'workdir.%d'),
                    '--input-files', 'out.cahn_hilliard_50000000.vtk',
                    '--output-dir', output_dir,
                    '--output-file', 'out.cahn_hilliard_end_state_PCA.rd.npy',
                    '--algorithm', 'super-mega-duper']
        try:
            reduce(arg_list)
        except SystemExit:
            print("Passed --algorithm incorrect check.\n")

        # test number of dimensions
        arg_list = ['--ensemble', os.path.join(test_data_dir, 'workdir.%d'),
                    '--input-files', 'out.cahn_hilliard_50000000.npz',
                    '--output-dir', output_dir,
                    '--output-file', 'out.cahn_hilliard_end_state_PCA.rd.npy',
                    '--algorithm', 'PCA',
                    '--over-write']
        try:
            reduce(arg_list)
        except ValueError:
            print("Passed --num-dim check.\n")

        # test field-var
        arg_list = ['--ensemble', os.path.join(test_data_dir, 'workdir.%d'),
                    '--input-files', 'out.cahn_hilliard_50000000.npz',
                    '--output-dir', output_dir,
                    '--output-file', 'out.cahn_hilliard_end_state_PCA.rd.npy',
                    '--algorithm', 'PCA',
                    '--num-dim', '2',
                    '--over-write']
        try:
            reduce(arg_list)
        except ValueError:
            print("Passed --field-var check.\n")

        # test over-write
        arg_list = ['--ensemble', os.path.join(test_data_dir, 'workdir.%d'),
                    '--input-files', 'out.cahn_hilliard_50000000.npz',
                    '--output-dir', output_dir,
                    '--output-file', 'out.cahn_hilliard_end_state_PCA.rd.npy',
                    '--algorithm', 'PCA',
                    '--num-dim', '2']
        try:
            reduce(arg_list)
        except SystemExit:
            print("Passed --over-write check.\n")
        
        # un-recognized argument
        arg_list = ['--ensemble', os.path.join(test_data_dir, 'workdir.%d'),
                    '--input-files', 'out.cahn_hilliard_50000000.npz',
                    '--input-format', 'npy',
                    '--output-dir', output_dir,
                    '--output-file', 'out.cahn_hilliard_end_state_PCA.rd.npy',
                    '--algorithm', 'PCA',
                    '--num-dim', '2',
                    '--over-write', '--foo']
        try:
            reduce(arg_list)
        except SystemExit:
            print("Passed un-recognized argument check.\n")

        # check auto-correlate without binary
        arg_list = ['--ensemble', os.path.join(test_data_dir, 'workdir.%d'),
                    '--input-files', 'out.cahn_hilliard_50000000.npz',
                    '--output-dir', output_dir,
                    '--output-file', 'out.cahn_hilliard_end_state_PCA.rd.npy',
                    '--algorithm', 'PCA',
                    '--num-dim', '2',
                    '--field-var', 'phase_field',
                    '--auto-correlate',
                    '--over-write']
        try:
            reduce(arg_list)
        except ValueError:
            print ("Passed missing --binary check.\n")
        
        # check csv-out
        arg_list = ['--ensemble', os.path.join(test_data_dir, 'workdir.%d'),
                    '--input-files', 'out.cahn_hilliard_50000000.npz',
                    '--output-dir', output_dir,
                    '--output-file', 'out.cahn_hilliard_end_state_PCA.rd.npy',
                    '--algorithm', 'PCA',
                    '--num-dim', '2',
                    '--field-var', 'phase_field',
                    '--auto-correlate',
                    '--over-write',
                    '--csv-out', 'end-state-PCA-links.csv']
        try:
            reduce(arg_list)
        except SystemExit:
            print("Passed missing --csv-header.\n")

        # check save model file extension
        arg_list = ['--ensemble', os.path.join(test_data_dir, 'workdir.%d'),
                    '--input-files', 'out.cahn_hilliard_50000000.npz',
                    '--output-dir', output_dir,
                    '--output-file', 'out.cahn_hilliard_end_state_PCA_50.rd.npy',
                    '--algorithm', 'PCA',
                    '--field-var', 'phase_field',
                    '--over-write',
                    '--output-model', 'pca-model.txt',
                    '--num-dim', '50']
        try:
            reduce(arg_list)
        except SystemExit:
            print("Passed .pkl extension save model.\n")
        
        # check load model file extension
        arg_list = ['--ensemble', os.path.join(test_data_dir, 'workdir.%d'),
                    '--input-files', 'out.cahn_hilliard_50000000.npz',
                    '--output-dir', output_dir,
                    '--output-file', 'out.cahn_hilliard_end_state_PCA_50.rd.npy',
                    '--algorithm', 'PCA',
                    '--field-var', 'phase_field',
                    '--over-write',
                    '--input-model', 'pca-model.txt',
                    '--num-dim', '50']
        try:
            reduce(arg_list)
        except SystemExit:
            print("Passed .pkl extension load model.\n")

# save/load models
##################

def test_save_load(args):

    if args.test_save_load or args.test_all:

        # save PCA model
        arg_list = ['--ensemble', os.path.join(test_data_dir, 'workdir.%d'),
                    '--input-files', 'out.cahn_hilliard_50000000.npz',
                    '--output-dir', output_dir,
                    '--output-file', 'out.cahn_hilliard_end_state_PCA_10.rd.npy',
                    '--algorithm', 'PCA',
                    '--auto-correlate', '--binary',
                    '--over-write',
                    '--xy-out', 'PCA-end-state-trained.csv',
                    '--xy-header', 'PCA End State',
                    '--output-model', 'end-state-pca-model-10.pkl',
                    '--num-dim', '10']
        reduce(arg_list)
        print()

        # load PCA model with parameters provided
        arg_list = ['--ensemble', os.path.join(test_data_dir, 'workdir.%d'),
                    '--input-files', 'out.cahn_hilliard_50000000.npz',
                    '--output-dir', output_dir,
                    '--output-file', 'out.cahn_hilliard_end_state_PCA_10.rd.npy',
                    '--algorithm', 'PCA',
                    '--over-write',
                    '--input-model', os.path.join(output_dir, 
                        'end-state-pca-model-10.pkl'),
                    '--num-dim', '10']
        try:
            reduce(arg_list)
        except ValueError:
            print("Passed load model with parameter check.\n")

        # load PCA model and run
        arg_list = ['--ensemble', os.path.join(test_data_dir, 'workdir.%d'),
                    '--input-files', 'out.cahn_hilliard_50000000.npz',
                    '--output-dir', output_dir,
                    '--output-file', 'out.cahn_hilliard_end_state_PCA_10.rd.npy',
                    '--over-write',
                    '--auto-correlate', '--binary',
                    '--input-model', os.path.join(output_dir, 
                        'end-state-pca-model-10.pkl'),
                    '--xy-out', 'PCA-end-state-loaded.csv',
                    '--xy-header', 'PCA End State']
        reduce(arg_list)

        # compare trained and loaded models
        if filecmp.cmp(os.path.join(output_dir, 'PCA-end-state-trained.csv'),
            os.path.join(output_dir, 'PCA-end-state-loaded.csv'), shallow=False):
            print("Passed load/save file comparison check.\n")
        else:
            print("Failed load/save file comparison check.\n")

        # save time-aligned model (using only 3 time points)
        arg_list = ['--ensemble', os.path.join(test_data_dir, 'workdir.%d'),
                    '--input-files', 'out.cahn_hilliard_%d[0:1500000].npz',
                    '--output-dir', output_dir,
                    '--output-file', 'out.cahn_hilliard_time_aligned_PCA.rd.npy',
                    '--algorithm', 'PCA',
                    '--num-dim', '2',
                    '--time-align', '10',
                    '--auto-correlate', '--binary',
                    '--over-write',
                    '--file-batch-size', '500',
                    '--output-model', 'PCA-time-aligned.pkl']
        reduce(arg_list)

        # load time-aligned model
        arg_list = ['--ensemble', os.path.join(test_data_dir, 'workdir.%d'),
                    '--input-files', 'out.cahn_hilliard_%d[0:1500000].npz',
                    '--output-dir', output_dir,
                    '--output-file', 'out.cahn_hilliard_time_aligned_PCA_loaded.rd.npy',
                    '--input-model', os.path.join(output_dir, 'PCA-time-aligned.pkl'),
                    '--auto-correlate', '--binary',
                    '--over-write',
                    '--file-batch-size', '500']
        reduce(arg_list)

        # compare trained and loaded model results
        results_same = True
        for i in [7, 15, 18, 20, 27, 33, 34, 37, 39, 40, 43, 44, 49, 
                  50, 57, 62, 65, 68, 71, 76, 81, 86, 92, 95, 98]:
            if not filecmp.cmp(os.path.join(output_dir, 'workdir.' + str(i) + '/out.cahn_hilliard_time_aligned_PCA.rd.npy'),
                os.path.join(output_dir, 'workdir.' + str(i) + '/out.cahn_hilliard_time_aligned_PCA_loaded.rd.npy'), shallow=False):
                results_same = False
        print("Time aligned traied/loaded results same: " + str(results_same))

# end state test reductions
###########################

def test_end_state(args):

    if args.test_end_state or args.test_all:

        # PCA on end state
        arg_list = ['--ensemble', os.path.join(test_data_dir, 'workdir.%d'),
                    '--input-files', 'out.cahn_hilliard_50000000.npz',
                    '--output-dir', output_dir,
                    '--output-file', 'out.cahn_hilliard_end_state_PCA_10.rd.npy',
                    '--algorithm', 'PCA',
                    '--over-write',
                    '--xy-out', 'PCA-end-state-xy.csv',
                    '--xy-header', 'PCA End State',
                    '--csv-out', 'PCA-end-state-links.csv',
                    '--csv-header', 'PCA End State',
                    '--num-dim', '10']
        reduce(arg_list)

        # auto-correlated PCA on end state
        arg_list = ['--ensemble', os.path.join(test_data_dir, 'workdir.%d'),
                    '--input-files', 'out.cahn_hilliard_50000000.npz',
                    '--output-dir', output_dir,
                    '--output-file', 'out.cahn_hilliard_end_state_auto_PCA_10.rd.npy',
                    '--algorithm', 'PCA',
                    '--auto-correlate', '--binary',
                    '--over-write',
                    '--xy-out', 'auto-PCA-end-state-xy.csv',
                    '--xy-header', 'Auto-PCA End State',
                    '--num-dim', '10']
        reduce(arg_list)

        # Isomap on end state
        arg_list = ['--ensemble', os.path.join(test_data_dir, 'workdir.%d'),
                    '--input-files', 'out.cahn_hilliard_50000000.npz',
                    '--output-dir', output_dir,
                    '--output-file', 'out.cahn_hilliard_end_state_Isomap.rd.npy',
                    '--algorithm', 'Isomap',
                    '--over-write',
                    '--xy-out', 'Isomap-end-state-xy.csv',
                    '--xy-header', 'Isomap End State',
                    '--num-dim', '2']
        reduce(arg_list)

        # auto-correlated Isomap on end state
        arg_list = ['--ensemble', os.path.join(test_data_dir, 'workdir.%d'),
                    '--input-files', 'out.cahn_hilliard_50000000.npz',
                    '--output-dir', output_dir,
                    '--output-file', 'out.cahn_hilliard_end_state_auto_Isomap.rd.npy',
                    '--algorithm', 'Isomap',
                    '--auto-correlate', '--binary',
                    '--over-write',
                    '--xy-out', 'auto-Isomap-end-state-xy.csv',
                    '--xy-header', 'Auto-Isomap End State',
                    '--num-dim', '2']
        reduce(arg_list)

        # # tSNE on end state (use PCA output)
        # arg_list = ['--ensemble', os.path.join(output_dir, 'workdir.%d'),
        #             '--input-files', 'out.cahn_hilliard_end_state_PCA_10.rd.npy',
        #             '--output-dir', output_dir,
        #             '--output-file', 'out.cahn_hilliard_end_state_tSNE.rd.npy',
        #             '--algorithm', 'tSNE',
        #             '--over-write',
        #             '--xy-out', 'tSNE-end-state-xy.csv',
        #             '--xy-header', 'tSNE End State',
        #             '--num-dim', '2']
        # reduce(arg_list)

        # # auto-correlated tSNE on end state (using auto-correlated PCA)
        # arg_list = ['--ensemble', os.path.join(output_dir, 'workdir.%d'),
        #             '--input-files', 'out.cahn_hilliard_end_state_auto_PCA_10.rd.npy',
        #             '--output-dir', output_dir,
        #             '--output-file', 'out.cahn_hilliard_end_state_auto_tSNE.rd.npy',
        #             '--algorithm', 'tSNE',
        #             '--auto-correlate', '--binary',
        #             '--over-write',
        #             '--xy-out', 'auto-tSNE-end-state-xy.csv',
        #             '--xy-header', 'Auto-tSNE End State',
        #             '--num-dim', '2']
        # reduce(arg_list)

# UMAP
######

def test_umap(args):

    if args.test_umap or args.test_all:

        # Umap on inc-auto test set
        arg_list = ['--ensemble', os.path.join(output_dir, 'workdir.%d'),
                    '--input-files', 'out.cahn_hilliard_end_state_auto_PCA_10.rd.npy',
                    '--output-dir', output_dir,
                    '--output-file', 'out.cahn_hilliard_umap_10.rd.npy',
                    '--algorithm', 'Umap',
                    '--over-write',
                    '--csv-out', 'umap.csv',
                    '--csv-header', 'Umap',
                    '--num-dim', '10',
                    '--output-model', 'auto-PCA-10-umap.pkl']
        reduce(arg_list)

# auto-encoder
##############

# def test_auto_encoder(args):

#     if args.test_auto_encoder or args.test_all:

#         # auto-encoder on full training set
#         arg_list = ['--ensemble', os.path.join(output_dir, 'workdir.%d'),
#                     '--input-files', 'out.cahn_hilliard_inc_whiten_PCA_1000.rd.npy',
#                     '--output-dir', output_dir,
#                     '--output-file', 'out.cahn_hilliard_inc_whiten_PCA_1000_autoencoder.rd.npy',
#                     '--algorithm', 'auto-encoder',
#                     '--over-write',
#                     '--csv-out', 'inc-whiten-PCA-1000-auto-encoder.csv',
#                     '--csv-header', 'Whiten PCA Auto-Encoder',
#                     '--num-dim', '10',
#                     '--MLP-arch', '750', '500', '250', '100', '50',
#                     '--num-processes', '4',
#                     '--epochs', '100',
#                     '--batch-size', '250',
#                     '--output-model', 'inc-whiten-PCA-1000-autoencoder.pkl']
#         reduce(arg_list)

# betti number algorithm (experimental)
#######################################

# def test_betti(args):

#     if args.test_betti or args.test_all:

#         # check betti arguments
#         arg_list = ['--ensemble', os.path.join(test_data_dir, 'workdir.%d'),
#                     '--input-files', 'out.cahn_hilliard_50000000.npz',
#                     '--output-dir', output_dir,
#                     '--output-file', 'out.cahn_hilliard_end_state_Betti.rd.npy',
#                     '--algorithm', 'Betti',
#                     '--over-write']
#         try:
#             reduce(arg_list)
#         except ValueError:
#             print("Passed --rows Betti number check.\n")
        
#         arg_list += ['--rows', '512']
#         try:
#             reduce(arg_list)
#         except ValueError:
#             print("Passed --cols Betti number check.\n")

#         arg_list += ['--cols', '512']
#         try:
#             reduce(arg_list)
#         except ValueError:
#             print("Passed --threshold Betti number check.\n") 

#         # betti number calculation
#         arg_list = ['--ensemble', os.path.join(test_data_dir, 'workdir.%d'),
#                     '--input-files', 'out.cahn_hilliard_50000000.npz',
#                     '--output-dir', output_dir,
#                     '--output-file', 'out.cahn_hilliard_end_state_Betti.rd.npy',
#                     '--algorithm', 'Betti',
#                     '--over-write',
#                     '--rows', '512',
#                     '--cols', '512',
#                     '--threshold', '0',
#                     '--xy-out', 'Betti-end-state.csv',
#                     '--xy-header', 'Betti End State',
#                     '--num-dim', '2',
#                     '--log-file', 'betti.log']
#         reduce(arg_list)

# time-aligned algorithms
#########################

def test_time_aligned(args):

    if args.test_time_aligned or args.test_all:

        # time-aligned PCA in memory (no --file-batch-size)
        arg_list = ['--ensemble', os.path.join(test_data_dir, 'workdir.%d'),
                    '--input-files', 'out.cahn_hilliard_%d[0:2000000].npz',
                    '--output-dir', output_dir,
                    '--output-file', 'out.cahn_hilliard_time_aligned_PCA.rd.npy',
                    '--algorithm', 'PCA',
                    '--time-align', '10',
                    '--num-dim', '2',
                    '--auto-correlate', '--binary',
                    '--over-write',
                    '--csv-out', 'time-aligned-PCA.csv',
                    '--csv-header', 'Time Aligned PCA']
        reduce(arg_list)
        print("Passed time-aligned in memory.\n")

        # time-aligned PCA in batch using fit (--file-batch-size == size ensemble)
        arg_list = ['--ensemble', os.path.join(test_data_dir, 'workdir.%d'),
                    '--input-files', 'out.cahn_hilliard_%d[0:2000000].npz',
                    '--output-dir', output_dir,
                    '--output-file', 'out.cahn_hilliard_time_aligned_PCA.rd.npy',
                    '--algorithm', 'PCA',
                    '--time-align', '10',
                    '--num-dim', '2',
                    '--auto-correlate', '--binary',
                    '--over-write',
                    '--file-batch-size', '50',
                    '--csv-out', 'time-aligned-PCA.csv',
                    '--csv-header', 'Time Aligned PCA']
        reduce(arg_list)
        print("Passed time-aligned non-incremental.\n")

        # # time-aligned PCA using incremental in batches
        # arg_list = ['--ensemble', os.path.join(test_data_dir, 'workdir.%d'),
        #             '--input-files', 'out.cahn_hilliard_%d[0:2000000].npz',
        #             '--output-dir', output_dir,
        #             '--output-file', 'out.cahn_hilliard_time_aligned_PCA.rd.npy',
        #             '--algorithm', 'incremental-PCA',
        #             '--time-align', '10',
        #             '--num-dim', '2',
        #             '--auto-correlate', '--binary',
        #             '--over-write',
        #             '--file-batch-size', '20',
        #             '--csv-out', 'time-aligned-PCA.csv',
        #             '--csv-header', 'Time Aligned PCA']
        # reduce(arg_list)
        # print("Passed time-aligned incremental in batches.\n")

# all time step algorithms
##########################

def test_all_time(args):

    if args.test_all_time or args.test_all:

        # incremental PCA
        arg_list = ['--ensemble', os.path.join(test_data_dir, 'workdir.%d'),
                    '--input-files', 'out.cahn_hilliard_%d.npz',
                    '--output-dir', output_dir,
                    '--output-file', 'out.cahn_hilliard_inc_whiten_PCA_1000.rd.npy',
                    '--algorithm', 'incremental-PCA',
                    '--whiten',
                    '--over-write',
                    '--csv-out', 'incremental-whiten-PCA-1000.csv',
                    '--csv-header', 'Incremental Whiten PCA',
                    '--num-dim', '1000',
                    '--file-batch-size', '1500',
                    '--output-model', 'inc-whiten-PCA-1000.pkl']
        reduce(arg_list)

# parallel testing
##################

def test_parallel(args):

    if args.test_parallel or args.test_all:

        # test parallel
        arg_list = ['--ensemble', os.path.join(test_data_dir, 'workdir.%d'),
                    '--input-files', 'out.cahn_hilliard_50000000.npz',
                    '--output-dir', output_dir,
                    '--output-file', 'out.cahn_hilliard_end_state_auto_PCA_10.rd.npy',
                    '--algorithm', 'PCA',
                    '--auto-correlate', '--binary',
                    '--over-write',
                    '--parallel',
                    '--xy-out', 'auto-PCA-end-state-parallel-xy.csv',
                    '--xy-header', 'Auto-PCA End State',
                    '--num-dim', '10',
                    '--log-file', os.path.join(output_dir, 'auto-PCA-parallel.log')]
        reduce(arg_list)
    
        # compare to serial
        arg_list = ['--ensemble', os.path.join(test_data_dir, 'workdir.%d'),
                    '--input-files', 'out.cahn_hilliard_50000000.npz',
                    '--output-dir', output_dir,
                    '--output-file', 'out.cahn_hilliard_end_state_auto_PCA_10.rd.npy',
                    '--algorithm', 'PCA',
                    '--auto-correlate', '--binary',
                    '--over-write',
                    '--xy-out', 'auto-PCA-end-state-serial-xy.csv',
                    '--xy-header', 'Auto-PCA End State',
                    '--num-dim', '10']
        reduce(arg_list)

        # compare parallel/serial models
        if filecmp.cmp(os.path.join(output_dir, 'auto-PCA-end-state-serial-xy.csv'),
            os.path.join(output_dir, 'auto-PCA-end-state-parallel-xy.csv'), shallow=False):
            print("Passed serial/parallel file comparison check.\n")
        else:
            print("Failed serial/parallel file comparison check " +
                  "(sometimes this is due to precision errors).\n")

# restart testing
#################

def test_restart(args):

    if args.test_restart or args.test_all:

        # restart testing (must be pickle file)
        arg_list = ['--ensemble', os.path.join(test_data_dir, 'workdir.%d'),
                    '--input-files', 'out.cahn_hilliard_50000000.npz',
                    '--output-dir', output_dir,
                    '--output-file', 'out.cahn_hilliard_inc_auto_PCA_10.rd.npy',
                    '--algorithm', 'incremental-PCA',
                    '--auto-correlate', '--binary',
                    '--over-write',
                    '--restart', 'restart.txt',
                    '--num-dim', '10',
                    '--file-batch-size', '1000']
        try:
            reduce(arg_list)
        except SystemExit:
            print("Passed --restart file.pkl check.\n")

        # test for --output-model
        arg_list = ['--ensemble', os.path.join(test_data_dir, 'workdir.%d'),
                    '--input-files', 'out.cahn_hilliard_50000000.npz',
                    '--output-dir', output_dir,
                    '--output-file', 'out.cahn_hilliard_inc_auto_PCA_10.rd.npy',
                    '--algorithm', 'incremental-PCA',
                    '--auto-correlate', '--binary',
                    '--over-write',
                    '--restart', 'restart.pkl',
                    '--num-dim', '10',
                    '--file-batch-size', '1000']
        try:
            reduce(arg_list)
        except SystemExit:
            print("Passed --restart --output-model check.\n")

# test reduction using rd.npy load
def test_rd_npy(args):

    if args.test_rd_npy or args.test_all:

        # check if inc-auto PCA has already been computed
        if not os.path.exists(os.path.join(output_dir, 
            'workdir.1/out.cahn_hilliard_inc_auto_PCA_100.rd.npy')):

            # compute .rd.npy on test data using inc-auto PCA
            arg_list = ['--ensemble', os.path.join(test_data_dir, 'workdir.%d'),
                '--input-files', 'out.cahn_hilliard_%d.npz',
                '--output-dir', output_dir,
                '--output-file', 'out.cahn_hilliard_inc_auto_PCA_100.rd.npy',
                '--algorithm', 'incremental-PCA',
                '--auto-correlate', '--binary',
                '--over-write',
                '--num-dim', '100',
                '--file-batch-size', '2000']
            reduce(arg_list)

        # compute time-aligned PCA using inc-auto PCA
        arg_list = ['--ensemble', os.path.join(output_dir, 'workdir.%d'),
                    '--input-files', 'out.cahn_hilliard_inc_auto_PCA_100.rd.npy',
                    '--output-dir', output_dir,
                    '--output-file', 'out.cahn_hilliard_time_aligned_PCA.rd.npy',
                    '--algorithm', 'PCA',
                    '--time-align', '20',
                    '--num-dim', '10',
                    '--over-write',
                    '--output-model', 'time-aligned-PCA.pkl']
        reduce(arg_list)        
        print("Finished training time-aligned PCA model.\n")

        # test rd.npy from loaded model
        arg_list = ['--ensemble', os.path.join(output_dir, 'workdir.%d'),
                    '--input-files', 'out.cahn_hilliard_inc_auto_PCA_100.rd.npy', 
                    '--output-dir', output_dir,
                    '--output-file', 'out.cahn_hilliard_time_aligned_model_PCA.rd.npy',
                    '--input-model', os.path.join(output_dir, 'time-aligned-PCA.pkl'),
                    '--over-write']
        reduce(arg_list)

if __name__ == "__main__":

    # get command line flags
    parser = init_parser()
    args = parser.parse_args()

    # delete output directory, if requested
    delete_output_dir(args)

    # check if there are any tests
    if not (args.test_UI or \
            args.test_save_load or \
            args.test_time_aligned or \
            args.test_all_time or \
            args.test_umap or \
            # args.test_auto_encoder or \
            args.test_parallel or \
            args.test_restart or \
            args.test_rd_npy or \
            args.test_all):
        print("No tests were selected.")

    # run tests
    test_UI(args)
    test_save_load(args)
    test_end_state(args)
    test_time_aligned(args)
    test_all_time(args)
    # test_betti(args)
    test_umap(args)
    # test_auto_encoder(args)
    test_parallel(args)
    test_restart(args)
    test_rd_npy(args)