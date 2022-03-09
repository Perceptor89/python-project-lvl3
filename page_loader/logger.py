import logging
import os


def add_filehandler(output_dir, is_log):
    if is_log:
        log_path = os.path.join(output_dir, 'download.log')

        file_handler = logging.FileHandler(log_path, mode='w')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(
            logging.Formatter('%(levelname)s: %(message)s')
        )
        logging.root.addHandler(file_handler)


def set_logger():
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(logging.Formatter('%(message)s'))
    logging.root.setLevel(logging.INFO)
    logging.root.addHandler(console_handler)
