from setuptools import setup, find_packages

setup(
    name="djinx",
    version="0.1",
    author="Philipp Rollinger",
    author_email="philipp.rollinger@protonmail.com",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.10",
    install_requires=[
        "Django>=4.2,<4.3",  # Django 4.2 is the latest LTS
    ],
    classifiers=[
        "Framework :: Django",
        "Programming Language :: Python :: 3",
    ],
)
