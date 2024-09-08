import os
import django

# Django-Setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kempeUndCo_backend.settings')
django.setup()

from PIL import Image
import io


def compress_image(image_path, quality=30):
    """Komprimiert ein Bild und überschreibt die Originaldatei."""
    with Image.open(image_path) as img:
        # Entfernen von Metadaten und Konvertieren in RGB
        img = img.convert('RGB')
        output = io.BytesIO()
        img.save(output, format='JPEG', quality=quality, optimize=True, subsampling=0)
        output.seek(0)

        # Schreibe die komprimierte Datei zurück auf die Festplatte
        with open(image_path, 'wb') as f:
            f.write(output.getvalue())


def compress_images_in_directory(directory, quality=30):
    """Komprimiert alle JPEG-Bilder in einem Verzeichnis und überschreibt die Originale."""
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg')):
                image_path = os.path.join(root, file)

                print(f"Komprimiere {image_path}...")
                compress_image(image_path, quality)
                print(f"Überschrieben: {image_path}")


def main():
    # Definiere die Verzeichnisse, die die Bilder enthalten
    directories = [
        'media/images',  # Hauptbilderverzeichnis
        'media/info',    # Info-Bilderverzeichnis
        'media/recipes'  # Rezepte-Bilderverzeichnis
    ]

    # Komprimiere Bilder in allen definierten Verzeichnissen
    for directory in directories:
        print(f"Verarbeite Verzeichnis: {directory}")
        compress_images_in_directory(directory)
        print(f"Fertig mit Verzeichnis: {directory}")


if __name__ == "__main__":
    main()
