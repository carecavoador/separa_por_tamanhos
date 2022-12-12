import sys
import pathlib

from separador import separa_por_tamanho
from separador.papel import FOLHA_A4, FOLHA_A3, ROLO


TAMANHOS_PAPEL = [FOLHA_A4, FOLHA_A3, ROLO]
DESKTOP = pathlib.Path.home() / "Desktop"


def main() -> None:
    """Executa o programa."""
    arquivos = sys.argv[1:]
    arquivos = [
        pathlib.Path(pdf)
        for pdf in arquivos
        if pathlib.Path(pdf).suffix.lower() == ".pdf"
    ]

    if not arquivos:
        input("Nenhum arquivo separado. Pressione 'Enter' para sair: ")
        exit()

    for arquivo in arquivos:
        separa_por_tamanho(arquivo, TAMANHOS_PAPEL, DESKTOP)


if __name__ == "__main__":
    main()
