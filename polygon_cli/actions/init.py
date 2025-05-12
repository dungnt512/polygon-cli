from prettytable import PrettyTable
import re

from .common import *
from .. import colors
from .. import config
from .. import global_vars


def process_init(polygon_name, problem_id, pin, **session_options):
    config.setup_login_by_url(polygon_name)
    
    # Handle problem name lookup if not a numeric ID
    problem_code = None  # Store original problem code for URL purposes
    owner = None
    
    if not problem_id.isdigit():
        problem_code = problem_id  # Lưu lại tên bài toán (code) trước khi tìm ID
        print(f"Looking up problem with name: {problem_code}")
        
        session = ProblemSession(polygon_name, None, None, **session_options)
        problems = session.send_api_request('problems.list', {}, problem_data=False)
        list = []
        for i in problems:
            if i["name"] == problem_id:
                list.append(i)
        if len(list) == 0:
            print('No problem %s found' % problem_id)
            exit(0)
        if len(list) == 1:
            problem_id = list[0]["id"]
            owner = list[0]["owner"]
            print('Detected problem id is %s' % problem_id)
            print('Problem owner: %s' % owner)
            print('Problem code: %s' % problem_code)
        if len(list) > 1:
            print('Problem %s is ambigious, choose by id' % problem_id)
            table = PrettyTable(['Id', 'Name', 'Owner', 'Access'])
            for i in list:
                table.add_row([i["id"], i["name"], i["owner"], i["accessType"]])
            print(table)
            exit(0)
    
    # Khởi tạo session mới
    print("Initializing problem session...")
    global_vars.problem = ProblemSession(polygon_name, problem_id, pin, **session_options)
    
    if owner:
        global_vars.problem.owner = owner
    
    # Lưu thông tin mã bài
    if problem_code:
        print(f"Saving problem code: {problem_code}")
        global_vars.problem.problem_code = problem_code
    
    # Lấy thêm thông tin từ problem links
    # print("Getting problem details...")
    # links = global_vars.problem.get_problem_links()
    # if links:
    #     if links['owner'] and not global_vars.problem.owner:
    #         global_vars.problem.owner = links['owner']
    #         print(f"Problem owner: {links['owner']}")
        
    #     if links['problem_name']:
    #         global_vars.problem.problem_name = links['problem_name']
    #         print(f"Problem name: {links['problem_name']}")
    
    #     # Get PIN code from URL if available (p85dlBF part)
    #     if links['continue']:
    #         match = re.search(r'/p([^/]+)/', links['continue'])
    #         if match:
    #             problem_pin = match.group(1)
    #             print(f"Detected problem PIN: {problem_pin}")
    #             global_vars.problem.problem_pin = problem_pin
    
    # Verify and print data before saving
    print(f"Session data to be saved:")
    print(f"- Problem ID: {global_vars.problem.problem_id}")
    print(f"- Problem Code: {global_vars.problem.problem_code}")
    print(f"- Problem PIN: {global_vars.problem.problem_pin}")
    print(f"- Owner: {global_vars.problem.owner}")
    
    # Lưu session
    save_session()


def process_init_contest(polygon_name, contest_id, pin, **session_options):
    config.setup_login_by_url(polygon_name)
    contest = ProblemSession(polygon_name, None, pin, **session_options)
    problems = contest.get_contest_problems(contest_id)
    print(problems)
    result = PrettyTable(['Problem name', 'Problem id', 'Status'])

    for problem in problems.keys():
        if os.path.exists(problem):
            result.add_row([problem, problems[problem], colors.error('Directory exists')])
        else:
            try:
                os.mkdir(problem)
                old_path = os.getcwd()
                os.chdir(problem)
                process_init(polygon_name, str(problems[problem]), pin, **session_options)
                os.chdir(old_path)
                result.add_row([problem, problems[problem], colors.success('Done')])
            except Exception as e:
                print(e)
                result.add_row([problem, problems[problem], colors.error('Exception during init')])

    print(result)


def add_parser(subparsers):
    parser_init = subparsers.add_parser(
            'init',
            help="Initialize tool"
    )
    parser_init.add_argument('problem_id', help='Problem id or name to work with')
    parser_init.add_argument('--pin', dest='pin', default=None, help='Pin code for problem')
    parser_init.set_defaults(func=lambda options: process_init(options.polygon_name, options.problem_id, options.pin, **get_session_options(options)))
    parser_init.add_argument('--polygon-name',
                        action='store',
                        dest='polygon_name',
                        help='Name of polygon server to use for this problem',
                        default='main'
                        )

    parser_init_contest = subparsers.add_parser(
            'init_contest',
            help="Initialize tool for several problems in one contest"
    )
    parser_init_contest.add_argument('contest_id', help='Contest id to init')
    parser_init_contest.add_argument('--pin', dest='pin', default=None, help='Pin code for contest')
    parser_init_contest.add_argument('--polygon-name',
                        action='store',
                        dest='polygon_name',
                        help='Name of polygon server to use for this problem',
                        default='main'
                        )
    parser_init_contest.set_defaults(func=lambda options: process_init_contest(options.polygon_name, options.contest_id, options.pin, **get_session_options(options)))
