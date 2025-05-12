import os
import zipfile
import shutil
import datetime
from .common import *

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def process_download_files(options):
    """
    Tải tất cả các file từ Polygon và lưu theo cấu trúc giống package
    """
    if not load_session_with_options(options):
        fatal('No session known. Use relogin or init first.')
    
    problem_id = global_vars.problem.problem_id
    problem_code = global_vars.problem.problem_code
    owner = global_vars.problem.owner or config.login
    
    # Tạo thư mục đầu ra
    output_dir = options.output or (problem_code or f"problem_{problem_id}")
    if os.path.exists(output_dir) and not options.force:
        if not options.quiet:
            print(f"Directory {output_dir} already exists. Use --force to overwrite.")
        return
    
    if os.path.exists(output_dir):
        if not options.quiet:
            print(f"Removing existing directory {output_dir}...")
        shutil.rmtree(output_dir)
    
    # Tạo cấu trúc thư mục
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(os.path.join(output_dir, "src"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "tests"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "solutions"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "statements"), exist_ok=True)
    
    if not options.quiet:
        print(f"Downloading all files for problem {problem_id} ({problem_code if problem_code else ''})...")
        print(f"Output directory: {output_dir}")
    
    # Tải tất cả các loại files
    total_files = 0
    
    # 1. Download source files (checker, validator, etc.)
    files = global_vars.problem.get_files_list()
    if not options.quiet:
        print(f"Found {len(files)} source files")
    
    for file in files:
        if file.type == 'script':
            content = global_vars.problem.get_script_content()
            if content:
                target_path = os.path.join(output_dir, "src", "script.txt")
                utils.safe_rewrite_file(target_path, content, "wb")
                total_files += 1
                if not options.quiet:
                    print(f"Downloaded: src/script.txt")
            continue
        
        content = file.get_content()
        if content is None:
            continue
        
        # Xác định thư mục đích
        if file.type == 'source':
            target_dir = os.path.join(output_dir, "src")
        elif file.type in ['resource', 'attachment']:
            target_dir = os.path.join(output_dir, "src")
        else:
            target_dir = os.path.join(output_dir, "src")
        
        # Lưu file
        target_path = os.path.join(target_dir, file.name)
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        utils.safe_rewrite_file(target_path, content, "wb")
        total_files += 1
        
        if not options.quiet:
            relative_path = os.path.relpath(target_path, output_dir)
            print(f"Downloaded: {relative_path}")
    
    # 2. Download solutions
    solutions = global_vars.problem.get_solutions_list()
    if not options.quiet:
        print(f"Found {len(solutions)} solutions")
    
    for solution in solutions:
        content = solution.get_content()
        if content is None:
            continue
        
        target_path = os.path.join(output_dir, "solutions", solution.name)
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        utils.safe_rewrite_file(target_path, content, "wb")
        total_files += 1
        
        if not options.quiet:
            relative_path = os.path.relpath(target_path, output_dir)
            print(f"Downloaded: {relative_path}")
    
    # 3. Download statements
    statements = global_vars.problem.get_statements_list()
    if not options.quiet:
        print(f"Found {len(statements)} statement files")
    
    for statement in statements:
        content = statement.content
        if content is None:
            continue
        
        target_path = os.path.join(output_dir, "statements", statement.name)
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        utils.safe_rewrite_file(target_path, content, "wb")
        total_files += 1
        
        if not options.quiet:
            relative_path = os.path.relpath(target_path, output_dir)
            print(f"Downloaded: {relative_path}")
    
    # 4. Download statement resources
    stmt_resources = global_vars.problem.get_statement_resources_list()
    if not options.quiet:
        print(f"Found {len(stmt_resources)} statement resources")
    
    for resource in stmt_resources:
        content = resource.get_content()
        if content is None:
            continue
        
        target_path = os.path.join(output_dir, "statements", "resources", resource.name)
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        utils.safe_rewrite_file(target_path, content, "wb")
        total_files += 1
        
        if not options.quiet:
            relative_path = os.path.relpath(target_path, output_dir)
            print(f"Downloaded: {relative_path}")
    
    # 5. Download tests
    try:
        tests = global_vars.problem.get_tests()
        if not options.quiet:
            print(f"Found {len(tests)} tests")
        
        for test in tests:
            test_index = test["index"]
            
            # Download test input
            input_content = global_vars.problem.send_api_request(
                'problem.testInput',
                {'testset': 'tests', 'testIndex': test_index},
                is_json=False
            )
            
            if input_content:
                target_path = os.path.join(output_dir, "tests", f"{int(test_index):03d}")
                utils.safe_rewrite_file(target_path, utils.convert_newlines(input_content), "wb")
                total_files += 1
                
                if not options.quiet:
                    relative_path = os.path.relpath(target_path, output_dir)
                    print(f"Downloaded: {relative_path}")
            
            # Download test answer
            answer_content = global_vars.problem.send_api_request(
                'problem.testAnswer',
                {'testset': 'tests', 'testIndex': test_index},
                is_json=False
            )
            
            if answer_content:
                target_path = os.path.join(output_dir, "tests", f"{int(test_index):03d}.a")
                utils.safe_rewrite_file(target_path, utils.convert_newlines(answer_content), "wb")
                total_files += 1
                
                if not options.quiet:
                    relative_path = os.path.relpath(target_path, output_dir)
                    print(f"Downloaded: {relative_path}")
    except Exception as e:
        if not options.quiet:
            print(f"Error downloading tests: {str(e)}")
    
    # 6. Create problem info file
    try:
        info_content = f"""Problem Information:
ID: {problem_id}
Name: {global_vars.problem.problem_name or problem_code or ""}
Owner: {owner}
Downloaded on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Files count: {total_files}
"""
        
        target_path = os.path.join(output_dir, "problem_info.txt")
        utils.safe_rewrite_file(target_path, info_content.encode('utf-8'), "wb")
        
        if not options.quiet:
            print(f"Created problem info file: problem_info.txt")
    except Exception as e:
        if not options.quiet:
            print(f"Error creating problem info: {str(e)}")
    
    # 7. Create ZIP archive if requested
    if options.create_zip:
        zip_path = f"{output_dir}.zip"
        if not options.quiet:
            print(f"Creating ZIP archive: {zip_path}")
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(output_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, os.path.dirname(output_dir))
                    zipf.write(file_path, arcname)
    
    if not options.quiet:
        print(f"Successfully downloaded {total_files} files to {output_dir}")
    
    save_session()

def add_parser(subparsers):
    parser_download_files = subparsers.add_parser(
        'download_files',
        help="Download all files from polygon with a package-like structure"
    )
    
    parser_download_files.add_argument(
        '--output', '-o',
        help="Output directory path (default: problem name or problem_ID)"
    )
    
    parser_download_files.add_argument(
        '--create-zip',
        action='store_true',
        help="Create a ZIP archive of all downloaded files"
    )
    
    parser_download_files.add_argument(
        '--force', '-f',
        action='store_true',
        help="Overwrite output directory if it already exists"
    )
    
    parser_download_files.add_argument(
        '--quiet', '-q',
        action='store_true',
        help="Suppress output messages"
    )
    
    parser_download_files.set_defaults(func=process_download_files)
