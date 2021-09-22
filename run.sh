#!/usr/bin/env bash
set -e
cd $(cd -P -- "$(dirname -- "$0")" && pwd -P) || exit

name="uol_auto_vpn"
dl_address="https://git.raymondt.co.uk/${name}"

if [ "$1" -gt "-1" ]; then
  echo "Downloading"
  cd ~
  mkdir -p $HOME/projects/
  cd $HOME/projects/
  git clone ${dl_address} ${name}  --depth=1 || true
  cd "${name}"
  trash .git || rm -rf .git || true
  echo -e "\nTo run in future please execute .$(realpath run.sh)"
fi

if ! [ -f uol_auto_vpn.py ]; then
  echo "Script root not found see ${dl_address}"
  exit 1
fi

if ! [ -d venv ]; then
  python3 -m venv venv --clear
  source venv/bin/activate
  pip install --upgrade pip setuptools wheel
  pip install -r requirements.txt
fi

source venv/bin/activate
python uol_auto_vpn.py