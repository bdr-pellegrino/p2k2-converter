from dataclasses import dataclass
from p2k2_converter.core import Profile
from p2k2_converter.core import Optional


@dataclass
class Model:
    name: str
    width: float
    height: float
    verse: str | None
    profiles: dict[str, Profile]
    optionals: dict[str, Optional]

    def add_profile(self, profile: Profile) -> None:
        self.profiles[profile.code] = profile

    def remove_profile(self, profile: Profile) -> None:
        del self.profiles[profile.code]

    def get_profiles(self) -> list[Profile]:
        return list(self.profiles.values())

    def add_optional(self, optional: Optional) -> None:
        self.optionals[optional.name] = optional

    def remove_optional(self, optional: Optional) -> None:
        del self.optionals[optional.name]

    def get_optionals(self) -> list[Optional]:
        return list(self.optionals.values())



