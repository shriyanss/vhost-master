# vhost_master v0.0.1
Command line utility to hunt for Virtual Hosts

## Table of contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Example](#example)
- [Social Links](#social-links)

## Features
1. Get the list of IP addresses having different hostnames (*v0.0.1 onwards*)

**Upcoming features:-**
1. Generate output (plain text, JSON, html)
1. Bruteforce VHosts as per user specifies input
1. Generate wordlists
1. Analyze responses to make bruteforcing VHosts easier

## Installation
The tool can be installed with the following command:-

**Install for current user:-**
```
python3 setup.py install --user
```

**Install for all users:-**
```
sudo python3 setup.py install
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
