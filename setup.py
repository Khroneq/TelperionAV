from setuptools import setup, find_packages

setup(
    name="telperion_scanner",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'watchdog',
        'scapy',
        'requests',
        'schedule'
    ],
    entry_points={
        'console_scripts': [
            'telperion = main:main'
        ]
    }
)