import os

from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), "README.md"), encoding="UTF-8") as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

dev_requirements = [
    "pre-commit",
]

setup(
    name="django-visit-count",
    version="1.1.1",
    description="Count visits using cache for Django models",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Mohammad Javad Naderi",
    url="https://github.com/QueraTeam/django-visit-count",
    download_url="https://pypi.python.org/pypi/django-visit-count",
    license="MIT",
    packages=find_packages(".", include=("django_visit_count", "django_visit_count.*")),
    include_package_data=True,
    install_requires=["Django>=3.2", "django-ipware>=2.0.0"],
    extras_require={"dev": dev_requirements},
    tests_require=dev_requirements,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Framework :: Django :: 4.1",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
