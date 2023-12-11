import setuptools

long_description = open("README.md", "rt").read()

setuptools.setup(
    name="ntropy-timer",
    version="0.0.2",
    author="Cauê Bittencourt Carnietto",
    author_email="cbcaue@protonmail.com",
    description="Human readable function time measuring.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cacauisadog/ntropy",
    packages=["ntropy"],
    keywords="profiling tuning",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
