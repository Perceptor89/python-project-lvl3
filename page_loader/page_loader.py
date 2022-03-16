import os
import logging
from progress.bar import ChargingBar
from page_loader import url
from page_loader.logger import add_filehandler
from page_loader.store import check_dir, make_dir, write_to
from page_loader.web_loader import get_web_content
from page_loader import html


def download_resources(resources):
    bar = ChargingBar('Processing', max=len(resources))
    for resource in resources:
        bar.next()
        resource_url, resource_local_path = resource
        try:
            resource_content = get_web_content(resource_url)
            write_to(resource_content, resource_local_path)
        except Exception:
            logging.warning(
                'Couldn\'t download from "{0}".'.format(resource_url)
            )
            continue
        logging.info('Downloaded from "{0}".'.format(resource_url))
    bar.finish()


def download(page_url, output_dir, is_log=False):
    check_dir(output_dir)
    add_filehandler(output_dir, is_log)

    res_dir_name = url.make_name_from_url(page_url, '_files')
    res_dir_path = os.path.join(output_dir, res_dir_name)
    html_page, resources = html.get_html_and_resources(page_url, res_dir_path)

    if resources:
        make_dir(res_dir_path)
        download_resources(resources)

    page_name = url.make_name_from_url(page_url, '.html')
    page_local_path = os.path.join(output_dir, page_name)
    write_to(html_page, page_local_path)

    return page_local_path
