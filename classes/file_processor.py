from classes.file_handler import FileHandler
from classes.stats_utils_mixin import StatsUtilsMixin


class FileProcessor(FileHandler, StatsUtilsMixin):
    def __init__(self, *args, **kwargs):
        FileHandler.__init__(self, *args, **kwargs)
