import argparse
import os


def get_args():
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
    return args
