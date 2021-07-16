#!/bin/sh
# For best results run this in a manylinux docker container or AL2 container
# Some packages ignore the `plat-name` build option

# target build platform options: https://github.com/pypa/manylinux
PLATFORM=manylinux1_x86_64
TARGET_DIR=./lambda_package/lambda_wheel/

. ./venv/bin/activate
pip install -e ".[deploy]"
python -m pip wheel \
  --wheel-dir="$TARGET_DIR" \
  --build-option "--plat-name=$PLATFORM" \
  --no-binary ":all:" \
  -e .

cp ./lambda_package_files/* ./lambda_package/.
mkdir ./lambda_package/src
cp src/keep_actions_alive.py ./lambda_package/src/.
cp src/lambda.py ./lambda_package/src/.
cp ./setup.cfg ./lambda_package/.
cp ./setup.py ./lambda_package/.
