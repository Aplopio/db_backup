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


setup(name='db_backup',
      version='0.1',
      description='Automate the sql backups with rds.',
      long_description=open('Readme.rst').read(),
      url='http://github.com/aplopio/db_backup',
      author='Aplopio',
      author_email='devs@aplopio.com',
      license='MIT',
      packages=['db_backup'],
      include_package_data=True,
      entry_points={
          'console_scripts': [
              'db_backup = db_backup.cli:main',
          ]
      },
      install_requires=requirements,
      tests_require=['pytest'],
      cmdclass={'test': PyTest},
      zip_safe=False)
