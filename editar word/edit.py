from docx import Document

# 1. Abre el archivo existente
doc = Document('plantilla_boleta.docx')

# 2. Realiza las modificaciones que desees
for paragraph in doc.paragraphs:
    # Ejemplo: Modificar el contenido del primer párrafo
    if "#control" in paragraph.text:
        paragraph.text = paragraph.text.replace("#control", "21301061550024")

# 3. Guarda el documento modificado
doc.save('documento_modificado.docx')