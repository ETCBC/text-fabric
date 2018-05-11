![logo](/images/tf.png)

Text-Fabric is a Python3 package for Text plus Annotations.

It provides a data model, a text file format, and a binary format for (ancient) text plus
(linguistic) annotations.

The emphasis of this all is on:

* data processing
* sharing data
* contributing modules

A defining characteristic is that Text-Fabric does not make use of XML or JSON,
but stores text as a bunch of plain text files.
Each of these files contains the data of a single feature,
aligned with a *graph* of nodes and edges, which make up the
abstract fabric of the text.

## Install

Have [Python3](https://www.python.org/downloads/) on your system.

Optionally install [Jupyter](http://jupyter.org) as well:

```sh
pip3 install jupyter
```

Install Text-Fabric:

```sh
pip3 install text-fabric
```

## Corpora

There are a few corpora in Text-Fabric that are being supported
with extra modules.

### Hebrew Bible

Get the corpus:

```sh
cd ~/github/etcbc
git clone https://github.com/etcbc/bhsa
```

### Cuneiform tablets from Uruk

Get the corpus:

```sh
cd ~/github/Nino-cunei
git clone https://github.com/Nino-cunei/uruk
```

### More

We have example corpora (Greek, Sanskrit, Babylonian),
but these are not supported by extra modules.

```sh
cd ~/github
git clone https://github.com/Dans-labs/text-fabric-data
```

## Getting started

Start programming: write a python script or code in the Jupyter notebook

```sh
cd somewhere-else
jupyter notebook
```

Enter the following text in a code cell

```python
from tf.fabric import Fabric
TF = Fabric(modules=['my/dataset'])
api = TF.load('sp lex')
api.makeAvailableIn(globals())
```

Maybe you have to tell Text-Fabric exactly where your data is.
If you have the data in a directory `text-fabric-data`
under your home directory  or under `~/github`, Text-Fabric can find it.
In your `modules` argument you then specify one or more subdirectories of
`text-fabric-data`.

### Using Hebrew data

To get started with the Hebrew corpus, use its tutorial in the BHSA repo:
[start](http://nbviewer.jupyter.org/github/etcbc/bhsa/blob/master/tutorial/start.ipynb).

Or go straight to the
[bhsa-api-docs](/Api/Bhsa).

### Using Cuneiform data

To get started with the Uruk corpus, use its tutorial in the Nino-cunei repo:
[start](http://nbviewer.jupyter.org/github/nino-cunei/tutorials/blob/master/start.ipynb).

Or go straight to the
[cunei-api-docs](/Api/Cunei).

## History

Most ideas derive from an earlier project, 
[LAF-Fabric](https://github.com/Dans-labs/laf-fabric).
We have taken out everything that makes LAF-Fabric complicated and
all things that are not essential for the sake of raw data processing.