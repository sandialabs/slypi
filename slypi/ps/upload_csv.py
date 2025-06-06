# Copyright (c) 2013, 2018 National Technology and Engineering Solutions of Sandia, LLC . Under the terms of Contract
# DE-NA0003525 with National Technology and Engineering Solutions of Sandia, LLC, the U.S. Government
# retains certain rights in this software.

# This script reads and processes a .csv file before pushing it to the Slycat server
# as a parameter space model.

import os
import re
import sys

import numpy as np

import slypi
import urllib.parse as urlparse

# slycat csv parser
import slypi.pandas_util

# parse command line arguments
def parser():

  parser = slypi.ArgumentParser(description=
    "Create Slycat Parameter Space model from .csv table.")

  # input file
  parser.add_argument("file", help="Input CSV file.")

  # input/output columns
  parser.add_argument("--input-columns", default=[], nargs="*", 
    help="Input column names, can't be media columns.")
  parser.add_argument("--output-columns", default=[], nargs="*", 
    help="Output column names, can't be media columns.")
  parser.add_argument("--categorical-columns", default=[], nargs="*",
    help="Categorical column names, can't be media coluns.")

  # media columns
  parser.add_argument("--media-columns", default=None, nargs="*", 
    help="Columns that contain media URLs.")
  parser.add_argument("--media-hostname", default=None, 
    help="Optionally override the hostname for media columns.")
  parser.add_argument("--strip", type=int, default=None, 
    help="Optionally strip N prefix directories from the stored URLs.")

  # model and project names/descriptions
  parser.add_argument("--marking", default="mna", 
      help="Marking type.  Default: %(default)s")
  parser.add_argument("--model-description", default="", 
      help="New model description.  Default: %(default)s")
  parser.add_argument("--model-name", default="SlyPI PS Model", 
      help="New model name.  Default: %(default)s")
  parser.add_argument("--project-description", default="", 
      help="New project description.  Default: %(default)s")
  
  # require either project name or project ID
  group = parser.add_mutually_exclusive_group(required=True)
  group.add_argument("--project-name", help="Project name (will create if doesn't exist).")
  group.add_argument("--project-id", help="Project ID.")

  # debug mode prints full stack trace
  parser.add_argument("--debug", action="store_true")

  return parser

# logging is just printing to the screen
# in case of failure exit gracefully unless in debug mode
def log (msg, debug=False, exception_type=None):
    
    print(msg)

    if exception_type:

      if debug:
        raise exception_type(msg)
      else:
        sys.exit(1)

# create PS model, arguments include the command line connection parameters
# and project/model information
def upload_model (arguments, attributes, dimensions, data):

  # get column names/types
  column_names = [attribute["name"] for attribute in attributes]

  # setup a connection to the Slycat Web Server.
  connection = slypi.connect(arguments)

  # create a new project to contain our model.
  if arguments.project_name:
    try:
      pid = connection.find_or_create_project(arguments.project_name, arguments.project_description)
    except Exception as e:
      log('Could not find/create project: use a different name, or try a project id.', 
        debug = arguments.debug, exception_type=Exception)
  else:
    pid = arguments.project_id

  # create the new, empty model.
  try:
    mid = connection.post_project_models(pid, "parameter-image", 
      arguments.model_name, arguments.marking, arguments.model_description)
  except Exception as e:
    log('Could not create a new model: is project id correct?', debug=arguments.debug,
      exception_type=Exception)

  # Upload our observations as "data-table".
  connection.put_model_arrayset(mid, "data-table")

  # Start our single "data-table" array.
  connection.put_model_arrayset_array(mid, "data-table", 0, dimensions, attributes)

  # Upload each column into the array.
  for index in range(len(column_names)):
    values = [np.asarray(data[index])]

    # push to server
    connection.put_model_arrayset_data(mid, "data-table", "0/%s/..." % index, values)

  # Store the remaining parameters.
  input_col_inds = [index for index, header in enumerate(column_names) 
    if header in arguments.input_columns]
  connection.put_model_parameter(mid, "input-columns", input_col_inds)
  output_col_inds = [index for index, header in enumerate(column_names) 
    if header in arguments.output_columns]
  connection.put_model_parameter(mid, "output-columns", output_col_inds)
  cat_col_inds = [index for index, header in enumerate(column_names) 
    if header in arguments.categorical_columns]
  connection.put_model_parameter(mid, "category-columns", cat_col_inds)
  media_col_inds = [index for index, header in enumerate(column_names) 
    if header in arguments.media_columns]
  connection.put_model_parameter(mid, "image-columns", media_col_inds)

  # Signal that we're done uploading data to the model.  This lets Slycat Web
  # Server know that it can start computation.
  connection.post_model_finish(mid)

  # Wait until the model is ready.
  connection.join_model(mid)

  return mid

