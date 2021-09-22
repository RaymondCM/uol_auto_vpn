#!/usr/bin/env bash
cd "$(cd -P -- "$(dirname -- "$0")" && pwd -P)" || (echo "Cannot cd to correct dir of bash script, exiting." && exit)
pip install sphinx sphinx-rtd-theme
rm -rf source/api
sphinx-apidoc -f -o source/api ../uol_auto_vpn
make clean
make html