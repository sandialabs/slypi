# This is a script to test the csv utitlies using the
# memphis test data.  Tests csv operations create, join, and expand.
#
# WARNING: When this script is run, the output_dir is
# deleted, unless delete_output_dir is set to False.

# Copyright (c) 2021 National Technology and Engineering Solutions of Sandia, LLC.  
# Under the terms of Contract DE-NA0003525 with National Technology and Engineering 
# Solutions of Sandia, LLC, the U.S. Government retains certain rights in this software.

# NOTE: To test the --join option, you must first run test-reduce.py
# with the end-state option to create the xy-out .csv files to join.

# S. Martin
# 3/23/2021

# file/path manipulation
import os
import shutil

# table code
from slypi.ensemble.table import table
from slypi.ensemble.table import join_csv
from slypi.ensemble.table import convert_uris
from slypi.ensemble import ArgumentError

# delete output_dir
delete_output_dir = True

# directory containing the phase-field test dataset
test_data_dir = os.path.join('example-data', 'spinodal')

# output directory to use for testing
output_dir = os.path.join('example-data', 'spinodal-out', 'test_table')

# convert directory containing end state images and movies
convert_dir = os.path.join('example-data', 'spinodal-out', 'test-convert')

# reduce directory containing the end state reductions
reduce_dir = os.path.join('example-data', 'spinodal-out', 'test_reduce')

# uri-root-out conversion (location of files on cluster)
uri_root_out = 'file://test/spindoal-out'

# delete output_dir, if present
if delete_output_dir:
    if os.path.isdir(output_dir):
        shutil.rmtree(output_dir)

# test UI
#########

# check for no arguments
arg_list = []
try:
    table(arg_list)
except ArgumentError:
    print("Passed no argument check.\n")

# check output-dir
arg_list = ['--create']
try:
    table(arg_list) 
except ArgumentError:
    print("Passed create --output-dir check.\n")

# check for --csv-out
arg_list = ['--create',
            '--output-dir', output_dir]
try:
    table(arg_list)
except ArgumentError:
    print("Passed --output-file check.\n")

# check for multiple competing requests (create & join)
arg_list = ['--create',
            '--output-dir', output_dir,
            '--output-file', 'out.csv',
            '--join', 'join.csv']
try:
    table(arg_list)
except SystemExit:
    print("Passed --join too many arguments check.\n")

# check create --ensemble argument
arg_list = ['--create',
            '--output-dir', output_dir,
            '--output-file', 'out.csv']
try:
    table(arg_list)
except ArgumentError:
    print("Passed create --ensemble check.\n")

# check create --input-files
arg_list = ['--create',
            '--output-dir', output_dir,
            '--output-file', 'out.csv',
            '--ensemble', os.path.join(test_data_dir, 'workdir.%d')]
try:
    table(arg_list)
except ArgumentError:
    print("Passed create --input-files check.\n")

# check create --input-header
arg_list = ['--create',
            '--output-dir', output_dir,
            '--output-file', 'out.csv',
            '--ensemble', os.path.join(test_data_dir, 'workdir.%d'),
            '--input-files', 'in.cahn_hilliard']
try:
    table(arg_list)
except ArgumentError:
    print("Passed create --input-header check.\n")

# check join one file
arg_list = ['--join', 'in.csv',
            '--output-dir', output_dir,
            '--output-file', 'out.csv']
try:
    table(arg_list)
except ArgumentError:
    print("Passed join check.\n")

# check join with --ignore-index
arg_list = ['--join', 'in.csv',
            '--output-dir', output_dir,
            '--output-file', 'out.csv',
            '--ensemble', os.path.join(test_data_dir, 'workdir.%d'),
            '--input-files', 'in.cahn_hilliard',
            '--input-header', 'VTK Files',
            '--ignore-index']
try:
    table(arg_list)
except ArgumentError:
    print("Passed --join --output-no-index missing.\n")    

# check join with uri conversion
arg_list = ['--join', 'in.csv',
            '--output-dir', output_dir,
            '--ensemble', os.path.join(test_data_dir, 'workdir.%d'),
            '--input-files', 'in.cahn_hilliard',
            '--input-header', 'VTK Files',
            '--output-file', 'out.csv',
            '--convert-uri-cols', 'foo', 'bar']
try:
    table(arg_list)
