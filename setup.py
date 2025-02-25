from setuptools import setup, find_packages

setup(
    name="SuperNeva",
    version="0.1.4",
    packages=find_packages(),
    install_requires=[
        "boto3",
        "aws-sqs-consumer",
        "typing",
        "requests",
    ],
    python_requires=">=3.11",
    description="SuperNeva Python SDK",
    author="Berkay Sargın",
    author_email="berkay@nevaxr.com",
    url="https://github.com/nevaxr/superneva-python-sdk",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Typing :: Typed",
    ],
    package_data={
        "AIRunner": ["py.typed", "**/*.py"],
        "AIRunner.AIRunner": ["py.typed", "**/*.py"],
        "AIRunner.SuperNeva": ["py.typed", "**/*.py"],
        "AIRunner.Types": ["py.typed", "**/*.py"],
    },
    include_package_data=True,
)
