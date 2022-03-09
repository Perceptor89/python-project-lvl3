def get_content(_path, flag='r'):
    with open(_path, flag) as file:
        return file.read()
