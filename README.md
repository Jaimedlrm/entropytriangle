# Entropy Triangle Package
[![Anaconda-Server Badge](https://anaconda.org/jaimedlrm/entropytriangle/badges/version.svg)](https://anaconda.org/jaimedlrm/entropytriangle)
[![PyPI version](https://badge.fury.io/py/entropytriangle.svg)](https://badge.fury.io/py/entropytriangle)

A Python package to work with entropic coordinates and the entropy triangles defined by Valverde-Albacete and Peláez Moreno in: 

- [100% Classification Accuracy Considered Harmful: The Normalized Information Transfer Factor Explains the Accuracy Paradox](https://www.researchgate.net/publication/259743406_100_Classification_Accuracy_Considered_Harmful_The_Normalized_Information_Transfer_Factor_Explains_the_Accuracy_Paradox)

- [The Evaluation of Data Sources using Multivariate Entropy Tools](https://www.researchgate.net/publication/313460913_The_Evaluation_of_Data_Sources_using_Multivariate_Entropy_Tools)

- [Assessing Information Transmission in Data Transformations with the Channel Multivariate Entropy Triangle](https://www.researchgate.net/publication/326023467_Assessing_Information_Transmission_in_Data_Transformations_with_the_Channel_Multivariate_Entropy_Triangle)

The packages uses NumPy, Pandas, SciPy, Scikit-learn and Matplotlib


# Package Installation


### Pip

The package is stored in [PyPI](https://pypi.org/project/entropytriangle/)

Using pip you can install the current release (0.1.1) using the command:

```bash
pip intstall entropytriangle
```

Note that with pip you may need to use sudo. 

```bash
sudo pip intstall entropytriangle
```

### Anaconda

The package is stored in [Anaconda Cloud](https://anaconda.org/jaimedlrm/entropytriangle)

You can install entropytriangle with the conda command:

```bash
conda config --add channels Jaimedlrm
conda install entropytriangle
```
or :

```bash
conda install -c jaimedlrm entropytriangle
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

# Usage and Examples

You can see [here some use cases](vignettes/) in this link, where you can find some examples of real case scenarios.
