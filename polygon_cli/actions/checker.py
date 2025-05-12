from .common import *

def process_download_checker(options):
    if not load_session_with_options(options):
        fatal('No session known. Use relogin or init first.')
    
    # First, get problem info to find checker
    try:
        problem_info = global_vars.problem.send_api_request('problem.info', {})
        
        if 'checker' in problem_info:
            checker_name = problem_info['checker']
            print(f"Found checker: {checker_name}")
            
            # Handle standard checkers
            if checker_name.startswith('std::'):
                print(f"This is a standard checker: {checker_name}")
                # Can add option to download standard testlib checkers if needed
                if not options.force:
                    print("Use --force to attempt downloading standard checkers")
                    return
                
        # Get all files
        files = global_vars.problem.get_files_list()
        
        # Find checker file with multiple name patterns
        checker_file = None
        checker_patterns = ['check.cpp', 'checker.cpp', 'chk.cpp']
        
        # First try to find exact match with checker_name if available
        if 'checker' in problem_info and not problem_info['checker'].startswith('std::'):
            for file in files:
                if file.name == problem_info['checker']:
                    checker_file = file
                    break
        
        # If not found, try common patterns
        if checker_file is None:
            for file in files:
                if file.type == 'source':
                    for pattern in checker_patterns:
                        if file.name.endswith(pattern):
                            checker_file = file
                            break
                    if checker_file:
                        break
        
        if checker_file is None:
            print('No custom checker found')
            return
        
        # Download content
        content = checker_file.get_content()
        
        # Save file
        target_path = options.target or checker_file.name
        utils.safe_rewrite_file(target_path, content, "wb")
        print(f'Checker "{checker_file.name}" downloaded to "{target_path}"')
        
    except Exception as e:
        print(f"Error downloading checker: {str(e)}")
    
    save_session()

def add_parser(subparsers):
    parser_download_checker = subparsers.add_parser(
        'download_checker',
        help="Download checker file from polygon"
    )
    parser_download_checker.add_argument('--target', help='Target path to save checker file')
    parser_download_checker.add_argument('--force', action='store_true', 
                                       help='Force download even for standard checkers')
    parser_download_checker.set_defaults(func=process_download_checker)