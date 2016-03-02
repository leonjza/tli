from setuptools import setup

setup(
    name='tli',
    description='A Twitter (command) Line Interface',
    author='Leon Jacobs',
    author_email='leonja511@gmail.com',
    url='https://github.com/leonjza/tli',
    download_url='https://github.com/leonjza/tli/tarball/2.1',
    keywords=['twitter', 'line', 'console', 'command', 'client'],
    version='2.2',
    packages=['tli', 'tli.util'],
    include_package_data=True,
    install_requires=[
        'click', 'tweepy', 'pycrypto'
    ],
    entry_points='''
        [console_scripts]
        tli=tli.cli:cli
    ''',
)
