#!/usr/bin/env sh
QE_DOCDIR=

DOCSET_DIR=QuantumESPRESSO.docset
CONTENTS_DIR=$DOCSET_DIR/Contents
RESOURCES_DIR=$CONTENTS_DIR/Resources
DOCUMENTS_DIR=$RESOURCES_DIR/Documents

rm -r $DOCUMENTS_DIR/*
rm $RESOURCES_DIR/docSet.dsidx

cp -rL $(find $QE_DOCDIR/*.html) $QE_DOCDIR/images $DOCUMENTS_DIR
cp -rL $QE_DOCDIR/user_guide $DOCUMENTS_DIR
cp -rL $QE_DOCDIR/developer_man $DOCUMENTS_DIR

python3 generate.py

tar --exclude='.DS_Store' -cvzf QuantumESPRESSO.tgz QuantumESPRESSO.docset