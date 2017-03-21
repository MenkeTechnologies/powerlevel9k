#!/bin/sh

# Install ZSH
sudo pkg install -y zsh
sudo chsh -s `which zsh` vagrant
sudo ln -s /usr/local/bin/zsh /usr/bin/zsh

# Install git
sudo pkg install -y git