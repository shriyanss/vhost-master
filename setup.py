# setup.py
from setuptools import setup, find_packages

setup(
    name="vhost-master",
    version="0.0.2",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "vhost_master = vhost_master.vhost_master:main",
        ],
    },
)   