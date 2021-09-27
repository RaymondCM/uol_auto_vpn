# UoL Auto VPN

![](https://github.com/RaymondKirk/uol_auto_vpn/workflows/build/badge.svg)

Automatically extract a VPN cookie from remote.lincoln.ac.uk and connect. For faster access fill in env.json.

## Documentation

Please refer to the [documentation](https://raymondkirk.github.io/uol_auto_vpn/) for installation instructions and API usage.

## Usage

### Method One (Best)

One line installer. 

```bash 
wget -qO - https://raw.githubusercontent.com/RaymondKirk/uol_auto_vpn/main/install.sh | bash
```

Once installed run from any terminal window via the command ```uol_auto_vpn```.

### Method Two (Pip)

```bash 
pip install uol_auto_vpn
uol_auto_vpn
```

### Method Three (Source)

```bash
sudo apt install python3 python3-venv openconnect
git clone https://github.com/uol_auto_vpn --depth 1
cd uol_auto_vpn
python3 -m venv venv --clear
source venv/bin/activate
pip install -e .
uol_auto_vpn  # or => python uol_auto_vpn/run.py
```
