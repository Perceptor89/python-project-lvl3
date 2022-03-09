import pytest
import tempfile
import os
import requests_mock
import requests
from page_loader import download
from tests.reader import get_content


MAIN_URL = 'https://ru.hexlet.io'
MOCK_DIR = 'tests/fixtures/mock'
FILES_DIR = 'ru-hexlet-io-courses_files'


test_data = {
    'html': {
        'url': os.path.join(MAIN_URL, 'courses'),
        'content': get_content(os.path.join(MOCK_DIR, 'template.html'), 'r'),
        'corr_name': 'ru-hexlet-io-courses.html',
        'corr_html': get_content('tests/fixtures/correct_html.html'),
    },
    'png': {
        'url': os.path.join(MAIN_URL, 'assets/professions/python.png'),
        'content': get_content(os.path.join(MOCK_DIR, 'python.png'), 'rb'),
        'corr_name': 'ru-hexlet-io-assets-professions-python.png',
    },
    'css': {
        'url': os.path.join(MAIN_URL, 'assets/application.css'),
        'content': get_content(os.path.join(MOCK_DIR, 'style.css'), 'r'),
        'corr_name': 'ru-hexlet-io-assets-application.css',
    },
    'js': {
        'url': os.path.join(MAIN_URL, 'packs/js/runtime.js'),
        'content': get_content(os.path.join(MOCK_DIR, 'script.js'), 'r'),
        'corr_name': 'ru-hexlet-io-packs-js-runtime.js',
    },
}

parametrize = [
    (test_data['html']['content'], test_data['html']['corr_name'], 'r'),
    (test_data['png']['content'], test_data['png']['corr_name'], 'rb'),
    (test_data['css']['content'], test_data['css']['corr_name'], 'r'),
    (test_data['js']['content'], test_data['js']['corr_name'], 'r'),
]


@pytest.mark.parametrize('file_content, file_name, flag', parametrize)
def test_download(file_content, file_name, flag):
    with tempfile.TemporaryDirectory() as tempdir:
        with requests_mock.Mocker() as mock:
            mock.get(
                test_data['html']['url'],
                text=test_data['html']['content']
            )
            mock.get(
                test_data['png']['url'],
                content=test_data['png']['content']
            )
            mock.get(test_data['css']['url'], text=test_data['css']['content'])
            mock.get(test_data['js']['url'], text=test_data['js']['content'])

            download(test_data['html']['url'], tempdir)

            html_path = os.path.join(tempdir, test_data['html']['corr_name'])
            received_html = get_content(html_path)
            correct_html = test_data['html']['corr_html']
            assert os.path.isfile(html_path)
            assert received_html == correct_html

            file_path = os.path.join(tempdir, FILES_DIR, file_name)
            received_file = get_content(file_path, flag)
            correct_file = file_content
            assert os.path.isfile(file_path)
            assert received_file == correct_file


def test_not_existing_dir():
    with tempfile.TemporaryDirectory() as tempdir:
        with requests_mock.Mocker() as mock:
            mock.get(MAIN_URL, text="<html></html>")
            with pytest.raises(FileNotFoundError):
                no_dir = os.path.join(MAIN_URL, tempdir, '/not_existing_dir')
                download(MAIN_URL, no_dir)


def test_wrong_status_code():
    with tempfile.TemporaryDirectory() as tempdir:
        with requests_mock.Mocker() as mock:
            mock.get(MAIN_URL, status_code=404)
            with pytest.raises(requests.RequestException):
                download(MAIN_URL, tempdir)
            assert not os.listdir(tempdir)


def test_no_resources():
    with tempfile.TemporaryDirectory() as tempdir:
        with requests_mock.Mocker() as mock:
            mock.get(test_data['html']['url'], text="<html></html>")
            download(test_data['html']['url'], tempdir)
            assert os.path.isfile(
                os.path.join(tempdir, test_data['html']['corr_name'])
            )
            assert not os.path.isdir(os.path.join(tempdir, FILES_DIR))


def test_permission_error():
    with tempfile.TemporaryDirectory() as tempdir:
        with requests_mock.Mocker() as mock:
            mock.get(test_data['html']['url'], text="<html></html>")
            os.chmod(tempdir, 0o444)
            with pytest.raises(PermissionError):
                download(test_data['html']['url'], tempdir)
