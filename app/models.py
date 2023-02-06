import uuid
from django.db import models


class URL(models.Model):
    uid = models.UUIDField(
        primary_key=True, default=uuid.uuid4(), editable=True, max_length=36
    )
    link = models.CharField(max_length=1000)
    new = models.CharField(max_length=6)
