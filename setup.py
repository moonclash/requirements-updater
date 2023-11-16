from setuptools import setup, find_packages

setup(
    name='requirements-updater',
    version='0.1.0',
    author="Emil Mladenov",
    author_email="emladenoff@gmail.com",
    description="a super simple requirements updater for python packages.",
    url="https://github.com/moonclash/requirements-updater",
    project_urls={
        "Bug Tracker": "https://github.com/moonclash/requirements-updater/issues"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["requests"],
    packages=find_packages(),
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            'requpdater = updater.cli:main',
        ],
    },
)