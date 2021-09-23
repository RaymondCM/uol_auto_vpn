# UoL Auto VPN

![](https://github.com/RaymondKirk/uol_auto_vpn/workflows/build/badge.svg)

Automatically extract a VPN cookie from remote.lincoln.ac.uk and connect. For faster access fill in env.json.

## Documentation

Please refer to the [documentation](https://raymondkirk.github.io/uol_auto_vpn/) for installation instructions and API usage.

## Usage
### Method One

One line installer. 

```bash 
wget -qO - https://raw.githubusercontent.com/RaymondKirk/uol_auto_vpn/main/run.sh | bash -s 1
```

This will install the repo to `~/projects/uol_auto_vpn"`. Where you can add to the configuration.


### Method Two

```bash
git clone https://github.com/uol_auto_vpn --depth 1
cd uol_auto_vpn
./run.sh  # or python uol_auto_vpn/run.py
```
