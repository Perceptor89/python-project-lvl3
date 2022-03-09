#!/usr/bin/env python3
import argparse
import os
import sys
import logging
import traceback
from page_loader import download


def main():
    parser = argparse.ArgumentParser(description='Load web-page')
    parser.add_argument(
        '-o',
        '--output',
        help='output folder (current working directory by default)',
        default=os.getcwd()
    )
    parser.add_argument('url', help='url of page to download')
    parser.add_argument(
        '-l',
        '--log',
        help='creates log-file',
        action='store_true',
    )
    args = parser.parse_args()
    try:
        page_local_path = download(args.url, args.output, args.log)
    except Exception:
        logging.warning('Page wasn\'t download!')
        logging.info(traceback.format_exc())
        sys.exit(42)
    logging.warning(
        f'Page was successfully downloaded to "{page_local_path}".'
    )
    sys.exit(0)


if __name__ == '__main__':
    main()
