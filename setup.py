"""Setup configuration."""
import setuptools

setuptools.setup(
    name="beerbolaget",
    version='0.2.1',
    author="Robert Kallin",
    author_email="kallin.roberts@gmail.com",
    description="A python package to get information about the latest beer available at Systembolaget.",
    long_description="A python package to get information about the latest beer available at Systembolaget.",
    install_requires=['requests'],
    long_description_content_type="text/markdown",
    url="https://github.com/Ceerbeerus/pybeerbolaget",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
