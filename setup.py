from setuptools import setup

setup(
    name='logfind',
    version='0.0.1',
    author='Roman Levin',
    author_email='romanlevin@gmail.com',
    license='MIT',
    packages=['logfind'],
    extras_require={
        'test': ['pytest']
    },
    entry_points={
        'console_scripts': [
            'logfind=logfind:main'
        ]
    }
)
