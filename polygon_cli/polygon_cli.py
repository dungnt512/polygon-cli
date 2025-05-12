#!/usr/bin/env python3
import argparse
from sys import argv

from .actions import add as add_action
from .actions import commit as commit_action
from .actions import diff as diff_action
from .actions import gettest as get_test_action
from .actions import init as init_action
from .actions import list as list_action
from .actions import update as update_action
from .actions import package as download_package_action
from .actions import samples as samples_action
from .actions import import_package as import_package_action
from .actions import update_groups as update_groups_action
from .actions import update_info as update_info_action
from .actions import tag_solution as tag_solution_action
from .actions import tag_problem as tag_problem_action
from .actions import checker as checker_action
from .actions import list_problemset as list_problemset_action
from .actions import download_files as download_files_action

from . import config
from . import utils


def make_actions(subparsers):
    add_action.add_parser(subparsers)
    commit_action.add_parser(subparsers)
    diff_action.add_parser(subparsers)
    get_test_action.add_parser(subparsers)
    init_action.add_parser(subparsers)
    list_action.add_parser(subparsers)
    update_action.add_parser(subparsers)
    download_package_action.add_parser(subparsers)
    samples_action.add_parser(subparsers)
    import_package_action.add_parser(subparsers)
    update_groups_action.add_parser(subparsers)
    update_info_action.add_parser(subparsers)
    checker_action.add_parser(subparsers)
    tag_solution_action.add_parser(subparsers)
    tag_problem_action.add_parser(subparsers)
    list_problemset_action.add_parser(subparsers)
    download_files_action.add_parser(subparsers)
    return subparsers


def main():
    parser = argparse.ArgumentParser(prog="polygon-cli")
    subparsers = parser.add_subparsers(
            title='Available subcommands',
            metavar='subcommand',
    )
    subparsers.required = True
    subparsers.dest = 'subcommand'
    
    make_actions(subparsers)

    parser.add_argument('--verbose', action='store_true', help='Verbose mode')
    parser.add_argument('--polygon-name',
                      action='store',
                      dest='polygon_name',
                      help='Name of polygon server to use for this problem',
                      default='main')

    # Xử lý help message
    for arg in argv:
        if arg in ["-h", "--help"]:
            if hasattr(utils, 'help_message'):
                utils.help_message()
    
    args = parser.parse_args()
    config.setup_login_by_url(args.polygon_name)
    args.func(args)

if __name__ == "__main__":
    main()
