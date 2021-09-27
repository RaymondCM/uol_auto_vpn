#!/usr/bin/env bash
set -e
cd $(cd -P -- "$(dirname -- "$0")" && pwd -P) || exit

name="uol_auto_vpn"
dl_address="https://git.raymondt.co.uk/${name}"
run_file="uol_auto_vpn/run.py"
command_file="/usr/local/bin/${name}"
install_location=${1:-"/usr/share"}

# Download and install
echo "Installing to ${install_location}"

if [ -d "${install_location}/${name}" ]; then
  echo -n "${name} already appears to be installed in ${install_location}. Would you like to overwrite (y/n)? "
  read -r answer
  if [ "$answer" != "${answer#[Yy]}" ]; then
      echo "Removing '${install_location}/${name}'"
      sudo rm -rf "${install_location}/${name}"
      sudo rm -f "${command_file}" || true
  else
    echo "Okay not installing. Exiting."
    exit
  fi
fi

if ! [ -d "${install_location}/${name}" ]; then
  cd "${install_location}"
  sudo chown -R "$(id -u):$(id -g)" "${install_location}"

  git clone ${dl_address} "${name}" --depth=1 || true

  cd "${name}"

  if ! [ -f "${command_file}" ]; then
    echo "Creating '${command_file}'"
    w_com="cat > ${command_file}"
    sudo bash -c "${w_com}" << EOF
#!/bin/bash
set -e
cd "${install_location}"
cd "${name}"
source venv/bin/activate
python ${run_file}
EOF
    sudo chmod +x "${command_file}"
    sudo chown -R "$(id -u):$(id -g)" "${command_file}"
  fi

  echo -e "\nTo run in future please execute ${name}"
fi

cd "${install_location}"
cd "${name}"

if ! [ -f ${run_file} ]; then
  echo "Script root not found see ${dl_address}"
  exit 1
fi

# Install to virtual environment with highest supported python version
if ! [ -d venv ]; then
  _python=python3
  if command -v python3.9 > /dev/null; then
    _python=python3.9
  elif command -v python3.8 > /dev/null; then
    _python=python3.8
  elif command -v python3.7 > /dev/null; then
    _python=python3.7
  elif command -v python3.6 > /dev/null; then
    _python=python3.7
  elif command -v python3 > /dev/null; then
    _python=python3
  else
      echo "Could not find a suitable python3 version on your system."
      exit 1
  fi

  echo "Installing ${name} with python $(${_python} -c "import sys;print('.'.join(map(str, sys.version_info[:3])))")"

  ${_python} -m venv venv --clear
  source venv/bin/activate
  pip install --upgrade pip setuptools wheel
  pip install -e .
fi

if ! command -v openconnect > /dev/null; then
  echo -n "Package 'openconnect' is required. Would you like to install (y/n)? "
  read -r answer
  if [ "$answer" != "${answer#[Yy]}" ]; then
      echo "Installing 'openconnect'"
      sudo apt-get update
      sudo apt-get install openconnect
  else
    echo "Okay not installing. Exiting."
    exit
  fi
fi

echo -e "\n\nPackage installed. source your bash environment then run '${name}'"