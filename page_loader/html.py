from page_loader.web_loader import get_web_content
from page_loader import url
import requests
import logging
from bs4 import BeautifulSoup


TAG_ATTRIBUTES_DICT = {
    'script': 'src',
    'img': 'src',
    'link': 'href',
}


def get_bs(html_doc):
    return BeautifulSoup(html_doc, 'html.parser')


def get_paths_replace_tags(page_url, res_dir_path, linked_tags):
    resources = []
    for tag in linked_tags:
        attribute_name = TAG_ATTRIBUTES_DICT.get(tag.name)
        tag_link = tag.get(attribute_name)
        if not url.is_common_host(page_url, tag_link):
            logging.info(f'Tag with "{tag_link}" link was ignored.')
            continue
        res_paths = url.build_paths(page_url, tag_link, res_dir_path)
        resources.append((res_paths['url'], res_paths['local_path']))

        tag[attribute_name] = res_paths['html_link']
        logging.info('Link "{0}" replaced to "{1}".'.format(
            tag_link, res_paths['html_link']
        ))

    return resources


def set_linked_tags(tag):
    cond_1 = tag.name in ['img', 'script', 'link']
    cond_2 = tag.has_attr('src') or tag.has_attr('href')
    return cond_1 and cond_2


def get_html_and_resources(page_url, res_dir_path):
    try:
        html_page = get_web_content(page_url)
    except Exception:
        raise requests.RequestException(
            f'Couldn\'t get access to "{page_url}".'
        )
    logging.info(f'Got content from "{page_url}".')

    bs_html_page = get_bs(html_page)
    linked_tags = bs_html_page.find_all(set_linked_tags)
    logging.info('Got tags:\n{0}.'.format('\n'.join(map(str, linked_tags))))
    resources = get_paths_replace_tags(page_url, res_dir_path, linked_tags)

    altered_html_page = bs_html_page.prettify()

    return altered_html_page, resources
