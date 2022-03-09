import pytest
from page_loader.url import make_name_from_url


test_data = {
    ('https://ru.hexlet.io/courses', '_files', 'ru-hexlet-io-courses_files'),
    ('https://ru.hexlet.io/courses', '.html', 'ru-hexlet-io-courses.html'),
    ('https://ru.hexlet.io/courses', '', 'ru-hexlet-io-courses.html'),
    ('https://ru.hexlet.io/courses.rss', '', 'ru-hexlet-io-courses.rss'),
    ('https://ru.hexlet.io/_courses', '_files', 'ru-hexlet-io--courses_files'),
}


@pytest.mark.parametrize('url, tail, name', test_data)
def test_make_name_from_url(url, tail, name):
    assert make_name_from_url(url, tail) == name
