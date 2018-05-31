import sys
import json
import re

def get_versions() -> (str, str):
    version_f90 = sys.stdin.read()
    version_number = re.search(r"version_number\s*=\s*'(\d+\.\d+)'", version_f90).group(1)
    svn_revision = re.search(r"svn_revision\s*=\s*'(\d+)'", version_f90).group(1)
    return version_number, svn_revision

if __name__ == '__main__':

    version_number, svn_revision = get_versions()
    docset_version = "%s.%s" % (version_number, svn_revision)

    with open('docset.json', 'w', encoding='utf8') as fp:
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

    with open('meta.json', 'w', encoding='utf8') as fp:
        json.dump({
            "name": "QuantumESPRESSO",
            "revision": "0",
            "title": "Quantum ESPRESSO",
            "version": docset_version
        }, fp, indent=4)
