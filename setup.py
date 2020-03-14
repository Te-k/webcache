from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='webcache',
    version='0.1.1',
    description='Tool to search or save pages in cache',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/Te-k/webcache',
    author='Tek',
    author_email='tek@randhome.io',
    keywords='osint',
    include_package_data=True,
    install_requires=[
        'requests',
        ],
    python_requires='>=3.5',
    license='GPLv3',
    packages=['webcache'],
    #package_dir={'harpoon.lib': 'harpoon/lib'},
    #package_data={'harpoon': ['harpoon/data/*.conf']},
    entry_points= {
        'console_scripts': [ 'cache=webcache.main:main' ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
