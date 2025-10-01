class CharacterContext:
    def __init__(self, username):
        self.username = username

    def to_dict(self):
        return {"username": self.username}

    @classmethod
    def from_dict(cls, data: dict):
        return cls(username=data["username"])
