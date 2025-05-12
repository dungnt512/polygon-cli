from .common import *
from prettytable import PrettyTable


def process_list_problemset(options):
    if not load_session_with_options(options):
        fatal('No session known. Use relogin or init first.')
    
    # Get problems list via API
    problems = global_vars.problem.send_api_request('problems.list', {}, problem_data=False)
    
    # Sort problems by ID in descending order
    problems = sorted(problems, key=lambda x: int(x["id"]), reverse=True)
    
    table = PrettyTable(['ID', 'Name', 'Owner', 'Access Type'])
    
    for problem in problems:
        table.add_row([
            problem["id"],
            problem["name"],
            problem["owner"],
            problem["accessType"]
        ])
    
    print(table)
    save_session()


def add_parser(subparsers):
    parser_list_problemset = subparsers.add_parser(
        'list_problemset',
        help="List all available problemsets sorted by ID (newest first)"
    )
    parser_list_problemset.set_defaults(func=process_list_problemset) 