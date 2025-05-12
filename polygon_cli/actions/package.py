from .common import *
import requests
import os


def process_download_last_package(options):
    if not load_session_with_options(options):
        fatal('No session known. Use relogin or init first.')
    
    print("[DEBUG] Options received: format=%s, output=%s" % (options.format, options.output))
    
    # Lấy thông tin đầy đủ về URL từ session
    full_url = global_vars.problem.make_link('', debug=True)
    
    # Trích xuất thông tin cần thiết từ phiên làm việc
    problem_id = global_vars.problem.problem_id
    owner = global_vars.problem.owner or config.login
    problem_code = global_vars.problem.problem_code
    problem_pin = global_vars.problem.problem_pin or options.pin or 'p9SJsMy'
    
    print(f"[DEBUG] Problem ID: {problem_id}")
    print(f"[DEBUG] Problem owner: {owner}")
    print(f"[DEBUG] Problem code: {problem_code}")
    print(f"[DEBUG] Problem PIN: {problem_pin}")
    
    # Tạo URL cho bài toán
    if problem_pin:
        url = f"{config.polygon_url}/p{problem_pin}/{owner}"
        if problem_code:
            url += f"/{problem_code}"
    else:
        url = f"{config.polygon_url}/p{problem_id}/{owner}"
        if problem_code:
            url += f"/{problem_code}"
    
    # Xác định định dạng gói
    format_type = options.format or 'windows'
    print(f"Requesting {format_type} package...")
    
    print(f"[DEBUG] Problem URL: {url}")
    print(f"[DEBUG] Login: {config.login}")
    
    # Thêm định dạng vào URL nếu cần
    if format_type != 'windows':
        url = f"{url}?type={format_type}"
        print(f"[DEBUG] URL with format: {url}")
    
    # Định dạng file đầu ra
    file_path = options.output
    if not file_path:
        name_part = problem_code or f"problem_{problem_id}"
        file_path = f"{name_part}_{format_type}.zip"
    
    # Chuẩn bị dữ liệu POST
    post_data = {
        'login': config.login,
        'password': config.password
    }
    
    # Thêm PIN vào dữ liệu POST nếu được cung cấp thông qua đối số
    if options.pin and not problem_pin:
        post_data['pin'] = options.pin
        print(f"[DEBUG] Using PIN from command line: {options.pin}")
    elif global_vars.problem.pin:
        post_data['pin'] = global_vars.problem.pin
        print(f"[DEBUG] Using PIN from session: {global_vars.problem.pin}")
    
    try:
        # Gửi yêu cầu POST trực tiếp đến URL bài toán
        print(f"[DEBUG] Sending POST request to: {url}")
        print("[DEBUG] Using wget equivalent command:")
        print(f"wget --post-data=login={config.login}\\&password=******** \\")
        print(f"     {url}")
        
        response = requests.post(url, data=post_data, stream=True)
        
        print(f"[DEBUG] Response status code: {response.status_code}")
        print(f"[DEBUG] Response headers: {response.headers}")
        
        if response.status_code != 200:
            print(f"Error downloading package: HTTP {response.status_code}")
            try:
                error_text = response.text[:500]
                print(f"Error details: {error_text}")
            except:
                pass
            return
        
        # Kiểm tra Content-Type để đảm bảo đây là file zip
        content_type = response.headers.get('Content-Type', '')
        if 'application/zip' not in content_type and 'application/octet-stream' not in content_type:
            print(f"Warning: Unexpected content type: {content_type}")
            try:
                error_text = response.text[:500]
                print(f"Response content: {error_text}")
            except:
                pass
            return
        
        # Lưu nội dung phản hồi vào file
        print(f"Downloading package to {file_path}...")
        bytes_written = 0
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    bytes_written += len(chunk)
                    
                    # Log quá trình tải
                    if bytes_written % 1024000 == 0:  # Log mỗi ~1MB
                        print(f"Downloaded {bytes_written/1024/1024:.2f} MB...")
        
        # Kiểm tra kích thước file
        if bytes_written == 0:
            print("Warning: Downloaded file is empty")
            return
            
        print(f"Package successfully downloaded to {file_path} ({bytes_written/1024/1024:.2f} MB)")
    
    except Exception as e:
        print(f"[DEBUG] Exception occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        fatal(f"Error downloading package: {str(e)}")
    
    save_session()


def add_parser(subparsers):
    parser_download_package = subparsers.add_parser(
            'download_package',
            help="Download problem package from polygon"
    )
    
    parser_download_package.add_argument(
        '--format',
        choices=['windows', 'linux', 'unix', 'mac'],
        default='windows',
        help="Package format (default: windows)"
    )
    
    parser_download_package.add_argument(
        '--output', '-o',
        help="Output file path for the package"
    )
    
    parser_download_package.add_argument(
        '--pin',
        help="PIN code for the problem (if required)"
    )
    
    parser_download_package.set_defaults(func=process_download_last_package)