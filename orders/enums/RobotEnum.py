from enum import Enum


class Model(Enum):
    Model_R2 = "R2"
    Model_13 = "13"
    Model_X5 = "X5"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class Version(Enum):
    Version_R2 = "D2"
    Version_13 = "XS"
    Version_X5 = "LT"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]