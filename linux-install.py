#!/usr/bin/env python3


import os
import sys


INSTALL_SCRIPT_DIRECTORY = os.path.dirname(os.path.abspath(sys.argv[0]))
USER_HOME_DIRECTORY = os.path.expanduser("~")


SOURCE_TO_DESTINATION_SYMLINK_MAPPING = {
  f"{INSTALL_SCRIPT_DIRECTORY}/.bashrc": f"{USER_HOME_DIRECTORY}/.bashrc",
  f"{INSTALL_SCRIPT_DIRECTORY}/.xonshrc": f"{USER_HOME_DIRECTORY}/.xonshrc",
  f"{INSTALL_SCRIPT_DIRECTORY}/.inputrc": f"{USER_HOME_DIRECTORY}/.inputrc",
  f"{INSTALL_SCRIPT_DIRECTORY}/vs-code-settings.json": f"{USER_HOME_DIRECTORY}/.config/Code/User/settings.json",
  f"{INSTALL_SCRIPT_DIRECTORY}/alacritty.yml": f"{USER_HOME_DIRECTORY}/.config/alacritty/alacritty.yml",
  f"{INSTALL_SCRIPT_DIRECTORY}/shell.nix": f"{USER_HOME_DIRECTORY}/default.nix",
}


for (source, destination) in SOURCE_TO_DESTINATION_SYMLINK_MAPPING.items():
  if not os.path.exists(source):
    print(f"Source path {source} does not exist")
    continue

  if os.path.exists(destination):
    print(f"Path {destination} already exists")
    continue

  if not os.path.exists(os.path.dirname(destination)):
    print(f"Creating directory {os.path.dirname(destination)}")
    os.makedirs(os.path.dirname(destination))

  print(f"Creating symlink {destination} -> {source}")
  os.symlink(source, destination)


def update_nix_configuration():
  try:
    if (input("Do you wish to update configuration.nix file?") in ("y", "")):
      os.system(f"sudo cp {INSTALL_SCRIPT_DIRECTORY}/configuration.nix /etc/nixos/configuration.nix")
    else:
      return
    
    if (input("Do you wish to test new nixos configuration? ") in ("y", "")):
      os.system("sudo nixos-rebuild test")

  except KeyboardInterrupt:
    pass

if os.path.exists("/etc/nixos"):
  update_nix_configuration()