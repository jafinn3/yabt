from setuptools import setup, find_packages

setup(
    name='yet-another-backup-tool',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pyaml',
        'argparse',
    ],
    entry_points={
        'console_scripts': [
            'yet-another-backup-tool = yabt.yabt:main',
        ],
    },
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

