from setuptools import setup, find_packages

setup(
    name="makestack",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "click >=8.1.3",
        "click-plugins >=1.1.1"
    ],
    entry_points="""
        [console_scripts]
        makestack=cli:main

        [makestack.cli]
        startproject=cli.startproject:startproject
    """,
)