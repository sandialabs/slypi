#!/bin/env python
# Copyright (c) 2013, 2018 National Technology and Engineering Solutions of Sandia, LLC . Under the terms of Contract
# DE-NA0003525 with National Technology and Engineering Solutions of Sandia, LLC, the U.S. Government
# retains certain rights in this software.

import pprint
import slypi

parser = slypi.ArgumentParser("Get details of project from Slycat server.")

# get either pid or name
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--project-name', help='Project name to retrieve.')
group.add_argument('--pid', help='Project ID to retrieve.')

arguments = parser.parse_args()

connection = slypi.connect(arguments)
if arguments.pid:
    project = connection.get_project(arguments.pid)
elif arguments.project_name:
    project = connection.find_project(arguments.project_name)
pprint.pprint(project)
