import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION = '0.1.0'
PACKAGE_NAME = 'agrifoodpy_data'
AUTHOR = 'FixOurFood developers'
AUTHOR_EMAIL = 'juanpablo.cordero@york.ac.uk'
URL = 'https://github.com/FixOurFood/agrifoodpy-data'

LICENSE = 'BSD-3-Clause license'
DESCRIPTION = 'Prepackaged data for the AgriFoodPy modelling package'
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = [
      'numpy',
      'pandas',
      'xarray',
      'matplotlib',
      'netcdf4'
]

setup(name=PACKAGE_NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      long_description_content_type=LONG_DESC_TYPE,
      author=AUTHOR,
      license=LICENSE,
      author_email=AUTHOR_EMAIL,
      url=URL,
      install_requires=INSTALL_REQUIRES,
      packages=find_packages(),
      include_package_data=True
      )
