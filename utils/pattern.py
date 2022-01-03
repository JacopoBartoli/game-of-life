from pathlib import Path
import numpy as np
from utils.config import config


def get_pattern() -> list:
    """
    Get all the .cells file stored in the path described by the configuration file.
    :return: List of file name.
    """
    folder_path = config.DIR_PATTERN.glob('**/*')
    lst = [str(f).replace(".cells", '').replace(str(config.DIR_PATTERN) + '/', "") for f in folder_path if f.is_file()
           and f.suffix == ".cells"]
    return lst


def read_pattern(file_path: str) -> np.ndarray:
    """
    Read pattern from a .cells file in plain text format.
    :param file_path: The file that contains the pattern.
    :return: The numpy array that represents the requested pattern.
    """
    file_path = Path(file_path)
    # Check if the example file exist.
    if not Path.is_file(file_path):
        return None

    rows = 0
    cols = 0
    with open(file_path) as f:
        for i, line in enumerate(f):
            if line[0] != "!":
                rows += 1
                if len(line) > cols:
                    # Exclude the end of line char from the column count.
                    cols = len(line) - 1

    grid = np.zeros((rows, cols), dtype=np.uint8)

    skip_rows = 0
    with open(file_path) as f:
        for i, line in enumerate(f):
            for k, c in enumerate(line):
                if c == "!" and k == 0:
                    skip_rows += 1
                    break
                elif c == "O":
                    grid[i - skip_rows, k] = 1

    return grid


def save_pattern(file_path: str, grid_pattern: np.ndarray):
    """
    Write a pattern into a .cells file in plain text format.
    :param file_path: The file into which save the pattern.
    :param grid_pattern: Numpy array representing the grid state of the pattern.
    """

    # Transform the grid into a list of string lines.
    lines = []
    for row in range(len(grid_pattern)):
        line = ["." if cell == 0 else "O" for cell in grid_pattern[row]]
        line_str = "".join(line) + "\n"
        lines.append(line_str)

    with open(file_path, "w") as f:
        f.writelines(lines)


