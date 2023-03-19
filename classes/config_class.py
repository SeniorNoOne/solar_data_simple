from os.path import sep


class GraphConfig:
    def __init__(self, file_extension=".txt", **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.file_extension = file_extension
        self.path = self.name if self.name.endswith(sep) else self.name + sep
        self.output_filename = self.path + self.name + self.file_extension
