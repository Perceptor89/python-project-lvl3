import pytest
import tempfile
import os
from page_loader import download


@pytest.fixture
def correct_html():
    with open('tests/fixtures/template.html') as file:
        return file.read()


def test_download(requests_mock, correct_html):
    page_to_load = 'https://ru.hexlet.io/courses'
    loaded_page_correct_name = 'ru-hexlet-io-courses.html'
    requests_mock.get(page_to_load, text=correct_html)

    with tempfile.TemporaryDirectory() as tmpdir:
        loaded_page_path = download(page_to_load, tmpdir)
        loaded_page_name = os.path.basename(loaded_page_path)
        with open(loaded_page_path, 'r') as loaded_page:
            content = loaded_page.read()
        assert loaded_page_name == loaded_page_correct_name
        assert content == correct_html
