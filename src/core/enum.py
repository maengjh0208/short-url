from enum import Enum


class Environment(str, Enum):
    PROD = "prod"
    LOCAL = "local"
