from setuptools import setup

setup(
    name='pytest-clearread',
    description='pytest plugin that makes terminal printouts of the reports easier to read based on pytest-easyread',
    long_description=open("README.md").read(),
    version='0.0.3',
    url='https://github.com/adrianer/pytest-clearread',
    download_url='https://github.com/adrianer/pytest-clearread/archive/0.1.tar.gz',
    license='BSD',
    author='Adrian Kalla',
    author_email='adrian.kalla@gmail.com',
    py_modules=['pytest_clearread'],
    entry_points={'pytest11': ['clearread = pytest_clearread']},
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=['pytest>=3.3.2'],
    keywords=['testing', 'readability', 'terminal'],
    classifiers=[
        "Framework :: Pytest",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ]
)
