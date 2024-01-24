# setup.py
from setuptools import setup, find_packages

setup(
    name="vhost-master",
    version="0.0.4",
    packages=find_packages(),
    install_requires=[
        "tldextract",
        "colorama"
    ],
    entry_points={
        "console_scripts": [
            "vhost_master = vhost_master.vhost_master:main",
        ],
    },
)
