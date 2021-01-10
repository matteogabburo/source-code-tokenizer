import setuptools
import json


def load_long_description():
    with open("README.md", "r") as fh:
        long_description = fh.read()
    return long_description


def load_requirements():
    requirements = []
    with open("requirements.txt", "r") as f:
        for line in f.readlines():
            line = line.strip()
            if len(line) > 0:
                requirements.append(line)
    return requirements


def get_version():
    # get semver version [major.minor.patch]
    json_version = {}
    with open(".version.json", "r") as f:
        json_version = json.load(f)
    return ".".join(
        str(w)
        for w in [json_version["major"], json_version["minor"], json_version["patch"]]
    )


setuptools.setup(
    name="source-code-tokenizer",
    version=get_version(),
    author="Matteo Gabburo",
    author_email="matteogabburo@gmail.com",
    description="Collection of tokenizers for multiple languages",
    long_description=load_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/matteogabburo/source-code-tokenizer",
    packages=setuptools.find_packages(),
    install_requires=load_requirements(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
