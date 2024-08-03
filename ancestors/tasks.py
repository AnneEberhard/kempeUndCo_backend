import os


def rename_image(instance, filename, field_index):
    ext = filename.split('.')[-1]
    new_filename = f"{instance.id}_image{field_index}.{ext}"
    return os.path.join('images/', new_filename)
