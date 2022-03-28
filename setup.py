from pathlib import Path
from setuptools import setup, find_packages

readme = Path(__file__).parent.joinpath('README.md').read_text()
requirements = Path(__file__).parent.joinpath('requirements.txt').read_text().splitlines()

setup(
    name='csv_fix',
    version='0.0.1',
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
    url='https://github.com/FrancoisNadeau/csv_fix.git',
    license='MIT License',
    long_description=readme,
    author='Francois Nadeau',
    author_email='francois.nadeau.1@umontreal.ca',
    description='Methods to retrieve and repair data from potentially broken or non-standard tabular files.',
    keywords="csv, tsv, table, tabular, data, repair, pandas, sniffer, delimiter, separator"
)
