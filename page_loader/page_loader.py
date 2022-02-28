import requests
import os
import re


def make_file_name(url, ext):
    file_name_no_schema = re.sub(r'^(https?:\/\/)', '', url)
    file_name_with_dashes = re.sub(r'[^\w]', '-', file_name_no_schema)
    file_name_with_ext = file_name_with_dashes + ext
    return file_name_with_ext


def download(url, output_directory):
    request = requests.get(url)
    file_name = make_file_name(url, '.html')
    loaded_page_path = os.path.join(
        output_directory,
        file_name,
    )
    with open(loaded_page_path, 'w+') as loaded_page:
        loaded_page.write(request.text)
    print(loaded_page_path)
    return loaded_page_path
