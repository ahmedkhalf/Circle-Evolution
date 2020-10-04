import re

from setuptools import find_packages, setup  # type: ignore
from setuptools.extern import packaging  # type: ignore

# Version info -- read without importing
with open("circle_evolution/__init__.py", "rt", encoding="utf8") as f:
    version_re = re.search(r"__version__ = \"(.*?)\"", f.read())
    if version_re:
        version = version_re.group(1)
    else:
        raise ValueError("Could not determine package version")
    # Normalize version so `setup.py --version` show same version as twine.
    version = str(packaging.version.Version(version))

# Add readme as long description
with open('README.md') as f:
    long_description = f.read()

# Library dependencies
INSTALL_REQUIRES = ["opencv-python==4.2.0.34", "numpy==1.18.4", "Pillow>=6.0", "scikit-image==0.17.2"]

# Testing dependencies
TEST_REQUIRES = [
    "pytest<5.4.0",
    "pytest-cov==2.8.1",
    "pytest-sugar==0.9.2",
    "black",
    "pre-commit",
    "flake8",
    "mypy",
    "bandit",
]

setup(
    name="circle_evolution",
    version=version,
    description="Evolutionary Art Using Circles",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/ahmedkhalf/Circle-Evolution/",
    packages=find_packages(),
    download_url="https://github.com/ahmedkhalf/Circle-Evolution/archive/v0.1.tar.gz",
    author="Ahmed Khalf, Guilherme de Amorim",
    author_email="ahmedkhalf567@gmail.com, ggimenezjr@gmail.com",
    python_requires=">=3.6",
    setup_requires=["wheel"],
    entry_points={"console_scripts": ["circle_evolution=circle_evolution.main:main"]},
    install_requires=INSTALL_REQUIRES,
    extras_require={"test": TEST_REQUIRES},
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development",
    ],
)
