from setuptools import setup, find_packages


setup(name='bsm_model',
      version='0.2',
      description='The Black–Scholes–Merton Model calculator in Python.',
      long_description='The Black–Scholes–Merton Model calculator in Python.',
      long_description_content_type='text/markdown',
      url='https://github.com/leopoldsw/bsm_model/',
      download_url = 'https://github.com/leopoldsw/bsm_model/archive/v0.2.tar.gz',
      author='Leopold W.',
      author_email='lsw@lwco.com',
      packages=find_packages(exclude=("tests", "tests_dev")),
      install_requires=['pandas', 'numpy', 'scipy'],
      )
