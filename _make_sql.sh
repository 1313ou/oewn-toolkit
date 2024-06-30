#!/bin/bash

DIR=/opt/devel/oewn
BRANCH=pr_quoting
DB=oewn-2024-sqlite-2.1.1-x
SUFFIX=pr

pushd $DIR > /dev/null
./_mymake_sql.sh $BRANCH
popd  > /dev/null

cp $DIR/dist/fromyaml/sql/$DB.sqlite $DB-$SUFFIX.sqlite

