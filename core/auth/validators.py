import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class NumberValidator:
    def __init__(self, min_digits=0):
        self.min_digits = min_digits

    def validate(self, password, user=None):
        if not len(re.findall("\d", password)) >= self.min_digits:
            raise ValidationError(
                _(
                    f"This password must contain at least {self.min_digits} digit(s), 0-9."  # noqa: E501
                ),
                code="password_no_number",
            )

    def get_help_text(self):
        return _(
            f"Your password must contain at least {self.min_digits} digit(s), 0-9."
        )
