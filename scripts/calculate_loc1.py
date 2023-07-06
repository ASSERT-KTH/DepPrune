import subprocess
import json
import sys

project = sys.argv[1]

def get_javascript_line_count(directory_path):
    cmd = ['cloc', '--json', '--include-lang=JavaScript', directory_path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        output = result.stdout.strip()
        data = json.loads(output)
        
        if 'JavaScript' in data:
            line_count = data['JavaScript']['code']
            return line_count
    else:
        print(f"Error: {result.stderr}")
    
    return 0  # Default value if line count cannot be obtained

# Usage example
# directory_path = f'./Original/{project}'
directory_path = f'./Original/{project}/node_modules'
line_count = get_javascript_line_count(directory_path)

targetfile = open("Logs/lines_of_code_temp.txt", "a")
# text = f'{project},{line_count}\n'
text = f'{line_count}\n'
targetfile.writelines(text)
