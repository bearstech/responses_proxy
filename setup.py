# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='responses_proxy',
    version='0.1.4',
    description='allow you to easily mock HTTP responses in your tests',
    long_description=long_description,
    url='https://github.com/bearstech/responses_proxy',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='requests responses',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['requests', 'responses', 'waitress', 'webob'],
    extras_require={
        'test': ['pytest'],
    },
    entry_points={
        'console_scripts': [
            'responses-proxy=responses_proxy.server:main',
        ],
    },
)
