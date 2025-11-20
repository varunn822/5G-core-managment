from setuptools import setup, find_packages

setup(
    name="5g-core-management-prototype",
    version="1.0.0",
    author="5G Learning Initiative",
    author_email="support@5g-learning.org",
    description="A hands-on learning environment for 5G core network management",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/5g-learning/5g-core-management-prototype",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Intended Audience :: Telecommunications Industry",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Education",
        "Topic :: System :: Networking",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pyang",
        "lxml",
        "ncclient",
        "flask",
        "pysnmp",
    ],
    entry_points={
        "console_scripts": [
            "5g-prototype-install=install_dependencies:main",
            "5g-prototype-run=run_all:main",
        ],
    },
)