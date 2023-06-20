from setuptools import setup, find_packages

setup(
    name='renderg-sdk',
    version='0.1.1',
    url='https://github.com/renderg-repo/renderg-sdk.git',
    author='RenderG',
    author_email='support@renderg.com',
    description='www.renderg.com',
    packages=find_packages(),    
    install_requires=[
        'requests',
        'tenacity'
    ],
)
