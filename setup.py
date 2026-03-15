from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

with open("README.md") as readme_file:
    readme = readme_file.read()
    
setup(
    name="prompttune",
    version="0.1.0",
    description="A Prompt Optimization Framework Inspired by REVOLVE and TextGrad",
    python_requires=">=3.9",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.9",
    ],
    license="MIT license",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/Peiyance/REVOLVE",
    author="Peiyan Zhang",
    author_email="pzhangao@cse.ust.hk",
    packages=find_packages(include=["prompttune", "prompttune.*"]),
    include_package_data=True,
    install_requires=requirements,
    extras_require={
        "vllm": ["vllm"],
    },
    zip_safe=False,
)
