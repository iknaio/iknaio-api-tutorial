# Iknaio API Tutorial

This tutorial demonstrates how to use the [GraphSense REST API](https://api.ikna.io) hosted by [Iknaio Cryptoasset Analytics GmbH](https://www.ikna.io) for conducting advanced, data-driven analytics tasks.

This tutorial uses sample data provided by BMF.

## Prerequisites

You need an API key provided by Iknaio.

You need Python >= 3.8

	python --version

## Notebook preparation

The tutorial will make use of several notebooks, which are available in this repository.

You can run the notebooks locally, as follows:

Setup a Python environment with [Anaconda](https://www.anaconda.com/products/distribution):

    conda env create -f environment.yml
    conda activate iknaio-api-tutorial

Copy the config temp file and enter your Iknaio API key

    cp config.json.tmp config.json
    vi config.json

Run the jupyter notebooks

    jupyter notebook

