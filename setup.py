from setuptools import setup


with open('README.txt') as file:
    long_description = file.read()

classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
]

setup(
    name="entropy-triangle",
    version="1.0.2",
    packages=['ternary'],
    install_requires=["matplotlib>=1.4"],
    author="Jaime de los Ríos Mouvet",
    author_email="jaime.delosriosmouvet@gmail.com",
    classifiers=classifiers,
    description="Calculation of the entropy trinagles",
    long_description=long_description,
    keywords="Entropy Triangle Information Theory",
    license="MIT",
    url="https://github.com/Jaimedlrm/entropytriangle",
    download_url="https://github.com/Jaimedlrm/entropytriangle.git",
)