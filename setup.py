from setuptools import find_packages, setup

setup(
    name='SudokuDLXsolver',
    packages=find_packages(include=['SudokuDLXsolver']),
    version='0.1.0',
    description='Sudoku solver using DLX algorithm',
    author='Thomas Kecker',
    license='MIT',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)