import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="safpy",
    version="0.0.1",
    author="Chris Hold",
    author_email="Christoph.Hold@aalto.fi",
    description="Spatial Audio Framework (SAF) Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chris-hld/SAFpy",
    project_urls={
        "Bug Tracker": "https://github.com/chris-hld/SAFpy/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    setup_requires=["cffi>=1.0.0"],
    cffi_modules=["safpy_build.py:ffibuilder"],
    install_requires=["cffi>=1.0.0","numpy"],
)
