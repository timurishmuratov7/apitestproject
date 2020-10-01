from django.core.exceptions import ValidationError

def file_size_validator(value): # add this to some file where you can import it from
    limit = 5242880
    if value.size > limit:
        raise ValidationError('File is too large. Size should not exceed 5 MiB.')
