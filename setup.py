from setuptools import setup

with open('README.rst') as f:
    long_description = f.read()

setup(
    name='yweather',
    version='0.1',
    author='Thomas Roten',
    author_email='thomas@roten.us',
    url='https://github.com/tsroten/yweather',
    description=('a Python module that provides an interface to the Yahoo! '
                 'Weather RSS feed.'),
    long_description=long_description,
    classifiers=[
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: Atmospheric Science',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        ],
    keywords=['weather', 'yahoo', 'interface', 'wrapper', 'api'],
    py_modules=['yweather'],
    test_suite='test',
)
