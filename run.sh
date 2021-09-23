#!/usr/bin/env bash
set -e
cd $(cd -P -- "$(dirname -- "$0")" && pwd -P) || exit

name="uol_auto_vpn"
dl_address="https://git.raymondt.co.uk/${name}"
run_file="uol_auto_vpn/run.py"

if [[ -n ${1+x} ]]; then
  echo "Downloading"
  cd ~
  mkdir -p $HOME/projects/
  cd $HOME/projects/
  git clone ${dl_address} ${name}  --depth=1 || true
  cd "${name}"
  trash .git || rm -rf .git || true
  echo -e "\nTo run in future please execute .$(realpath run.sh)"
fi

if ! [ -f ${run_file} ]; then
  echo "Script root not found see ${dl_address}"
  exit 1
fi

if ! [ -d venv ]; then
  python3 -m venv venv --clear
  source venv/bin/activate
  pip install --upgrade pip setuptools wheel
  pip install -e .
fi

if ! which openconnect > /dev/null; then
  echo "openconnect not found installing"
  sudo apt-get update
  sudo apt-get install openconnect
fi

source venv/bin/activate
python ${run_file}