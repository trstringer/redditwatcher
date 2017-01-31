from setuptools import setup

setup(
    name='redditwatcher',
    version='0.1.0',
    packages=['app'],
    install_requires=[
        'praw',
        'colorama'
    ],
    entry_points={
        'console_scripts': [
            'redditwatcher = app.app:main'
        ]
    }
)