# check arguments and create model, returns URL to model
def create_model (arguments, log):

  # check that input file exists
  if not os.path.isfile(arguments.file):
    log("Input file " + arguments.file + " does not exist.", debug=arguments.debug,
      exception_type=ValueError)

  # check that input/output columns are non-intersecting
  if set(arguments.input_columns).intersection(set(arguments.output_columns)):
    log("Input columns and output columns are intersecting.", debug=arguments.debug,
      exception_type=ValueError)

  # parse file using standard slycat csv parser
  attributes, dimensions, data, csv_read_error = \
    slypi.pandas_util.parse_file(arguments.file, file_name=True)

  # check for warnings/errors
  for i in range(len(csv_read_error)):
    if csv_read_error[i]["type"] == "warning":
      log("Warning: " + csv_read_error[i]["message"])
    else:
      log("Error: " + csv_read_error[i]["message"], debug=arguments.debug, 
        exception_type=ValueError)

  # get column names/types
  column_names = [attribute["name"] for attribute in attributes]
  column_types = [attribute["type"] for attribute in attributes]

  # check that inputs are in headers
  if arguments.input_columns is not None:
    for input_col in arguments.input_columns:
      if input_col not in column_names:
        log('Input column "' + input_col + '" not found in input file.', debug=arguments.debug,
          exception_type=ValueError)

  # check that outputs are in headers
  if arguments.output_columns is not None:
    for output_col in arguments.output_columns:
      if output_col not in column_names:
        log('Output column "' + output_col + '" not found in input file.', debug=arguments.debug,
          exception_type=ValueError)
  
  # check that categorical columns are in headers
  if arguments.categorical_columns is not None:
    for cat_col in arguments.categorical_columns:
      if cat_col not in column_names:
        log('Categorical column "' + cat_col + '" not found in input file.', debug=arguments.debug,
          exception_type=ValueError)
 
  # check that media-columns are in headers
  if arguments.media_columns is not None:
    for media_col in arguments.media_columns:
      if media_col not in column_names:
        log('Media column "' + media_col + '" not found in input file.', debug=arguments.debug,
          exception_type=ValueError)

  # check that there is at least one numeric columns (to display scatter plot)
  if not 'float64' in column_types:
    log("You must supply at least one numeric column in the input data.", debug=arguments.debug,
      exception_type=ValueError)

  # identify media columns automatically if not provided
  if arguments.media_columns is None:
    arguments.media_columns = []

    # search for "file://"
    expression = re.compile("file://")
    search = np.vectorize(lambda x:bool(expression.search(x)))

    # go through each column
    for header in range(len(column_names)):

      # strings are stored in pandas object type
      if column_types[header] == "string":
        if np.any(search(data[header])):
          arguments.media_columns.append(column_names[header])

  # replace media URL hostnames, if requested
  if arguments.media_hostname is not None:
    
    # go through each column
    for header in range(len(column_names)):

      # if media column is given and a string
      if column_names[header] in arguments.media_columns and \
         column_types[header] == "string":
        modified = []

        # replace file://cluster with file://hostname
        for uri in data[header]:
          uri = urlparse.urlparse(uri)
          path = uri.path
          uri = "file://%s%s" % (arguments.media_hostname, path)
          modified.append(uri)
        data[header] = modified

  # strip prefix directories, if requested
  if arguments.strip is not None:

    # go through each column:
    for header in range(len(column_names)):

      # for media columns, strip prefix directories
      if column_names[header] in arguments.media_columns and \
         column_types[header] == "string":
        modified = []

        # strip prefixes
        for uri in df[header].values:
          uri = urlparse.urlparse(uri)
          hostname = uri.netloc
          path = os.path.join(*([os.path.abspath(os.path.dirname(arguments.file))] + 
            uri.path.split(os.sep)[arguments.strip + 1:]))
          uri = "file://%s%s" % (hostname, path)
          modified.append(uri)
        data[header] = modified

  # echo inputs to user
  log('Input file: ' + arguments.file)
  if arguments.input_columns is not None:
    log('Input columns: ' + str(arguments.input_columns))
  if arguments.output_columns is not None:
    log('Output columns: ' + str(arguments.output_columns))
  if arguments.categorical_columns is not None:
    log('Categorical columns: ' + str(arguments.categorical_columns))
  if arguments.media_columns != []:
    log('Media columns: ' + str(arguments.media_columns))
  if arguments.media_hostname is not None:
    log('Media hostname: ' + str(arguments.media_hostname))
  if arguments.strip is not None:
    log('Stripped ' + str(arguments.strip) + ' prefixes from media columns.')

  # upload model
  mid = upload_model (arguments, attributes, dimensions, data)

  # supply direct link to model
  host = arguments.host
  if arguments.port:
      host = host + ":" + arguments.port
  url = host + "/models/" + mid
  log("Your new model is located at %s" % url)
  log('***** PS Model Successfully Created *****')

  # return url
  return url

# main entry point
def main():

    # set up argument parser
    ps_parser = parser()  

    # get user arguments
    arguments = ps_parser.parse_args()

    # check arguments and create model
    url = create_model(arguments, log)

# command line version
if __name__ == "__main__":

    main()