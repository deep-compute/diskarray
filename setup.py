from setuptools import setup, find_packages

version = '0.1.8'
setup(
    name="diskarray",
    version=version,
    description="A resizable and readable numpy array on disk",
    keywords='diskarray',
    author='Deep Compute, LLC',
    author_email="contact@deepcompute.com",
    url="https://github.com/deep-compute/diskarray",
    download_url="https://github.com/deep-compute/diskarray/tarball/%s" % version,
    license='MIT License',
    install_requires=[
        'numpy==1.14.3',
        'basescript==0.2.6'
    ],
    package_dir={'diskarray': 'diskarray'},
    packages=find_packages('.'),
    include_package_data=True,
    test_suite='test.suitefn',
    entry_points={
        "console_scripts": [
            "diskarray = diskarray:main",
        ]
    }
)