except SystemExit:
    print("Passed --join --convert-uri-cols combination.\n")

# check join with --convert-cols missing
# (this option is no longer supported)
# arg_list = ['--join', 'in.csv',
#             '--output-dir', output_dir,
#             '--ensemble', os.path.join(test_data_dir, 'workdir.%d'),
#             '--input-files', 'in.cahn_hilliard',
#             '--input-header', 'VTK Files',
#             '--output-file', 'out.csv',
#             '--uri-root-out', 'uri-out.csv']
# try:
#     table(arg_list)
# except SystemExit:
#     print("Passed --join --convert-cols missing.\n")

# check expand with no --expand-header option
arg_list = ['--expand', 'metadata.csv',
            '--output-dir', output_dir,
            '--output-file', 'expand-default.csv']
try:
    table(arg_list)
except ArgumentError:
    print("Passed --expand-header check.\n")

# check convert-uris with no --uri-root or --uri-cols
arg_list = ['--convert-uris', 'metadata.csv',
            '--output-dir', output_dir,
            '--output-file', 'convert-uris.csv']
try:
    table(arg_list)
except ArgumentError:
    print("Passed --convert-uris without --uri-root and --uri-cols check.\n")

# check convert-uris with no --uri-root, but with --uri-cols
arg_list = ['--convert-uris', 'metadata.csv',
            '--output-dir', output_dir,
            '--output-file', 'convert-uris.csv',
            '--uri-cols', 'foo', 'bar']
try:
    table(arg_list)
except ArgumentError:
    print("Passed --convert-uris without --uri-root check.\n")

# check convert-uris with no --uri-cols, but with --uri-root
arg_list = ['--convert-uris', 'metadata.csv',
            '--output-dir', output_dir,
            '--output-file', 'convert-uris.csv',
            '--uri-root', 'file:/path']
try:
    table(arg_list)
except ArgumentError:
    print("Passed --convert-uris without --uri-cols check.\n")

# join csv testing
##################

# test join end-state and movies (parameter space model)
arg_list = ['--join', 
            os.path.join(test_data_dir, 'metadata.csv'),
            os.path.join(convert_dir, 'end-state.csv'),
            os.path.join(convert_dir, 'movies.csv'),
            '--output-dir', output_dir,
            '--output-file', 'ps.csv',
            '--over-write',
            '--output-no-index',
            '--output-headers', 
            'mobility_coefficients-1', 'mobility_coefficients-2', 
            'composition_distribution-1', 'End State', 'Movie']
table(arg_list)
print("Created ps.csv.\n")

# test join end-state and movies (with ignore index)
arg_list = ['--join', 
            os.path.join(test_data_dir, 'metadata.csv'),
            os.path.join(convert_dir, 'end-state.csv'),
            os.path.join(convert_dir, 'movies.csv'),
            '--output-dir', output_dir,
            '--output-file', 'ps-ignore-index.csv',
            '--over-write',
            '--output-no-index',
            '--ignore-index', 
            '--output-headers', 
            'mobility_coefficients-1', 'mobility_coefficients-2', 
            'composition_distribution-1', 'End State', 'Movie']
table(arg_list)
print("Created ps-ignore-index.csv.\n")

# test join end-state and movies (no index join)
arg_list = ['--join', 
            os.path.join(test_data_dir, 'metadata.csv'),
            os.path.join(convert_dir, 'end-state.csv'),
            os.path.join(convert_dir, 'movies.csv'),
            '--output-dir', output_dir,
            '--output-file', 'ps-no-index.csv',
            '--over-write',
            '--no-index',
            '--output-headers', 
            'mobility_coefficients-1', 'mobility_coefficients-2', 
            'composition_distribution-1', 'End State', 'Movie']
table(arg_list)
print("Created ps-no-index.csv.\n")

# test join end-state and movies (no index join) with .sly extension
arg_list = ['--join', 
            os.path.join(test_data_dir, 'metadata.csv'),
            os.path.join(convert_dir, 'end-state.csv'),
            os.path.join(convert_dir, 'movies.csv'),
            '--output-dir', output_dir,
            '--output-file', 'ps-no-index.sly',
            '--over-write',
            '--no-index',
            '--output-headers', 
            'mobility_coefficients-1', 'mobility_coefficients-2', 
            'composition_distribution-1', 'End State', 'Movie']
