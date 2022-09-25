import io
from django.http import FileResponse
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

pdfmetrics.registerFont(TTFont('Verdana', 'Verdana.ttf'))


def make_file(data):
    buffer = io.BytesIO()
    file = canvas.Canvas(buffer)
    file.setFont('Verdana', 8)
    file.drawString(
        30,
        800,
        'Список покупок:'
    )
    pos_x, pos_y, count = 50, 795, 1
    for i, (key, value) in enumerate(data.items(), start=1):
        if count == 56:
            file.showPage()
        pos_y -= 15
        file.drawString(
            pos_x, pos_y,
            f'{i}. {key.name} : {value} {key.measurement_unit}'.encode()
        )
        count += 1
    file.showPage()
    file.save()
    buffer.seek(0)
    return FileResponse(
        buffer,
        as_attachment=True,
        filename='purchases.pdf')
