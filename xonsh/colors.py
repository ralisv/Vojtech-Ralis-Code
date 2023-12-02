import os
from stat import S_IXUSR
from typing import List
from pathlib import Path
from colorama import Fore
import colorsys
from random import randint

LS_COLORS = open(f"{os.path.expanduser('~')}/Config-Files/ls-colors.txt").read()
""" The contents of the LS_COLORS environment variable """

LS_COLORS_PARSED = dict(
    map(lambda assignment: assignment.split(sep="="), LS_COLORS.split(sep=":"))
)
""" LS_COLORS parsed into a dictionary where the keys are file types and the values are color codes """

GIT_STATUS_COLORS = {
    "STAGED": Fore.LIGHTGREEN_EX,
    "??": Fore.YELLOW,
    "M": Fore.BLUE,
    "A": Fore.GREEN,
    "D": Fore.RED,
    "R": Fore.GREEN,
    "C": Fore.GREEN,
    "U": Fore.RED,
    "DU": Fore.RED,
    "AU": Fore.RED,
    "UD": Fore.RED,
    "UA": Fore.RED,
    "DA": Fore.RED,
    "AA": Fore.RED,
    "UU": Fore.RED,
}

DEFAULT_RAINBOW_RESOLUTION = 10
RAINBOW_INDEX = randint(0, DEFAULT_RAINBOW_RESOLUTION - 1)


def get_file_color(path: Path) -> str:
    ext = f"*{path.suffix}"

    color = None

    if path.is_file() and ext in LS_COLORS_PARSED:
        color = LS_COLORS_PARSED[ext]

    # If the file is a directory, get the directory color
    if path.is_dir():
        color = LS_COLORS_PARSED.get("di")

    # If the file is a symbolic link, get the link color
    elif path.is_symlink():
        color = LS_COLORS_PARSED.get("ln")

    # If the file is a fifo pipe, get the pipe color
    elif path.exists() and path.is_fifo():
        color = LS_COLORS_PARSED.get("pi")

    # If the file is a socket, get the socket color
    elif path.exists() and path.is_socket():
        color = LS_COLORS_PARSED.get("so")

    # If the file is a block (buffered) special file, get the block color
    elif path.exists() and path.is_block_device():
        color = LS_COLORS_PARSED.get("bd")

    # If the file is a character (unbuffered) special file, get the character color
    elif path.exists() and path.is_char_device():
        color = LS_COLORS_PARSED.get("cd")

    # If the file is a symbolic link and orphaned, get the orphan color
    elif path.is_symlink() and not path.resolve() == path:
        color = LS_COLORS_PARSED.get("or")

    # If the file is a regular file and an executable
    elif path.is_file() and path.stat().st_mode & S_IXUSR:
        color = LS_COLORS_PARSED.get("ex")

    if color is None:
        color = LS_COLORS_PARSED.get("rs")

    return f"\033[{color}m"


def colorize(filename: str, color: str = "") -> str:
    """
    Returns the filename enclosed in the color escape sequence based on LS_COLORS
    It is required that at least rs (reset) color is defined in LS_COLORS, as it is
    used as a fallback when color for the file type is not defined
    """

    # Return the filename enclosed in the color escape sequence
    # The "\033[0m" sequence at the end resets the color back to the default
    return f"{get_file_color(Path(filename)) if not color else color}{filename}\033[0m"


def generate_rainbow_colors(
    resolution: int, *, lightness: float = 0.8, saturation: float = 1.0
) -> List[str]:
    """
    Generates a list of colors that can be used to colorize text in a rainbow pattern

    The colors are returned as a list of strings in the format "r;g;b", where r, g and b
    are integers in the range [0, 255]

    The resolution parameter determines the number of colors in the rainbow
    """
    colors = []
    for i in range(resolution):
        hue = i / resolution
        lightness = 0.8
        saturation = 1.0
        r, g, b = colorsys.hls_to_rgb(hue, lightness, saturation)
        hex_color = f"{int(r * 255)};{int(g * 255)};{int(b * 255)}"
        colors.append(hex_color)
    return colors


RAINBOW_COLORS = generate_rainbow_colors(DEFAULT_RAINBOW_RESOLUTION)
""" A list of colors that can be used to colorize text in a rainbow pattern """


def rainbowize(string: str) -> str:
    """
    Returns the string with each character enclosed in a color escape sequence

    The colors are taken from the RAINBOW_COLORS list

    This function is impure, as it uses the global RAINBOW_INDEX variable to keep
    track of the current color index when iterating over the strings
    """
    global RAINBOW_INDEX
    result = []
    for char in string:
        result.append(
            f"\033[38;2;{RAINBOW_COLORS[RAINBOW_INDEX % len(RAINBOW_COLORS)]}m{char}\033[0m"
        )
        RAINBOW_INDEX += 1
    return "".join(result)
