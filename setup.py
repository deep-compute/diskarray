from setuptools import setup, find_packages

version = "0.2.0"
setup(
    name="diskarray",
    python_requires=">3.8.0",
    version=version,
    description="A resizable and readable numpy array on disk",
    keywords="diskarray",
    author="Deep Compute, LLC",
    author_email="contact@deepcompute.com",
    url="https://github.com/deep-compute/diskarray",
    download_url="https://github.com/deep-compute/diskarray/tarball/%s" % version,
    license="MIT License",
    install_requires=["basescript==0.2.9", "numpy==1.22.3"],
    package_dir={"diskarray": "diskarray"},
    packages=find_packages("."),
    include_package_data=True,
    test_suite="test.suitefn",
    entry_points={"console_scripts": ["diskarray = diskarray:main"]},
)
