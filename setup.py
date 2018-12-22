from setuptools import find_packages, setup

setup(
    name='reddit_utils',
    version='1.0.4',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'arrow',
        'flask',
        'flask_bootstrap4',
        'praw',
        'PyYAML',
    ],
)
