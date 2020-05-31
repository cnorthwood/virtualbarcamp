from django.core.exceptions import ValidationError
from django.forms import Form, BooleanField


class AcceptCodeOfConductForm(Form):
    accept = BooleanField()

    def clean_accept(self):
        if self.cleaned_data["accept"] is not True:
            raise ValidationError("You must accept the code of conduct to continue")
        return True
