from dataclasses import dataclass


@dataclass
class Papel:
    """Classe para representar os tamanhos de papel."""

    nome: str
    largura: int
    altura: int


# Tamanhos de papel
FOLHA_A4 = Papel("A4", 595, 842)
FOLHA_A3 = Papel("A3", 842, 1191)
ROLO = Papel("ROLO", 2520, 91440)
