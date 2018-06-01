#!/usr/bin/env bash

QE_SRCDIR=/mnt/c/Standalone/qe-6.2.1
QE_DOCDIR=$QE_SRCDIR/Doc

BUILD_DIR=build
DOCSET_DIR=$BUILD_DIR/QuantumESPRESSO.docset
CONTENTS_DIR=$DOCSET_DIR/Contents
RESOURCES_DIR=$CONTENTS_DIR/Resources
DOCUMENTS_DIR=$RESOURCES_DIR/Documents

RES_DIR=res
SRC_DIR=src

DOC_REL_PATH=Doc/user_guide

# CLEARING GENERATED DOCUMENTS

rm -r $BUILD_DIR

# GENERATE DOCSET DIRECTORIES

mkdir -p $DOCUMENTS_DIR

# COPY RESOURCES

cp $RES_DIR/icon.png $RES_DIR/icon@2x.png $DOCSET_DIR
cp $RES_DIR/Info.plist $CONTENTS_DIR
cp $RES_DIR/logo_header.jpg $DOCUMENTS_DIR

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

python3 $SRC_DIR/gen_db.py

# INDEX PAGE GENERATION

python3 $SRC_DIR/gen_index.py

# GENERATE VERSION FILE

cat $QE_SRCDIR/dev-tools/release.sh | python3 $SRC_DIR/gen_version.py

# CREATING ARCHIVE

tar --exclude='.DS_Store' -cvzf $BUILD_DIR/QuantumESPRESSO.tgz -C $BUILD_DIR QuantumESPRESSO.docset