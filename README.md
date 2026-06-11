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
- 6 Sextortion Study with the modern ext API - [![6 Sextortion Ext](https://colab.research.google.com/assets/colab-badge.svg)](https://githubtocolab.com/iknaio/iknaio-api-tutorial/blob/main/06_Sextortion_Study_Ext.ipynb)

## Prerequisites

You need an API key provided by Iknaio. If you would like to get an API key, drop an email to contact@iknaio.com.

As a first step, clone this repository to your local drive

    git clone https://github.com/graphsense/iknaio-api-tutorial.git
    cd iknaio-api-tutorial

Copy the config template file and insert your API key:

    cp config.json.tmp config.json

Open `config.json`, insert your API key and save.

## Run locally with uv

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) if you don't have it yet, then run:

    uv sync
    uv run jupyter notebook

Now you are ready to run the tutorial notebooks!

## Run with Docker

Alternatively, you can run the notebooks in a container without installing anything on your host (apart from [Docker](https://docs.docker.com/get-docker/)):

    docker build -t iknaio-api-tutorial .
    docker run --rm -p 8888:8888 -v "$PWD/config.json:/app/config.json:ro,z" iknaio-api-tutorial

Open the link printed in the terminal (`http://127.0.0.1:8888/tree?token=...`) in your browser.

## The modern `ext` API

The `graphsense.ext` module is the modern take on the API: a hand-written convenience layer on top of the generated client that removes most boilerplate. Instead of wiring up `Configuration`, `ApiClient`, and the right `*Api` class for every call, you work with a single `GraphSense` object:

```python
from graphsense.ext import GraphSense

gs = GraphSense(api_key="...", currency="btc")  # or set GRAPHSENSE_API_KEY in the env

bundle = gs.lookup_address("1Archive...", with_tags=True, with_cluster=True)  # parallel fetch
df = pd.read_csv(io.StringIO(gs.bulk("get_address", addresses, format="csv")))  # bulk to pandas
tags = gs.tags_for("1Archive...")  # pagination handled
gs.raw.clusters.get_cluster("btc", 2647118)  # full raw access when needed
```

For new code we recommend starting with the `ext` API and only dropping down to the generated client (always available under `gs.raw`) for endpoints the facade doesn't cover. Notebook 6 demonstrates this by re-running the sextortion study with it.

## Documentation

Documentation of the API endpoints can be found in the repository of the [GraphSense Python client](https://github.com/graphsense/graphsense-lib/tree/master/clients/python#documentation-for-api-endpoints).

[paper]: https://arxiv.org/abs/1908.01051
