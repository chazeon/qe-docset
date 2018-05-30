# QE docset

The scripts in this repo is designated to generated a docset for [Quantum ESPRESSO](https://www.quantum-espresso.org/) (QE), an open-source package for electronic-structure calculations and materials modeling at the nanoscale, which should work with offline API Documentation Browsers such as [Dash](https://kapeli.com/dash) and [Zeal](https://zealdocs.org/).

## Usage

This script generate needs to use documents from `Doc` directory from original QE repository.

### Build original code

Download original QE code suite from [official website](https://www.quantum-espresso.org/download), which will show your way to the [GitLab](https://gitlub.com/QEF/q-e) or [GitHub](https://github.com/QEF/q-e) repo, and do the configure and build the doc by running
```sh
./configure [options]
make doc
```

And the generated docs lies in the `Doc/` folder.

### Install the dependencies

The project depends on [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/) and [SQLAlchemy](https://www.sqlalchemy.org/). You can install the dependencies simply by running
```sh
python3 -m pip install -r requirements.txt
```
as long as you have Python's [PIP](https://pypi.org/project/pip/) installed.

### Generating the docset

Edit the `generate.sh`, point the `QE_DOCDIR` variable to the `Doc/` folder such as `~/qe-6.2.1/Doc/`.

Then run the `generate.sh`. It will copy and edit the HTMLs and related resources to `QuantumESPRESSO.docset/Contents/Resources/Documents/`, and generate the index database at `QuantumESPRESSO.docset/Contents/Resources/docSet.dsidx`.

The `QuantumESPRESSO.docset` is what you want to copy to your device.

## Acknolegement

Docset icons, `icon.png` and `icon@2x.png` are derived from QE's [official logo](https://www.quantum-espresso.org/project/logos).

## Known Issues

TOCs for pages do not work right now. This should be fixed in a day or two.

## Additional Information

The code is tested for QE version 6.2.1.