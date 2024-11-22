import json
import os


class Config(dict):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance.load_config()
        return cls._instance

    def load_config(self, config_file: str = "config/config.json") -> None:
        if os.path.exists(config_file):
            try:
                with open(config_file, "r") as f:
                    config_data = json.load(f)
                    self.update(config_data)
            except json.JSONDecodeError:
                print("Error decoding the config file. Please check the format.")
        else:
            print(f"Config file '{config_file}' not found. Using default configuration.")
