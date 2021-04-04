from setuptools import setup, find_packages


setup(name='bsm_model',
      version='0.1',
      description='The Black–Scholes–Merton Model calculator in Python.',
      url='https://qrtt.org',
      download_url = 'https://github.com/leopoldsw/bsm_model/archive/v0.0.1.tar.gz',
      author='Leopold W.',
      author_email='lsw@lwco.com',
      packages=find_packages(exclude=("tests", "tests_dev")),
      install_requires=['pandas', 'numpy', 'scipy', 'datetime'],
      )
