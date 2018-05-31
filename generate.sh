#!/usr/bin/env bash

QE_SRCDIR=/mnt/c/Standalone/qe-6.2.1
QE_DOCDIR=$QE_SRCDIR/Doc

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
cp -rL $QE_DOCDIR/user_guide.pdf $DOCUMENTS_DIR
cp -rL $QE_DOCDIR/developer_man $DOCUMENTS_DIR
cp -rL $QE_DOCDIR/developer_man.pdf $DOCUMENTS_DIR

# INPUT DATA DESCRIPTION

cp -rL $(find $QE_DOCDIR/*.html) $QE_DOCDIR/images $DOCUMENTS_DIR

# PACKAGE-SPECIFIC DOCUMENTATION

for PACKAGE_NAME in CPV NEB PHonon PP PW
do
    cp -rL $QE_SRCDIR/$PACKAGE_NAME/$DOC_REL_PATH \
        $DOCUMENTS_DIR/$(echo $PACKAGE_NAME | sed 's/[[:lower:]]//g' | tr '[:upper:]' '[:lower:]')_user_guide
    cp -rL $QE_SRCDIR/$PACKAGE_NAME/$DOC_REL_PATH.pdf \
        $DOCUMENTS_DIR/$(echo $PACKAGE_NAME | sed 's/[[:lower:]]//g' | tr '[:upper:]' '[:lower:]')_user_guide.pdf
done

# DATABASE GENERATION

python3 gen_db.py

# INDEX PAGE GENERATION

python3 gen_index.py
cp logo_header.jpg $DOCUMENTS_DIR/

# GENERATE VERSION FILE

cat $QE_SRCDIR/Modules/version.f90 | python3 gen_version.py

# CREATING ARCHIVE

tar --exclude='.DS_Store' -cvzf QuantumESPRESSO.tgz QuantumESPRESSO.docset