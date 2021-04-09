from setuptools import setup, find_packages

def readme():
    with open("README.md", "r", encoding="utf-8") as f:
        return f.read()

setup(
    name="pyvoqc",
    version="0.1.0",
    author="Kesha Hietala",
    author_email="kesha@cs.umd.edu",
    description="Python wrapper for the VOQC quantum circuit compiler",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/inQWIRE/pyvoqc",
    project_urls={
        "Bug Tracker": "https://github.com/inQWIRE/pyvoqc/issues",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Programming Language :: OCaml",
        "Topic :: Scientific/Engineering",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    python_requires=">=3.6",
    include_package_data=True,
)

