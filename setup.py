from os import path
from codecs import open
from setuptools import setup, find_packages
here = path.abspath(path.dirname(__file__))

# get dependencies

with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')
install_requires = [x.strip() for x in all_reqs]


setup(
    name='run_task_in_fargate',
    version="0.0.1",
    author='Abdelhak Marouane (am0089@uah.edu)',
    description='Library to run a Cumulus task in a fargate',
    url='https://github.com/ghrcdaac/cumulus_records_cleanup',
    license='Apache 2.0',
    classifiers=[
        'Framework :: Pytest',
        'Topic :: Scientific/Engineering',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: Freeware',
        'Programming Language :: Python :: 3.9',
    ],
    entry_points={
        'console_scripts': [
            'cumulus-cleanup=cumulus_cleanup.cleanup_process:CleanupCumulusRecords.cli',
            'ims-cleanup=cumulus_cleanup.fix_ems_records:EMS_Correct.cli',
            'dlq-cleanup=cumulus_cleanup.clean_dlq:Correct_DLQ.cli'
        ]
    },
    packages=find_packages(exclude=['docs', 'tests*']),
    include_package_data=True,
    install_requires=install_requires,
)
