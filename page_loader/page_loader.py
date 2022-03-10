import os
import logging
from bs4 import BeautifulSoup
import requests
from progress.bar import ChargingBar
from page_loader import url
from page_loader.logger import set_logger, add_filehandler
from page_loader.in_out import check_dir, get_web_content, make_dir, write_to


TAG_ATTRS_DICT = {
    'script': 'src',
    'img': 'src',
    'link': 'href',
}


def get_bs(html_doc):
    return BeautifulSoup(html_doc, 'html.parser')


def set_tags(tag):
    cond_1 = tag.name in ['img', 'script', 'link']
    cond_2 = tag.has_attr('src') or tag.has_attr('href')
    return cond_1 and cond_2


def build_paths(page_url, tag_link, files_dir_path):
    base_name = url.get_base_name(page_url)
    resource_url = url.build_full_url(tag_link, base_name)
    resource_name = url.make_name_from_url(resource_url)
    resource_local_path = os.path.join(files_dir_path, resource_name)
    files_dir_name = os.path.split(files_dir_path)[1]
    resource_html_link = os.path.join(files_dir_name, resource_name)
    return {
        'url': resource_url,
        'local_path': resource_local_path,
        'html_link': resource_html_link,
    }


def download_resources(tag_list, page_url, files_dir_path):
    bar = ChargingBar('Processing', max=len(tag_list))
    for tag in tag_list:
        bar.next()
        attr_name = TAG_ATTRS_DICT.get(tag.name)
        tag_link = tag.get(attr_name)
        if not url.is_common_host(page_url, tag_link):
            logging.info(f'Tag with "{tag_link}" link was ignored.')
            continue
        res_paths = build_paths(page_url, tag_link, files_dir_path)
        try:
            resource_content = get_web_content(res_paths['url'])
        except Exception:
            logging.warning(
                'Couldn\'t download from "{0}".'.format(res_paths['url'])
            )
            continue
        write_to(resource_content, res_paths['local_path'])
        tag[attr_name] = res_paths['html_link']
        logging.info('Link "{0}" replaced to "{1}".'.format(
            tag_link, res_paths['html_link']
        ))
    bar.finish()


def download(page_url, output_dir, is_log=False):
    set_logger()
    check_dir(output_dir)
    add_filehandler(output_dir, is_log)

    try:
        raw_html = get_web_content(page_url)
    except Exception:
        raise requests.RequestException(
            f'Couldn\'t get access to "{page_url}".'
        )
    logging.info(f'Got content from "{page_url}".')

    html_soup = get_bs(raw_html)
    linked_tags = html_soup.find_all(set_tags)
    logging.info('Got tags:\n{0}.'.format('\n'.join(map(str, linked_tags))))
    if linked_tags:
        files_dir_name = url.make_name_from_url(page_url, '_files')
        files_dir_path = os.path.join(output_dir, files_dir_name)
        make_dir(files_dir_path)
        download_resources(linked_tags, page_url, files_dir_path)

    page_name = url.make_name_from_url(page_url, '.html')
    page_local_path = os.path.join(output_dir, page_name)
    write_to(html_soup.prettify(), page_local_path)

    return page_local_path
