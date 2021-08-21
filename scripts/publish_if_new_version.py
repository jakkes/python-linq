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


def set_version(version):
    with open("linq/__init__.py", "r") as f:
        data = f.read()
    data.replace("<%<%VERSION%>%>", version)
    with open("linq/__init__.py", "w") as f:
        f.write(data)


def main():
    with open("VERSION", "r") as f:
        version = f.read()

    if os.environ.get("PYPI_USERNAME") is None:
        raise RuntimeError("PYPI_USERNAME environment variable was not found.")
    if os.environ.get("PYPI_PASSWORD") is None:
        raise RuntimeError("PYPI_PASSWORD environment variable was not found.")

    if version not in get_versions():
        print(f"New version {version} detected. Uploading...")
        set_version(version)
        upload()
    else:
        print("No new version detected.")

if __name__ == "__main__":
    main()
