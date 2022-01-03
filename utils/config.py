import yaml
from pathlib import Path


class Config:
    """Class that allows the management of the .yml configuration file.
    """

    def __init__(self):

        self._root_path = Path(__file__).parent.parent.resolve()
        self.PATH_CONFIG = self._root_path.joinpath('config.yml')

        with open(self.PATH_CONFIG, 'r') as file:
            cfg = yaml.safe_load(file)

        _game_cfg = cfg['game_config']
        _pattern_cfg = cfg['pattern_config']
        _paths_cfg = cfg['filepaths']

        self.GRID_SIZE = eval(_game_cfg['grid_size'])

        self.SPEED = int(_game_cfg['speed'])

        self.BASE_PATTERN = _pattern_cfg['base']

        self.DIR_PATTERN = self._root_path.joinpath(_paths_cfg['resources']['path'])

        _pattern_paths_cfg = _paths_cfg['resources']['patterns']

        self.DIR_PATTERN = self.DIR_PATTERN.joinpath(_pattern_paths_cfg['path'])


config = Config()








