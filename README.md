# vhost_master v0.0.3
Command line utility to hunt for Virtual Hosts

## Table of contents
- [Features](#features)
- [Installation](#installation)
    - [Using `pip` (recommeded)](#using-pip-recommeded)
    - [Manually using source](#manually-using-source)
- [Upgrade the tool](#upgrade-the-tool)
- [Usage](#usage)
- [Example](#example)
- [Social Links](#social-links)

## Features
1. Get the list of IP addresses having different hostnames (*v0.0.1 onwards*)

**Upcoming features:-**
1. Generate output (plain text, JSON, html)
1. Bruteforce VHosts as per user specified input
1. Generate wordlists
1. Analyze responses to make bruteforcing VHosts easier

## Installation
The tool can be installed with the following command:-

### Using `pip` (recommeded)
You can install this tool by simply running the following command:-
```
pip3 install vhost-master
```
OR
```
python3 -m pip install vhost-master
```

### Manually using source
Download and extract files from one of the releases from https://github.com/shriyanss/vhost-master/releases. Then,


**Install for current user:-**
```
python3 setup.py install --user
```

**Install for all users:-**
```
sudo python3 setup.py install
```

**NOTE: If you install directly from `git clone`, you might encounter some errors. So, consider installing from [releases](https://github.com/shriyanss/vhost-master/releases) instead**

## Upgrade the tool
If you see a message that says that the tool is outdated, you can simply upgrade it using `pip`:-
```
pip3 install vhost-master --upgrade
```

## Usage
```
Usage: cat subdomains.txt | vhost_master
```

## Example
Suppose you have a list of subdomains and you want to get the IP addresses, on which VHost fuzzing can be done. Assuming the subdomains file to be `subdomains.txt`, you'll run the following command:-
```
cat subdomains.txt | vhost_master
```

If you just want to print IP addresses and not other messages, you can use the following command:-
```
cat subdomains.txt | vhost_master -s
```

## Social Links
If you liked this tool, please consider following me ;)
- X (Formerly Twitter): [@ss0x00](https://twitter.com/ss0x00)
- LinkedIn: [@shriyans-sudhi](https://www.linkedin.com/in/shriyans-sudhi/)
