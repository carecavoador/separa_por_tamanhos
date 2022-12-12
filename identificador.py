"""identificar.py"""
from io import BytesIO
from pathlib import Path

from PyPDF2 import PageObject, PdfReader, PdfWriter, Transformation
from reportlab.pdfgen import canvas


FONTE = "Helvetica"
TAMANHO_FONTE = 4
BORDA = 2


def atualiza_boxes(
    _pagina: PageObject, novo_retangulo: tuple[float, float, float, float]
) -> PageObject:
    """Atualiza todos os boxes de uma página com o retângulo informado."""
    _pagina.update({"/MediaBox": novo_retangulo})
    _pagina.update({"/TrimBox": novo_retangulo})
    _pagina.update({"/TrimBox": novo_retangulo})
    _pagina.update({"/ArtBox": novo_retangulo})
    _pagina.update({"/BleedBox": novo_retangulo})
    _pagina.update({"/CropBox": novo_retangulo})
    return _pagina


def identificar_layout_externo(arquivo_pdf: Path, identificador: str) -> PageObject:
    """Insere a identificação fornecida na área externa da página."""
    pdf = PdfReader(arquivo_pdf)
    pagina = pdf.pages[0]

    largura, altura = pagina.mediabox.upper_right
    largura, altura = float(largura), float(altura)

    bytes_pdf = BytesIO()
    documento = canvas.Canvas(
        bytes_pdf, pagesize=(largura, altura + TAMANHO_FONTE + BORDA)
    )
    texto = documento.beginText()
    texto.setTextOrigin(0, altura + BORDA)
    texto.setFont(FONTE, TAMANHO_FONTE)
    texto.textLine(identificador)
    documento.drawText(texto)
    documento.save()
    bytes_pdf.seek(0)

    novo_pdf = PdfReader(bytes_pdf)
    novo_pdf.pages[0].merge_page(pagina)
    return novo_pdf.pages[0]


def identificar_layout_interno(
    arquivo_pdf: Path, identificador: str, tamanho_pagina: tuple
) -> None:
    """Insere a identificação fornecida no canto superior esquerdo dentro do
    tamanho de página especificado."""
    pdf = PdfReader(arquivo_pdf)
    pagina = pdf.pages[0]

    largura_pagina, altura_pagina = tamanho_pagina

    largura, altura = pagina.mediabox.upper_right
    largura, altura = float(largura), float(altura)

    bytes_pdf = BytesIO()
    documento = canvas.Canvas(bytes_pdf, pagesize=(largura_pagina, altura_pagina))
    texto = documento.beginText()
    texto.setTextOrigin(14, altura_pagina - TAMANHO_FONTE - 14)
    texto.setFont(FONTE, TAMANHO_FONTE)
    texto.textLine(identificador)
    documento.drawText(texto)
    documento.save()
    bytes_pdf.seek(0)

    # Centraliza a página original na página com a identificação.
    novo_pdf = PdfReader(bytes_pdf)
    pos_x = (largura_pagina - largura) / 2
    pos_y = (altura_pagina - altura) / 2
    pagina.add_transformation(Transformation().translate(tx=pos_x, ty=pos_y))
    pagina = atualiza_boxes(pagina, (pos_x, pos_y, pos_x + largura, pos_y + altura))

    # novo_pdf.pages[0].merge_page(pagina)
    pg_id = novo_pdf.pages[0]
    pagina.merge_page(pg_id, expand=True)

    writer = PdfWriter()
    # writer.add_page(novo_pdf.pages[0])
    writer.add_page(pagina)
    with open(arquivo_pdf, "wb") as f:
        writer.write(f)
