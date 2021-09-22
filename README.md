# UoL Auto VPN

Automatically extract a VPN cookie from remote.lincoln.ac.uk and connect. For faster access fill in env.json.

## Usage

```bash
python uol_auto_vpn/run.py
```

## Setup

```bash
# Requirements
# sudo apt install python3 python3-venv openconnect
./run.sh
```

## One line run

This will install the repo to `~/projects/uol_auto_vpn"`. 
Where you can add to the configuration.

```bash 
wget -qO - https://raw.githubusercontent.com/RaymondKirk/uol_auto_vpn/main/run.sh | bash -s 1
```