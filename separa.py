import sys
import shutil

from pathlib import Path
from dataclasses import dataclass

from PyPDF2 import PdfReader

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

TAMANHOS_PAPEL = [
    FOLHA_A4,
    FOLHA_A3,
    ROLO
]

DESKTOP = Path.home().joinpath("Desktop")


def separa_por_tamanho(lista_prints: list[Path], tamanhos: list[Papel], saida: Path) -> None:
    """Recebe uma lista de objetos Path apontando para arquivos PDF e retorna uma
    lista de objetos Tuple com os arquivos separados por tamanho."""

    for printout in lista_prints:
        print(f"Processando {printout.name}...")
        with open(printout, "rb") as arquivo:
            reader = PdfReader(arquivo)
            pagina = reader.pages[0]
            largura = pagina.mediabox.width
            altura = pagina.mediabox.height
            for tamanho in tamanhos:
                pasta_tamanho = saida.joinpath(tamanho.nome)
                pasta_tamanho.mkdir(exist_ok=True)
                if (largura <= tamanho.largura and altura <= tamanho.altura) or (
                    largura <= tamanho.altura and altura <= tamanho.largura
                ):
                    shutil.copy(printout, pasta_tamanho)
                    break



def main() -> None:
    """Executa o programa."""
    arquivos = sys.argv[1:]
    arquivos = [Path(pdf) for pdf in arquivos if Path(pdf).suffix.lower() == ".pdf"]

    if not arquivos:
        input("Nenhum arquivo separado. Pressione 'Enter' para sair: ")
        exit()

    separa_por_tamanho(arquivos, TAMANHOS_PAPEL, DESKTOP)


if __name__ == "__main__":
    main()
