from setuptools import find_packages, setup

setup(
    name='HueScoreAlert',
    version='0.5.1',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'celery',
        'flask',
        'waitress'
    ]
)
# After dependency change
# pip install -e .
