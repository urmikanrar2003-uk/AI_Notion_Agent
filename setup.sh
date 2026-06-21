#!/bin/bash
# Install Node.js 20 (LTS) via NodeSource — required for mcp-remote
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs
