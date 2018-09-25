from setuptools import setup,find_packages

classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
]

with open('README.txt') as file:
    long_description = file.read()
    
with open('requirements.txt') as reqs:
	install_requires = reqs.read().splitlines()

print(find_packages())
setup(
    name="entropytriangle",
    version="1.0.1",
    packages= find_packages(),
    python_requires='>=3',
    install_requires = install_requires,
    author="Jaime de los Rios Mouvet",
    author_email="jaime.delosriosmouvet@gmail.com",
    classifiers=classifiers,
    description="Calculation of the entropy triangles",
    long_description=long_description,
    keywords="Entropy Triangle Information Theory",
    license="MIT",
    url="https://github.com/Jaimedlrm/entropytriangle",
    download_url="https://github.com/Jaimedlrm/entropytriangle.git",
)

