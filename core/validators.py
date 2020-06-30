from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def value_validator(value):
    if value <= 0:
        raise ValidationError(
            _('This value must be greater than 0.'),
            params={'value': value},
        )

def tax_validator(value):
    if value < 0:
        raise ValidationError(
            _('This value must be greater or equal to 0.'),
            params={'value': value},
        )