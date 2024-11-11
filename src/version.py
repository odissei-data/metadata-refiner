import subprocess


def get_version():
    result = subprocess.run(
        ["poetry", "version", "--short"],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()


if __name__ == '__main__':
    print(get_version())
