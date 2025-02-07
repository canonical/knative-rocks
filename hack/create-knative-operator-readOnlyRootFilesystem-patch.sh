#!/bin/bash

set -xe

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
KNATIVE_OP=$SCRIPT_DIR/../knative-operator

# cleanup patches
rm $KNATIVE_OP/patches/*

# Copy the git tag from `knative-operator` rock
TARGET_TAG=$(cat $KNATIVE_OP/rockcraft.yaml | yq ".parts.operator.source-tag")

cd /tmp
git clone https://github.com/knative/operator knative-operator
cd knative-operator
git checkout $TARGET_TAG

# create the patch
find . -type f \
	-exec sed -i \
	"s#readOnlyRootFilesystem: true#readOnlyRootFilesystem: false#g" \
	{} +
git add . && git commit -m "readOnlyRootFilesystem false"
git format-patch -1 HEAD
# 0001-readOnlyRootFilesystem-false.patch

# Copy back the patch
cd $KNATIVE_OP
cp /tmp/knative-operator/0001-readOnlyRootFilesystem-false.patch patches

# cleanup cloned repo
rm -rf /tmp/knative-operator
