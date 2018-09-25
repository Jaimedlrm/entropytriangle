# Entropy Triangle Package
[![PyPI version](https://badge.fury.io/py/entropytriangle.svg)](https://badge.fury.io/py/entropytriangle)
[![Anaconda-Server Badge](https://anaconda.org/jaimedlrm/entropytriangle/badges/version.svg)](https://anaconda.org/jaimedlrm/entropytriangle)

A Python package to work with entropic coordinates and the entropy triangles defined in: 

- [100% Classification Accuracy Considered Harmful: The Normalized Information Transfer Factor Explains the Accuracy Paradox](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0084217)

- [The Evaluation of Data Sources using Multivariate Entropy Tools](https://www.sciencedirect.com/science/article/pii/S0957417417300805)

- [Assessing Information Transmission in Data Transformations with the Channel Multivariate Entropy Triangle](https://www.mdpi.com/1099-4300/20/7/498)

The packages uses NumPy, Pandas, SciPy, Scikit-learn and Matplotlib


# Package Installation


### Pip

The package is stored in [PyPI](https://pypi.org/project/entropytriangle/)

Using pip you can install the current release (0.1.1) using the command:

```bash
pip install entropytriangle
```

Note that with pip you may need to use sudo. 

```bash
sudo pip install entropytriangle
```


### With setup.py

Alternatively you can clone the repository and run `setup.py` in the usual manner:

```bash
git clone https://github.com/Jaimedlrm/entropytriangle.git
cd entropytriangle
python setup.py install
```

Note that you may need

```bash
sudo python setup.py install
```


### Anaconda

The package is stored in [Anaconda Cloud](https://anaconda.org/jaimedlrm/entropytriangle)

It is just available at the moment for osx-64

You can install entropytriangle with the conda command:

```bash
conda config --add channels Jaimedlrm
conda install entropytriangle
```
or :

```bash
conda install -c jaimedlrm entropytriangle
```


# Usage and Examples

You can see [here some use cases](vignettes/) in this link, where you can find some examples of real case scenarios.
