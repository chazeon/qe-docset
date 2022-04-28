# QE Docset

The scripts in this repo is designated to generated a docset for [Quantum ESPRESSO](https://www.quantum-espresso.org/) (QE), an open-source package for electronic-structure calculations and materials modeling at the nanoscale, which should work with offline API documentation browsers such as [Dash](https://kapeli.com/dash) and [Zeal](https://zealdocs.org/).

## How to scrape and build docset

First, install the required dependencies

```bash
python3 -m pip install -r requirements.txt
```

then run the scripts

```bash
mkdir -p qe.docset/Contents/Resources/Documents
python3 scripts/scrape.py
python3 scripts/docs2set.py
```

## Prebuilt docset

[![Build docset](https://github.com/chazeon/qe-docset/actions/workflows/build.yml/badge.svg)](https://github.com/chazeon/qe-docset/actions/workflows/build.yml)

- Avaliable as [GitHub Action Artifact](https://github.com/chazeon/qe-docset/actions/workflows/build.yml) (or via [direct link](https://nightly.link/chazeon/qe-docset/workflows/build/master/qe.docset.zip)).

## Acknowledgement

Docset icons, `icon.png` and `icon@2x.png`, are derived from QE's [official logo](https://www.quantum-espresso.org/project/logos).
