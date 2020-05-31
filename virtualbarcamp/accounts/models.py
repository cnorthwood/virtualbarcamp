from django.contrib.auth.models import User
from django.db.models import Model, OneToOneField, CASCADE, DateTimeField


class Account(Model):
    user = OneToOneField(User, on_delete=CASCADE)
    has_accepted_code_of_conduct = DateTimeField()
