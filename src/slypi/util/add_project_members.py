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

# modify a single project
def modify_project_members (arguments, project):

    # add members
    members = project['acl']
    for member in arguments.project_users:

        # is member already in project?
        member_type = check_membership(member, members)

        # if so, remove
        if member_type is not None:
            members[member_type].remove({'user': member})

        # add new member of correct type
        members[arguments.user_type + 's'].append({'user': member})

    return members

# command line entry point
if __name__ == "__main__":

    # get arguments for connecting to Slycat server
    parser = slypi.ArgumentParser(
        description="Add users to a given project.  If a user is already on the project, " + 
        "that user's role will be modified (e.g. reader to writer).")
    
    # get either pid or name
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--project-name', help='Project name to retrieve.')
    group.add_argument('--pid', help='Project ID to retrieve.')
    group.add_argument('--all-projects', action="store_true", 
                       help="Apply to all projects where you are an administrator.")

    # get user names
    parser.add_argument('--project-users', required=True, nargs="+", help="User names to add to project.")

    # get user type
    parser.add_argument('--user-type', choices=["administrator", "writer", "reader"], default="reader",
                        help="User type to add to project. Default is %(default)s.")
    
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
            if {'user': arguments.user} in project['acl']['administrators']:
                members = modify_project_members(arguments, project)
                connection.put_project(project['_id'], {'acl': members})
        
    # only modifying a single project
    else:
        
        # connect by pid or project name for 
        if arguments.pid:
            project = connection.get_project(arguments.pid)
        elif arguments.project_name:
            project = connection.find_project(arguments.project_name)

        # add members and push to project
        members = modify_project_members(arguments, project)
        connection.put_project(project['_id'], {'acl': members})
