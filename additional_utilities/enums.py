from enum import Enum


class ChoiceEnum(Enum):
    @classmethod
    def choices(cls):
        return tuple((item.value, item.name) for item in cls)


class LogTypes(ChoiceEnum):
    LOCATION_START = 1
    LOCATION_CHANGE = 2
    LOCATION_FINISH = 3
    LOCATION_CANCELED = 4


class CargoStatuses(ChoiceEnum):
    created = 1
    in_progress = 2
    done = 3
    canceled = 4
