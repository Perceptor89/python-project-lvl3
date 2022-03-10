#!/usr/bin/env python3
import argparse
import os
import sys
import logging
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
        print(f'Downloading page from "{args.url}"...')
        page_local_path = download(args.url, args.output, args.log)
    except Exception as exc:
        logging.warning(exc)
        print('Page wasn\'t download!')
        sys.exit(42)
    print(f'Page was successfully downloaded to "{page_local_path}".')
    sys.exit(0)


if __name__ == '__main__':
    main()
