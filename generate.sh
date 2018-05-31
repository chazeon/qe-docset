#!/usr/bin/env bash

QE_DOCDIR=/mnt/c/Standalone/qe-6.2.1/Doc

DOCSET_DIR=QuantumESPRESSO.docset

CONTENTS_DIR=$DOCSET_DIR/Contents
RESOURCES_DIR=$CONTENTS_DIR/Resources
DOCUMENTS_DIR=$RESOURCES_DIR/Documents

DOC_REL_PATH=Doc/user_guide

# CLEARING GENERATED DOCUMENTS

rm -r $DOCUMENTS_DIR/*
rm $RESOURCES_DIR/docSet.dsidx

# GENERAL USER GUIDE

cp -rL $QE_DOCDIR/user_guide $DOCUMENTS_DIR
cp -rL $QE_DOCDIR/developer_man $DOCUMENTS_DIR

# INPUT DATA DESCRIPTION

cp -rL $(find $QE_DOCDIR/*.html) $QE_DOCDIR/images $DOCUMENTS_DIR

# PACKAGE-SPECIFIC DOCUMENTATION

for PACKAGE_NAME in CPV NEB PHonon PP PW
do
    cp -rL $QE_DOCDIR/../$PACKAGE_NAME/$DOC_REL_PATH \
        $DOCUMENTS_DIR/$(echo $PACKAGE_NAME | sed 's/[[:lower:]]//g' | tr '[:upper:]' '[:lower:]')_user_guide
done

# INDEX GENERATION

python3 generate.py

# CREATING ARCHIVE

tar --exclude='.DS_Store' -cvzf QuantumESPRESSO.tgz QuantumESPRESSO.docset