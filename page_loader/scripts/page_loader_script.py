#!/usr/bin/env python3

import argparse
from page_loader import download


def main():
    parser = argparse.ArgumentParser(description='Page download')
    parser.add_argument('--output', help='output folder', default='.')
    parser.add_argument('url', help='page to download')
    args = parser.parse_args()
    download(args.url, args.output)


if __name__ == '__main__':
    main()
