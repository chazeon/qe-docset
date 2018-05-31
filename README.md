# QE Docset

The scripts in this repo is designated to generated a docset for [Quantum ESPRESSO](https://www.quantum-espresso.org/) (QE), an open-source package for electronic-structure calculations and materials modeling at the nanoscale, which should work with offline API documentation browsers such as [Dash](https://kapeli.com/dash) and [Zeal](https://zealdocs.org/).

## Features

The generated docset includes user's guide, developer's manual, input data descriptions and package-specific documents.

The input data descriptions is the main part of the docset, they are indexed and arranged in the following nomenclature:
* Each package, such as `PW` or `PH` is of type `Package`
* Each `namelist` or `card` in the input is of type `Section`
* Each entry of input is of type `Variable`.

The user's guide, the developer's guide, and package-specific documents are classified in the `Guide` category.

## Usage

This script needs to use documents from `Doc` directory from original QE repository.

### Build original code

Download original QE code suite from [official website](https://www.quantum-espresso.org/download), which will show your way to the [GitLab](https://gitlab.com/QEF/q-e) or [GitHub](https://github.com/QEF/q-e) repo, and do the configure and build the doc by running
```sh
./configure [options]
make doc
```

and the generated docs will lie in the `Doc/` folder.

### Install the dependencies

The project depends on 
[Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/),
[SQLAlchemy](https://www.sqlalchemy.org/),
[requests](http://docs.python-requests.org/en/master/) and
[jinja2](http://jinja.pocoo.org/). You can install these dependencies simply by performing
```sh
python3 -m pip install -r requirements.txt
```
as long as you have Python's [pip](https://pypi.org/project/pip/) installed.

### Generating the docset

Edit the `generate.sh`, point the `QE_SRCDIR` variable to the QE's source code folder such as `~/qe-6.2.1`:
```sh
QE_DOCDIR=~/qe-6.2.1
```

Then run the `generate.sh`. It will:
* Copy the required files for docset from `res` folder;
* Copy and edit the HTMLs and related resources to `QuantumESPRESSO.docset/Contents/Resources/Documents/`;
* Run `src/gen_db.py` to generate the index database at `QuantumESPRESSO.docset/Contents/Resources/docSet.dsidx`;
* Run `src/gen_index.py` to generate the index page `index.html` according to the official website;
* Run `src/gen_version.py` to generate `meta.json` for using in Zeal and `docset.json` for using in submission.

All generated documents will locate in the `build` folder.

The `QuantumESPRESSO.docset` is what you want to copy to your device.

Please note that successfully creating the index page requires the user to maintain a good internet connection.

## Acknowledgement

Docset icons, `icon.png` and `icon@2x.png`, are derived from QE's [official logo](https://www.quantum-espresso.org/project/logos).

## Additional Information

The code is tested for QE version 6.2.1.