import codecs
import os
import re
from setuptools import setup


def read(*parts):
    path = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(path, encoding='utf-8') as fobj:
        return fobj.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


install_requires = [
    'libvirt-python >= 5.6.0',
    'prometheus-client >= 0.7.1'
]


setup(
    name="libvirt_exporter",
    version=find_version("libvirt_exporter", "__init__.py"),
    description="Prometheus exporter for libvirt",
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    url="https://github.com/patrickjahns/libvirt-prometheus-exporter",
    author="Patrick Jahns",
    author_email="github@patrickjahns.de",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        'Environment :: Console',
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    packages=["libvirt_exporter"],
    include_package_data=True,
    install_requires=install_requires,
    python_requires='>=3.7',
    entry_points={"console_scripts": ["libvirt_exporter=libvirt_exporter.cli:main"]},
)