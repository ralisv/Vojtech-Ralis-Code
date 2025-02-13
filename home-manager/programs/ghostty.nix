{
  programs.ghostty = {
    enable = true;

    settings = {
      background = "#000000";
      background-opacity = 0.7;

      cursor-style = "bar";
      cursor-style-blink = true;

      font-family = "FiraCode Nerd Font Ret";
      font-size = 9;

      initial-command = "xonsh";

      window-decoration = false;
      window-padding-x = 8;
      window-padding-y = 6;

      resize-overlay = "never";

      scrollback-limit = 10000;

      confirm-close-surface = false;

      shell-integration-features = "sudo";
    };
  };
}
