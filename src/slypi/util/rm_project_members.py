# Copyright (c) 2013, 2018 National Technology and Engineering Solutions of Sandia, LLC . Under the terms of Contract
# DE-NA0003525 with National Technology and Engineering Solutions of Sandia, LLC, the U.S. Government
# retains certain rights in this software.

# This script adds members to a given project

import slypi

# check if member is in project
def check_membership (member, acl):
    
    user = {'user': member}
    if user in acl['administrators']:
        return 'administrators'
    
    if user in acl['writers']:
        return 'writers'
    
    if user in acl['readers']:
        return 'readers'

    return None

# command line entry point
if __name__ == "__main__":

    # get arguments for connecting to Slycat server
    parser = slypi.ArgumentParser(
        description="Remove users from a given project.")
    
    # get either pid or name
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--project-name', help='Project name to retrieve.')
    group.add_argument('--pid', help='Project ID to retrieve.')

    # get user names
    parser.add_argument('--project-users', required=True, nargs="+", help="User names to add to project.")
    
    arguments = parser.parse_args()

    # connect and get project
    connection = slypi.connect(arguments)
    if arguments.pid:
        project = connection.get_project(arguments.pid)
    elif arguments.project_name:
        project = connection.find_project(arguments.project_name)

    # add members
    members = project['acl']
    for member in arguments.project_users:

        # is member already in project?
        member_type = check_membership(member, members)

        # if so, remove
        if member_type is not None:
            members[member_type].remove({'user': member})

    # update acl to server
    connection.put_project(project['_id'], {'acl': members})