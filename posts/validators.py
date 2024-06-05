# validators.py

import os
from django.core.exceptions import ValidationError

def validate_image_extension(value):
    ext = os.path.splitext(value.name)[1].lower()
    if ext == '.png':
        raise ValidationError('PNG 파일 말고 다른 확장자 파일을 넣어주세요.')
