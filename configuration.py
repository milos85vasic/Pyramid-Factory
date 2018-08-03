from Toolkit.configuration import *

configuration_repository = "https://github.com/milos85vasic/Pyramid-Factory-Config-Default.git"

pyramid_configuration = "pyramid_factory.ini"
pyramid_configuration_dir = "Pyramid_Configuration"
pyramid_configuration_matrix = "pyramid_factory.ini.matrix"

pyramid_configuration_matrix_egg = "PYRAMID_FACTORY_EGG"

venv_dir_name = "Venv"


def venv_dir_path(home_path):
    return home_path + "/" + venv_dir_name