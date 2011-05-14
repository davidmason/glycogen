#!/bin/bash

# must be run as super user
#TODO check for super-user permission

# echo `basename $0` $ACT_DIR

# directories used by sugar
#TODO replace these with environment variables
ACTIVITY_DIR=/home/sugar/Activities
LIBRARY_DIR=/usr/lib
EXTENSION_DIR=/usr/share/sugar/extensions

# generate directories for activities
MATH_PRAC_DIR="${ACTIVITY_DIR}/MathogenPrac.activity"

# glycogen library and extension directories
LIB_DIR="${LIBRARY_DIR}/python2.7/site-packages/glycogen"
EXT_DIR="${EXTENSION_DIR}/cpsection/glycogen"


# directories to copy from
HERE=`pwd`
ACTIVITY_FROM="${HERE}/activities"
MATH_PRAC_FROM="${ACTIVITY_FROM}/mathogen_prac/MathogenPrac.activity"
LIB_FROM="${HERE}/site-packages/glycogen"
EXT_FROM="${HERE}/extensions/cpsection/glycogen"


# decide which components to update
# TODO set these from command line arguments
DO_MATH_PRAC=true
DO_LIB=true
DO_EXT=true

# handle backing up of old directories
DO_BACKUP=true
BACKUP_LABEL=".old"

#TODO turn these into a function that takes from and to dir

if $DO_MATH_PRAC ; then
    if $DO_BACKUP ; then
        # remove old backup and copy a new one there
        rm -r $MATH_PRAC_DIR$BACKUP_LABEL
        cp -r $MATH_PRAC_DIR $MATH_PRAC_DIR$BACKUP_LABEL
    fi
    # remove old copy and deploy the source version to the working environment
    rm -r $MATH_PRAC_DIR
    cp -r $MATH_PRAC_FROM $MATH_PRAC_DIR
fi

if $DO_LIB ; then
    if $DO_BACKUP ; then
        # remove old backup and copy a new one there
        rm -r $LIB_DIR$BACKUP_LABEL
        cp -r $LIB_DIR $LIB_DIR$BACKUP_LABEL
    fi
    # remove old copy and deploy the source version to the working environment
    rm -r $LIB_DIR
    cp -r $LIB_FROM $LIB_DIR
fi

if $DO_EXT ; then
    if $DO_BACKUP ; then
        # remove old backup and copy a new one there
        rm -r $EXT_DIR$BACKUP_LABEL
        cp -r $EXT_DIR $EXT_DIR$BACKUP_LABEL
    fi
    # remove old copy and deploy the source version to the working environment
    rm -r $EXT_DIR
    cp -r $EXT_FROM $EXT_DIR
fi


exit
