#!/usr/bin/env python3
import sys
import logging
from page_loader import download
from page_loader.cli import get_args
from page_loader import logger


def main():
    logger.set_logger()
    args = get_args()
    try:
        logging.warning(f'Downloading page from "{args.url}"...')
        page_local_path = download(args.url, args.output, args.log)
    except Exception as exc:
        logging.warning(exc)
        logging.warning('Page wasn\'t download!')
        sys.exit(42)
    logging.warning(f'Page was successfully downloaded to "{page_local_path}".')
    sys.exit(0)


if __name__ == '__main__':
    main()
