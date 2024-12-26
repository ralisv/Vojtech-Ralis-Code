{ config, pkgs, ... }:

{
  imports = [
    ./hyprland/hyprland.nix
    ./programs/lsd.nix
    ./programs/alacritty.nix
  ];

  home.username = "ralis";
  home.homeDirectory = "/home/ralis";

  home.stateVersion = "24.05"; # Don't modify

  home.packages = with pkgs; [
  ];

  gtk.enable = true;

  gtk.theme.name = "Sweet-Dark-v40";

  home.file = { };

  home.sessionVariables = {
    EDITOR = "micro";
  };

  # Let Home Manager install and manage itself.
  programs.home-manager.enable = true;
}
