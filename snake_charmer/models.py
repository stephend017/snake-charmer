import enum


class VersionType(enum.Enum):
    NONE = -1
    MAJOR = 0
    MINOR = 1
    REVISION = 2

    @staticmethod
    def from_label(label_name: str):
        """
        """
        if label_name == "major-release":
            return VersionType.MAJOR
        if label_name == "minor-release":
            return VersionType.MINOR
        if label_name == "revision-release":
            return VersionType.REVISION
        return VersionType.NONE
