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

# remove members from project
def remove_project_members (arguments, connection, project):

    # remove members
    members = project['acl']
    for member in arguments.project_users:

        # is member already in project?
        member_type = check_membership(member, members)

        # if so, remove
        if member_type is not None:
            members[member_type].remove({'user': member})
    
    # remove members
    connection.put_project(project['_id'], {'acl': members})

    # update with users removed
    for user in arguments.project_users:
        print("Removed " + user + " from " + project['name'] + ".")

# command line entry point
if __name__ == "__main__":

    # get arguments for connecting to Slycat server
    parser = slypi.ArgumentParser(
        description="Remove users from a given project.")
    
    # get either pid or name
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--project-name', nargs="+", help='Project name to retrieve.')
    group.add_argument('--pid', nargs="+", help='Project ID to retrieve.')
    group.add_argument('--all-projects', action="store_true", 
                       help="Apply to all projects where you are an administrator.")
    
    # get user names
    parser.add_argument('--project-users', required=True, nargs="+", help="User names to add to project.")
    
    arguments = parser.parse_args()

    # make sure user is not on list
    if arguments.user in arguments.project_users:
        raise ValueError('Cannot modify your own membership.')
    
    # connect and get project
    connection = slypi.connect(arguments)

    # are we modifying all projects?
    if arguments.all_projects:

        # get projects
        projects = connection.get_projects()

        # add members to each project
        for project in projects["projects"]:
            remove_project_members (arguments, connection, project)
        
    # only modifying projects specified
    else:
        
        # add users by project id
        if arguments.pid:
            for project_id in arguments.pid:
                project = connection.get_project(project_id)
                remove_project_members(arguments, connection, project)

        # add users by project name
        elif arguments.project_name:
            for project_name in arguments.project_name:
                project = connection.find_project(project_name)
                remove_project_members(arguments, connection, project)