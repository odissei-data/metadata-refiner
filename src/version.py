import os


def get_version():
    return os.getenv('APP_VERSION') or 'development'


if __name__ == '__main__':
    print(get_version())