table(arg_list)
print("Created ps-no-index.sly.\n")

# test join using API
join_csv (join_tables=[os.path.join(test_data_dir, 'metadata.csv'), 
           os.path.join(convert_dir, 'end-state.csv'),
           os.path.join(convert_dir, 'movies.csv')],
           output_headers=['mobility_coefficients-1', 'mobility_coefficients-2', 
           'composition_distribution-1', 'End State', 'Movie'],
           output_dir=output_dir, output_file='ps-no-index-api.csv',
           no_index=True)
print("Created ps-no-index-api.csv.\n")

# test uri-convert
arg_list = ['--convert-uris', 
            os.path.join(output_dir, 'ps-no-index.sly'),
            '--output-dir', output_dir,
            '--output-file', 'ps-uri-convert.csv',
            '--over-write',
            '--uri-cols', 'End State', 'Movie',
            '--uri-root', uri_root_out]
table(arg_list)
print("Created ps-uri-convert.csv.\n")

# test convert_uris API version
convert_uris(os.path.join(output_dir, 'ps-no-index.sly'),
             uri_cols=['End State', 'Movie'],
             uri_root=uri_root_out,
             output_dir=output_dir, 
             output_file='ps-uri-convert-api.csv')
print("Created ps-uri-convet-api.csv\n")
    
# test join one file and non-existing file links
arg_list = ['--join',
            os.path.join(test_data_dir, 'metadata.csv'),
            '--ensemble', os.path.join(test_data_dir, 'workdir.%d'),
            '--input-files', 'out.cahn_hilliard_%d.jpg',
            '--input-header', 'Images',
            '--output-dir', output_dir,
            '--output-file', 'metadata-images.csv',
            '--ignore-index',
            '--output-no-index',
            '--over-write']
table(arg_list)
print("Created metadata-images.csv.\n")

# test join one file and existing file links
arg_list = ['--join',
            os.path.join(test_data_dir, 'metadata.csv'),
            '--ensemble', os.path.join(test_data_dir, 'workdir.%d'),
            '--input-files', 'out.cahn_hilliard_%d.vtk',
            '--input-header', 'Images',
            '--output-dir', output_dir,
            '--output-file', 'metadata-meshes.csv',
            '--ignore-index',
            '--output-no-index',
            '--over-write']
table(arg_list)
print("Created metadata-meshes.csv.\n")

# join all end-state xy coords
arg_list = ['--join',
            os.path.join(test_data_dir, 'metadata.csv'),
            os.path.join(convert_dir, 'end-state.csv'),
            os.path.join(convert_dir, 'movies.csv'),
            os.path.join(reduce_dir, 'PCA-end-state-xy.csv'),
            os.path.join(reduce_dir, 'auto-PCA-end-state-xy.csv'),
            os.path.join(reduce_dir, 'Isomap-end-state-xy.csv'),
            os.path.join(reduce_dir, 'auto-Isomap-end-state-xy.csv'),
            '--output-dir', output_dir,
            '--output-file', 'ps-PCA-Isomap-tSNE-end-state.csv',
            '--output-no-index',
            '--ignore-index',
            '--over-write']
            #'--uri-root-out', uri_root_out,
            #'--convert-cols', 'End State', 'Movie']
table(arg_list)
print("Created ps-PCA-Isomap-tSNE-end-state.csv.\n")

# join one file and dimension reduction links
# (for testing videoswarm expansion option later)
arg_list = ['--join',
            os.path.join(test_data_dir, 'metadata.csv'),
            os.path.join(convert_dir, 'end-state.csv'),
            os.path.join(convert_dir, 'movies.csv'),
            os.path.join(reduce_dir, 'time-aligned-PCA.csv'),
            '--output-dir', output_dir,
            '--output-file', 'metadata-time-aligned-PCA.csv',
            '--output-no-index',
            '--over-write',
            '--ignore-index',
            '--output-headers',
            'mobility_coefficients-1', 'mobility_coefficients-2', 
            'composition_distribution-1', 'End State', 'Movie', 'Time Aligned PCA']
            #'--uri-root-out', uri_root_out,
            #'--convert-cols', 'End State', 'Movie']
table(arg_list)
print("Created metadata-time-aligned.csv.\n")

