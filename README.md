# vhost_master v0.0.4
Command line utility to hunt for Virtual Hosts

## Table of contents
- [Features](#features)
- [Installation](#installation)
    - [Using `pip` (recommeded)](#using-pip-recommeded)
    - [Manually using source](#manually-using-source)
    - [Use without installation](#use-without-installation)
- [Upgrade the tool](#upgrade-the-tool)
- [Usage](#usage)
- [Examples](#examples)
- [Social Links](#social-links)

## Features
1. Get the list of IP addresses having different hostnames (*v0.0.1 onwards*)
1. Bruteforce VHosts as per user specified input (*v0.0.3 onwards*)

**Upcoming features:-**
1. Generate output (plain text, JSON, html)
1. Generate wordlists
1. Analyze responses to make bruteforcing VHosts easier

Other features requested can be found on the [issues tab](https://github.com/shriyanss/vhost-master/issues?q=is%3Aopen+is%3Aissue+label%3Aenhancement)

## Installation
The tool can be installed with the following command:-

### Using `pip` (recommeded)
You can install this tool by simply running the following command (not running as root might not be able to add it to path, so direct execution might not be possible):-
```
sudo pip3 install vhost-master
```
OR
```
sudo python3 -m pip install vhost-master
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

### Use without installation
If you want to use the script without installing the tool, you can execute `vhost_master-runner.py`. E.g.
```
cat subdomains.txt | python3 vhost_master-runner.py
```

All the options remains the same

<!-- **NOTE: If you install directly from `git clone`, you might encounter some errors. So, consider installing from [releases](https://github.com/shriyanss/vhost-master/releases) instead** -->

## Upgrade the tool
If you see a message that says that the tool is outdated, you can simply upgrade it using `pip`:-
```
pip3 install vhost-master --upgrade
```

## Usage
```
Usage: cat subdomains.txt | vhost_master
```

```
usage: vhost_master-runner.py [-h] [-s] [-b] [-c CONDITIONS] [-w WORDLIST] [-t THREADS] [-p PROTOCOL]
                              [--force-all-ports]

optional arguments:
  -h, --help            show this help message and exit
  -s, --silent          Silent mode (boolean flag)
  -b, --bruteforce      Bruteforce using the given wordlist
  -c CONDITIONS, --conditions CONDITIONS
                        Conditions to consider if a valid VHost exists. See https://github.com/shriyanss/vhost-
                        master/match_conditions.md
  -w WORDLIST, --wordlist WORDLIST
                        Wordlist to use (required with -b/--bruteforce)
  -t THREADS, --threads THREADS
                        Number of threads (default=30)
  -p PROTOCOL, --protocol PROTOCOL
                        Protocol to use (default="http:80,https:443"
  --force-all-ports     If both http:80 & https:443 are open, tool will skip http:80 and show results for https:443.
                        Use this flag to disable it
```

## Examples
Suppose you have a list of subdomains and you want to get the IP addresses, on which VHost fuzzing can be done. Assuming the subdomains file to be `subdomains.txt`, you'll run the following command:-
```
cat subdomains.txt | vhost_master
```

If you just want to print IP addresses and not other messages, you can use the following command:-
```
cat subdomains.txt | vhost_master -s
```

If you want to bruteforce with a wordlist, and filter status codes 404 and 400, here's an example:-
```
cat subdomains.txt | vhost_master -b -w wordlist.txt --conditions "status!=404,status!=400"
```

In this example, if both port 80 and 443 are open, tool will skip port 80 and just scan 443. To scan both ports, use the flag `--force-all-ports`
```
cat subdomains.txt | vhost_master -b -w wordlist.txt --conditions "status!=404,status!=400" --force-all-ports
```

## Social Links
If you liked this tool, please consider following me ;)
- X (Formerly Twitter): [@ss0x00](https://twitter.com/ss0x00)
- LinkedIn: [@shriyans-sudhi](https://www.linkedin.com/in/shriyans-sudhi/)
