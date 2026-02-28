import random
from dj import DJ

class DJService:

    def __init__(self, djs: list[DJ]):
        self.djs = djs

    def get_random_dj(self) -> DJ:
        return random.choice(self.djs)

    def get_dj_by_name(self, name: str) -> DJ | None:
        for dj in self.djs:
            if dj.name == name:
                return dj
        return None