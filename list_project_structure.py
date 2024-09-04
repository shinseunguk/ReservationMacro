import os

def list_files(startpath):
    exclude_dirs = {'.git', '.idea', '.venv'}
    exclude_files = {'.gitignore', '.gitmodules'}

    for root, dirs, files in os.walk(startpath):
        # 제외할 디렉토리 필터링
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print(f'{indent}{os.path.basename(root)}/')
        
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            if f not in exclude_files:
                print(f'{subindent}{f}')

# 실행 디렉토리 지정
project_dir = '.'  # 현재 디렉토리
list_files(project_dir)
