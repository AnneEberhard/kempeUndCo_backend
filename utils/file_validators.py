from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile

MAX_PDF_SIZE = 10 * 1024 * 1024


def validate_pdf(file):
    print('validator')
    if not isinstance(file, UploadedFile):
        raise ValidationError(
            "Ungültiger PDF-Upload."
        )
    if file.size > MAX_PDF_SIZE:
        raise ValidationError(
            "Die PDF-Datei darf maximal 10 MB groß sein."
        )

    header = file.read(5)
    file.seek(0)

    if header != b"%PDF-":
        raise ValidationError(
            "Die hochgeladene Datei ist keine gültige PDF-Datei."
        )