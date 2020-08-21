import setuptools

#with open("README.rst", "r") as fh:
#    long_description = fh.read()

setuptools.setup(
    name="pyinstrumentation",
    version="0.9.4",
    install_requires = [
        'pyserial==3.4',
        'PyQt5==5.15.0',
        'numpy>=1.19.1',
        'pyqtgraph==0.11.0'
    ],
    author="Propulsao Juiter",
    author_email="patricksampaio@usp.br",
    description="Instrumentation for static test.",
    #long_description=long_description,
    #long_description_content_type="text/markdown",
    url="https://github.com/Projeto-Jupiter/PyInstrumentation",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',
)