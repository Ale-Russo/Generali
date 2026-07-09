from dataclasses import dataclass, field


@dataclass
class Oggetto:
    id: int
    nome: str

    Tracks: list = field(default_factory=list)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return self.nome