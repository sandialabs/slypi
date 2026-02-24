# Copyright (c) 2013, 2018 National Technology and Engineering Solutions of Sandia, LLC . Under the terms of Contract
# DE-NA0003525 with National Technology and Engineering Solutions of Sandia, LLC, the U.S. Government
# retains certain rights in this software.

# This script lists the members in a given project

import pprint
import slypi

# command line entry point
if __name__ == "__main__":

    # get arguments for connecting to Slycat server
    parser = slypi.ArgumentParser(
        description="List users for a given project.")
    
    # get either pid or name
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--project-name', help='Project name to retrieve.')
    group.add_argument('--pid', help='Project ID to retrieve.')

    arguments = parser.parse_args()

    # connect and get project
    connection = slypi.connect(arguments)
    if arguments.pid:
        project = connection.get_project(arguments.pid)
    elif arguments.project_name:
        project = connection.find_project(arguments.project_name)

    # list members
    pprint.pprint(project['acl'])