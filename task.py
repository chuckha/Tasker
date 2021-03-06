#!/usr/local/bin/python
# Todo: Learn how to use #! properly

import os.path
import argparse

from dict_to_plist import dict_to_plist, new_name
from launchd import print_plist_files, LAUNCH_AGENT_DIR


#task create <label> <cmd>
#task edit <label>
#task delete <label>
#task show

# Todo: wow, launchd can run scripts from watched dirs

class NeedLaunchdException(Exception):
    pass

def printer(args):
    print_plist_files()

def create_file(args):
    # Todo: Actually check the OS and look for launchd. Does linux have launchd?
    basedir = LAUNCH_AGENT_DIR
    if not os.path.exists(basedir):
        raise NeedLaunchdException("You should have ~/Library/LaunchAgents, but"
        " you do not. I expect you to be running OS X 10.7 or later.")
    filename = "%s/Tasker.local.%s.plist" % (basedir, "".join(args.Label.split()))
    with open(filename, "w") as f:
        f.write(make_file_contents(args))
        # Todo: tell people how to load it
        print "Wrote: %s" % filename

def make_file_contents(args):
    d = vars(args)
    d.pop("func", None)
    return dict_to_plist(d)

def remove(args):
    pass

parser = argparse.ArgumentParser(prog="Tasker")
subparsers = parser.add_subparsers()

# Create
create = subparsers.add_parser("create", help="create a launchd task")
create.add_argument("ProgramArguments", nargs='+', help="The command you want to run on an interval")
create.add_argument("-l", "--label", dest="Label", default=new_name(), help="the label of the task to create")
create.add_argument("-s", "--seconds", metavar="seconds", default="18000", dest="StartInterval", type=int, help="start this task every <N> seconds")
create.set_defaults(func=create_file)

# Delete
delete = subparsers.add_parser("delete", help="delete a launchd task")
delete.add_argument("label", help="The label of the task to delete")
delete.set_defaults(func=remove)

# Edit
edit = subparsers.add_parser("edit", help="edit a launchd task")
edit.add_argument("label", help="The label of the task to edit")

# List
show = subparsers.add_parser("show", help="see all tasks for current user")
show.set_defaults(func=printer)

args = parser.parse_args()
args.func(args)

