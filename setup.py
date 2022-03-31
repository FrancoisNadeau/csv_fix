from pathlib import Path

from setuptools import setup, find_packages

readme = Path(__file__).parent.joinpath('README.md').read_text()
# requirements = Path(__file__).parent.joinpath('requirements.txt').read_text().splitlines()

setup(
    name='csvfix',
    packages=find_packages(),
    python_requires='>=3.8',
    url='https://github.com/FrancoisNadeau/csv_fix.git',
    license='MIT',
    long_description=readme,
    author='Francois Nadeau',
    author_email='francois.nadeau.1@umontreal.ca',
    maintainer='Francois Nadeau',
    maintainer_email='francois.nadeau.1@umontreal.ca',
    install_requires=[
        'chardet>=4.0.0',
        'docstring_parser>=0.13',
        'numpy',
        'pandas',
        'unidecode>=1.3.2'
    ],
    description='Methods to retrieve and repair data from .potentially broken or non-standard tabular files.',
    keywords="csv, tsv, table, tabular, data, repair, pandas, sniffer, delimiter, separator"
)
