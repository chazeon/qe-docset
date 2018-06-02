import sys
import json
import re

def get_versions() -> (str, str):
    version_f90 = sys.stdin.read()
    version_number = re.search(r"version=([0-9\.]+)", version_f90).group(1)
    revision_res = re.search(r"revision=(\d+)", version_f90)
    svn_revision = revision_res.group(1) if revision_res else None
    return version_number, svn_revision

if __name__ == '__main__':

    version_number, svn_revision = get_versions()
    docset_version = "%s (r%s)" % (version_number, svn_revision) if svn_revision else version_number

    with open('build/docset.json', 'w', encoding='utf8') as fp:
        json.dump({
            "name": "Quantum ESPRESSO",
            "version": docset_version,
            "archive": "QuantumESPRESSO.tgz",
            "author": {
                "name": "Chenxing Luo",
                "link": "https://github.com/chazeon"
            },
            "aliases": ["qe", "quantum-espresso"]
        }, fp, indent=4)

    with open('build/meta.json', 'w', encoding='utf8') as fp:
        json.dump({
            "name": "QuantumESPRESSO",
            "revision": "0",
            "title": "Quantum ESPRESSO",
            "version": docset_version
        }, fp, indent=4)
