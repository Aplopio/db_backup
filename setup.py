import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand

requirements = [line.strip() for line in open('requirements.txt').readlines()]


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(name='rds_sql_backup',
      version='0.1',
      description='Automate the sql backups with rds.',
      url='http://github.com/aplopio/rds_sql_backup',
      author='Aplopio',
      author_email='devs@aplopio.com',
      license='MIT',
      packages=['rds_sql_backup'],
      entry_points={
          'console_scripts': [
              'rds_sql_backup = rds_sql_backup.main:main',
          ]
      },
      install_requires=requirements,
      tests_require=['pytest'],
      cmdclass={'test': PyTest},
      zip_safe=False)
