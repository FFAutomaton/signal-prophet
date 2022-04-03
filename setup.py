import setuptools

REQUIRED_PACKAGES = ['prophet==1.0.1', 'pandas==1.3.5',
                     'turkish_gekko_binance_service @ git+https://github.com/turkish-gekko/service-binance-rest@main#egg=turkish_gekko_binance_service']

# dependency_links=[
#         "git+git://github.com/turkish-gekko/service-binance-rest@master#egg=turkish_gekko_binance_service",
#     ],
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="signal_prophet",
    version="1.0",
    author="turkish gekko",
    author_email="turkish-gekko@turkish-gekko.org",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/turkish-gekko/signal-prophet",
    install_requires=REQUIRED_PACKAGES,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
