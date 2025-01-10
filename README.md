# Iknaio API Tutorial

This tutorial demonstrates how to use the [GraphSense REST API](https://api.ikna.io) hosted by [Iknaio Cryptoasset Analytics GmbH](https://www.ikna.io) for conducting advanced, data-driven analytics tasks.

The example dataset is a subset of data taken from [a scientific study investigating sextortion spam][paper].

## Open in Google Colab

Google colab offers a zero setup notebook environment. The only thing needed is a Google account to load our notebooks.
Click the following links to open the notebooks.

- 1 Inspect BTC Addresses - [![1 Inspect BTC Addresses](https://colab.research.google.com/assets/colab-badge.svg)](https://githubtocolab.com/iknaio/iknaio-api-tutorial/blob/main/01_Inspect_BTC_address.ipynb)
- 2 Sextortion Study - [![2 Sextortion Study](https://colab.research.google.com/assets/colab-badge.svg)](https://githubtocolab.com/iknaio/iknaio-api-tutorial/blob/main/standalone/02_Sextortion_Study.ipynb)
- 3 Entities Demo - [![3 Entities Demo](https://colab.research.google.com/assets/colab-badge.svg)](https://githubtocolab.com/iknaio/iknaio-api-tutorial/blob/main/03_Basic_Entities_Demo.ipynb)
- 4 Path Search - [![4 Path Search](https://colab.research.google.com/assets/colab-badge.svg)](https://githubtocolab.com/iknaio/iknaio-api-tutorial/blob/main/04_Path_Search.ipynb)
- 5 Alice DWM - [![5 Alice](https://colab.research.google.com/assets/colab-badge.svg)](https://githubtocolab.com/iknaio/iknaio-api-tutorial/blob/main/standalone/05_alice_dwm.ipynb)
## Prerequisites

You need an API key provided by Iknaio.

You need Python >= 3.8

	python --version

## Notebook preparation

The tutorial will make use of several notebooks, which are available in this repository.

As a first step, clone this repository to your local drive

    git clone https://github.com/graphsense/iknaio-api-tutorial.git
    cd iknaio-api-tutorial

You can run the notebooks locally, as follows:

Setup a Python environment with [Anaconda](https://www.anaconda.com/products/distribution):

    conda env create -f environment.yml
    conda activate iknaio-api-tutorial

Copy the config template file:

    cp config.json.tmp config.json

Run the jupyter notebooks

    jupyter notebook

Open `config.json`, insert your API key and save.

Now you are ready to run the tutorial notebooks!


## Documentation

Documentation of the API endpoints can be found in the repository of the [GraphSense Python client](https://github.com/graphsense/graphsense-python/#documentation-for-api-endpoints).

[paper]: https://arxiv.org/abs/1908.01051
