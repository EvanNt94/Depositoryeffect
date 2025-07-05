from pdf2image import convert_from_path

# Pfad zur PDF-Datei
pdf_path = '/Users/a2/code/fin/trade/test_docs/Financial Report INTRALOT S.A. (2024,Six-Month Statement,Both).pdf'

# Konvertiere die PDF in Bilder (jede Seite als Bild)
images = convert_from_path(pdf_path, dpi=300)

# Speichere die Bilder als PNG
for i, image in enumerate(images):
    image.save(f'test/page_{i + 1}.png', 'PNG')
    