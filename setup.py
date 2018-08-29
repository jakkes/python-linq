import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python-linq",
    version="1.2.1",
    author="Jakob Stigenberg",
    description="Brings LINQ to Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jakkes/python-linq",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)

### Publish
### python3 setup.py sdist bdist_wheel
### twine upload dist/*