# # join Betti end-state dimension reduction
# arg_list = ['--join',
#             os.path.join(test_data_dir, 'metadata.csv'),
#             os.path.join(convert_dir, 'end-state.csv'),
#             os.path.join(convert_dir, 'movies.csv'),
#             '--output-dir', output_dir,
#             '--csv-out', 'metadata-Betti-end-state.csv',
#             '--csv-no-index',
#             '--ignore-index',
#             '--over-write',
#             '--csv-headers', 
#             'mobility_coefficients-1', 'mobility_coefficients-2', 
#             'composition_distribution-1', 'End State', 'Movie', 
#             '--uri-root-out', uri_root_out,
#             '--convert-cols', 'End State', 'Movie']
# table(arg_list)
# print("Created Betti-end-state.csv.\n")

# join incremental auto-PCA with all time points
arg_list = ['--join',
            os.path.join(test_data_dir, 'metadata.csv'),
            os.path.join(convert_dir, 'end-state.csv'),
            os.path.join(convert_dir, 'movies.csv'),
            os.path.join(reduce_dir, 'incremental-whiten-PCA-1000.csv'),
            '--output-dir', output_dir,
            '--output-file', 'metadata-inc-auto-PCA.csv',
            '--over-write',
            '--ignore-index',
            '--output-no-index']
            #'--uri-root-out', uri_root_out,
            #'--convert-cols', 'End State', 'Movie']
table(arg_list)
print("Created metadata-inc-PCA.csv.\n")

# expand csv testing
####################

# test file expansion with invalid links
arg_list = ['--expand', os.path.join(output_dir, 'metadata-images.csv'),
            '--expand-header', 'Images',
            '--output-dir', output_dir,
            '--output-file', 'metadata-expand-files.csv']
try:
    table(arg_list)
except SystemExit:
    print("Passed missing files check.\n")

# test parameter space number of coordinates > 1
arg_list = ['--expand', os.path.join(output_dir, 'metadata-inc-auto-PCA.csv'),
            '--expand-header', 'Incremental Auto-PCA',
            '--output-dir', output_dir,
            '--output-file', os.path.join(output_dir, 'ps-inc-auto-PCA.csv'),
            '--plugin', 'ps',
            '--num-coords', '0']
try:
    table(arg_list)
except ValueError:
    print("Passed number coordinates check.\n")

# test parameter space expansion (using full PCA dataset)
arg_list = ['--expand', os.path.join(output_dir, 'metadata-inc-auto-PCA.csv'),
            '--expand-header', 'Incremental Whiten PCA',
            '--output-dir', output_dir,
            '--output-file', 'ps-inc-PCA.csv',
            '--plugin', 'ps',
            '--remove-expand-col',
            '--include-original-index',
            '--num-coords', '3',
            '--output-no-index']
table(arg_list)
print("Created ps-inc-PCA.csv.\n")

# test parameter space expansion (using full auto-PCA dataset)
arg_list = ['--expand', os.path.join(output_dir, 'metadata-inc-auto-PCA.csv'),
            '--expand-header', 'Incremental Whiten PCA',
            '--output-dir', output_dir,
            '--output-file', 'ps-inc-auto-PCA.csv',
            '--plugin', 'ps',
            '--remove-expand-col',
            '--include-original-index',
            '--num-coords', '3',
            '--output-no-index',
            '--over-write']
table(arg_list)
print("Created ps-inc-auto-PCA.csv.\n")

# test videoswarm --video-duration parameter < 0
arg_list = ['--expand', os.path.join(output_dir, 'metadata-time-aligned-PCA.csv'),
            '--expand-header', 'Time Aligned PCA',
            '--output-dir', os.path.join(output_dir, 'videoswarm-out'),
            '--output-file', 'videoswarm.csv',
            '--plugin', 'vs',
            '--remove-expand-col',
            '--video-fps', '-1']
try:
    table(arg_list)
except ValueError:
    print("Passed --video-duration negative check.\n")

# test videoswarm required output-format
arg_list = ['--expand', os.path.join(output_dir, 'metadata-time-aligned-PCA.csv'),
            '--expand-header', 'Time Aligned PCA',
            '--output-dir', os.path.join(output_dir, 'time-aligned-PCA-vs'),
            '--output-file', 'videoswarm.csv',
            '--plugin', 'vs',
            '--remove-expand-col',
            '--video-fps', '25']
table(arg_list)
print("Created time-aligned-PCA-vs files.\n")
