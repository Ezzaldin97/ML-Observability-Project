import os
import yaml

class Config:
    """
    Read Configuration file
    """
    def __init__(self) -> None:
        with open(os.path.join("conf", "config.yml"), "r") as f_config:
            self.config = yaml.safe_load(f_config)