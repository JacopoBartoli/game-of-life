import numpy as np

from PyQt5.QtGui import QImage

import utils.colors as colors


def np_to_qimage(np_array: np.ndarray, show_age: bool) -> QImage:
    """
    Function to convert a np.ndarray in a QImage
    :param np_array: np array that will be converted
    :param show_age: flag to enable the colouring of the cells.
    :return: the QImage obtained from the conversion.
    """

    assert len(np_array.shape) == 2 and np_array.dtype == np.uint8

    width = np_array.shape[1]
    height = np_array.shape[0]
    bytes_per_line = width
    image = QImage(np_array, width, height, bytes_per_line, QImage.Format_Indexed8)

    # Maps array values to color
    if show_age:
        image.setColorTable(colors.COLOR_TABLE)
    else:
        image.setColorTable(colors.BW_COLOR_TABLE)

    return image
