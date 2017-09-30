from glob import glob
from os import path
from shutil import copy2

from utils.logger import Logger


class ConfigFilesManager(Logger):

    name = "ConfigManager"

    @classmethod
    def run(cls):

        # noinspection SpellCheckingInspection
        parameters_folder = "parameters"
        templates_folder = "templates"

        temp_files = [i.split("/")[-1] for i in glob("{}/*.json".format(templates_folder))]
        cls.log("The required configuration files are: '{}'.".format(temp_files))

        for i in temp_files:
            if not path.exists("{}/{}".format(parameters_folder, i)):
                cls.log("'{}' file is missing in parameters folder. I will create it.")
                copy2("{}/{}".format(templates_folder, i), parameters_folder)


if __name__ == "__main__":
    ConfigFilesManager.run()
