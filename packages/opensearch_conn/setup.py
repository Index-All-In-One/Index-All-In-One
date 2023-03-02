from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='opensearch_conn',
    version='0.0.1',
    author='Index-All-In-One',
    author_email='sample@gmail.com',
    description='utils to connect OpenSearch with python',
    keywords='opensearch',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Index-All-In-One/Opensearch-Conn',
    packages=find_packages(),
    include_package_data=True,
    license='Apache License 2.0',
    
    classifiers=[
        # see https://pypi.org/classifiers/
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: Apache License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'opensearch-py'
    ]
)