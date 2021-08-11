import os
from subprocess import run

import requests

from linq import __version__

HOST = "https://pypi.org/pypi/python-linq"


def get_versions():
    response = requests.get(f"{HOST}/json").json()
    return response["releases"].keys()


def upload():
    run("python setup.py sdist bdist_wheel", shell=True, check=True)
    run(
        f"twine upload -u {os.environ.get('PYPI_USERNAME')} -p {os.environ.get('PYPI_PASSWORD')} dist/*",
        shell=True,
        check=True,
    )


def main():
    if os.environ.get("PYPI_USERNAME") is None:
        raise RuntimeError("PYPI_USERNAME environment variable was not found.")
    if os.environ.get("PYPI_PASSWORD") is None:
        raise RuntimeError("PYPI_PASSWORD environment variable was not found.")

    if __version__ not in get_versions():
        print(f"New version {__version__} detected. Uploading...")
        upload()
    else:
        print("No new version detected.")

if __name__ == "__main__":
    main()
