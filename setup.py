from setuptools import setup, find_packages

setup(
    name='yet-another-backup-tool',
    version='0.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'pyaml',
        'argparse',
    ],
    entry_points={
        'console_scripts': [
            'yabt = yabt.yabt:main',
        ],
    },
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

