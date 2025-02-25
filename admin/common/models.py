from django.db import models
from common.kgs import generate_unique_id
from django.utils import timezone
# Create your models here.

class AuditableModel(models.Model):
    id = models.CharField(max_length=50, primary_key=True, default=generate_unique_id, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True