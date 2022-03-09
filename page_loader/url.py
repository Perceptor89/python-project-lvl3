import os
import re
from urllib.parse import urlparse


def make_name_from_url(url, tail=''):
    _path, extension = os.path.splitext(url)
    if not tail:
        tail = extension if extension else '.html'
    parsed_url = urlparse(_path)
    pattern = re.compile(r'[^\w]|_|\.')
    _host = re.sub(pattern, '-', parsed_url.hostname)
    _path = re.sub(pattern, '-', parsed_url.path)
    return "{0}{1}{2}".format(_host, _path, tail)


def get_base_name(url):
    parsed_url = urlparse(url)
    base_name = '{}://{}'.format(parsed_url.scheme, parsed_url.hostname)
    return base_name


def build_full_url(tag_link, base_name):
    parsed_link = urlparse(tag_link)
    if not parsed_link.hostname:
        return os.path.join(base_name, tag_link.strip('/'))
    else:
        return tag_link


def is_common_host(url, link):
    parsed_url = urlparse(url)
    parsed_link = urlparse(link)
    if not parsed_link.hostname:
        return True
    elif parsed_url.hostname == parsed_link.hostname:
        return True
    else:
        return False
