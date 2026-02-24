# Copyright (c) 2013, 2018 National Technology and Engineering Solutions of Sandia, LLC . Under the terms of Contract
# DE-NA0003525 with National Technology and Engineering Solutions of Sandia, LLC, the U.S. Government
# retains certain rights in this software.

# This script lists the projects available for a given user

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

# call server and list projects
def main (arguments, connection):

    # get projects
    projects = connection.get_projects()
    
    # output projects
    for project in projects["projects"]:
        membership = check_membership(arguments.user, project['acl'])
        print("Found user %s (%s) on project %s." %(arguments.user, membership[:-1], project["name"]))

# command line entry point
if __name__ == "__main__":

    # get arguments for connecting to Slycat server
    parser = slypi.ArgumentParser(
        description="List projects accessible for a given user.")
    arguments = parser.parse_args()

    # connect and get projects
    connection = slypi.connect(arguments)

    # list projects
    main(arguments, connection)