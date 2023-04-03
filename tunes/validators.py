from pathlib import Path
from django.core.exceptions import ValidationError
#import magic
import magic

def validate_file_extension(value):
    import os
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.pdf',]
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')


def validate_file_extension(data):
    import os
    import magic
    from django.core.exceptions import ValidationError

    mime = magic.Magic(mime=True)
    file_type = mime.from_buffer(data.read())

    extension = os.path.splitext(data.name)[1].lower()
    #content_type = magic.from_buffer(data.read(1024), mime=True)

    if extension != '.pdf':
        raise ValidationError('Unsupported file extension.')
    if file_type != 'application/pdf':
        raise ValidationError('DONT TRY TO FOOL ME.')
