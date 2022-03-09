import os
import logging
import requests


def check_dir(output_dir):
    if not os.path.exists(output_dir):
        logging.warning(
            f'Directory "{output_dir}" doesn\'t exist. Choose another one.'
        )
        raise FileNotFoundError


def make_dir(dir_path):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
        logging.info(f'Created directory in "{dir_path}".')
    else:
        logging.info(f'Directory "{dir_path}" already exists.')


def write_to(content, local_path):
    try:
        flag = 'wb' if isinstance(content, bytes) else 'w'
        with open(local_path, flag) as local_file:
            local_file.write(content)
        logging.info('File was written to "{0}"'.format(local_path))
    except Exception as _error:
        logging.warning('Couldn\'t write to "{0}"'.format(local_path))
        raise _error


def get_web_content(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.content