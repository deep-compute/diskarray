from setuptools import setup, find_packages

version = '0.1'
setup(
    name="diskarray",
    version=version,
    description="A resizable numpy array on disk (mmap based)",
    keywords='diskarray',
    author='Deep Compute, LLC',
    author_email="contact@deepcompute.com",
    url="https://github.com/deep-compute/diskarray",
    download_url="https://github.com/deep-compute/diskarray/tarball/%s" % version,
    license='MIT License',
    install_requires=[
        'numpy==1.13.1',
        'deeputil==0.2'
    ],
    package_dir={'diskarray': 'diskarray'},
    packages=find_packages('.'),
    include_package_data=True,
    #test_suite='test.suite',
    entry_points={
        "console_scripts": [
            "diskarray = diskarray",
        ]
    }

)
