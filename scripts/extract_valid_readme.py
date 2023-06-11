import requests
import json

# Specify the path to the JSON file
json_path = './Consts/detect_test.json'

# Open the JSON file
with open(json_path) as file:
    # Load the JSON data
    json_data = json.load(file)

# Access and use the JSON data
title_md = json_data['title']
character = '# '

modified_title_md = [character + item for item in title_md]

filePath = f'./Logs/repo_100000_coverage.txt'
with open(filePath) as f:
    lines = f.read().splitlines()

readme_filePath = f'./Logs/repo_100000_coverage_seperated.txt'
readme_file = open(readme_filePath, 'a')
readme_error_filePath = f'./Logs/repo_100000_readme_error.txt'
readme_error_file = open(readme_error_filePath, 'a')

def fetch_readme(item):
    line = item.split(',')
    branch = line[5]
    repo = line[1]
    raw_file_url = line[9]
    print(raw_file_url)
    # Make the HTTP GET request
    response = requests.get(raw_file_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Access the content of the response
        readme_content = response.text  # Assuming the file is in JSON format
        
        # print(readme_content)
        test_string = parse_readme(item, readme_content)
        if test_string is False:
            readme_error_file.writelines(repo + ',' + raw_file_url + ', none found. \n')
        if test_string is not False:
            line.pop(10)
            line.append(test_string)
            string = ",".join(line) + "\n"
            readme_file.writelines(string)
            # readme_file.writelines(item + ',' + raw_file_url + ', ' + test_string + '\n')
    else:
        print("Failed to retrieve the README file. Status code:", response.status_code)
        readme_error_file.writelines(repo + ', no readme. \n')

def parse_readme(item, content):
        
        if "coveralls.io" in content:
            return "coveralls.io"

        elif "codecov.io" in content:
            return "codecov.io"
        
        none_found = all(item not in content for item in modified_title_md)

        if none_found:
            return False

        else:
            title_str = ""
            for title_item in title_md:
                if title_item in content:
                    title_str = title_item + "_"
            return title_str



for item in lines:
    result = fetch_readme(item)
    

