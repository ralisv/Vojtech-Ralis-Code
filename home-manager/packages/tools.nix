{ pkgs, ... }:

{
  home.packages = with pkgs; [
    pwvucontrol # Audio control
    pulseaudio # CLI tools for audio
    brightnessctl
    gparted # For imaging USB drives
    lenovo-legion
    btop
    htop
    amdgpu_top
    coreutils
    unzip
    zip
    xdg-utils
    wayland-utils
    acpi
    man-pages
    timer # CLI timer
    translate-shell # CLI translator
    mullvad-vpn
    keepassxc # Password manager
    wvkbd # Virtual keyboard
    blueberry
  ];
}
