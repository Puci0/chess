import json
import os
import sys


class Config(dict):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance.__load_config()
        return cls._instance

    def __load_config(self, config_file: str = "config/config.json") -> None:
        config_file = self.__resource_path(config_file)

        if os.path.exists(config_file):
            try:
                with open(config_file, "r") as f:
                    config_data = json.load(f)
                    self.update(config_data)
            except json.JSONDecodeError:
                print("Error decoding the config file. Please check the format.")
        else:
            print(f"Config file '{config_file}' not found. Using default configuration.")

    def __resource_path(self, relative_path) -> os.path:
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)