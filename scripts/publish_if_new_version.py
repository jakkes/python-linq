import os
from subprocess import run

import requests

from linq import __version__

HOST = "https://pypi.org/pypi/python-linq"


def get_latest_version():
    response = requests.get(f"{HOST}/json").json()
    return response["info"]["version"]


def upload():
    run("python setup.py sdist bdist_wheel", shell=True, check=True)
    run(
        f"twine upload -u {os.environ.get('PYPI_USERNAME')} -p {os.environ.get('PYPI_PASSWORD')} dist/*",
        shell=True,
        check=True,
    )


def main():
    latest_version = get_latest_version()
    if __version__ != latest_version:
        print(f"New version {__version__} detected. Uploading...")
        upload()
    else:
        print("No new version detected.")

if __name__ == "__main__":
    main()
