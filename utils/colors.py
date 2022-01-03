"""
Define the color tables.
"""
from PyQt5.QtGui import qRgb

ALIVE_COLOR = qRgb(255, 255, 255)
DEAD_COLOR = qRgb(0, 0, 0)

COLOR_TABLE = [DEAD_COLOR] + [qRgb(0, 255, 255 - i * 2) for i in range(128)] + \
              [qRgb(i*2, 255-i*2, 0) for i in range(127)]
# Alive cell: white - Dead cell: black
BW_COLOR_TABLE = [DEAD_COLOR] + [ALIVE_COLOR for i in range(256)]
