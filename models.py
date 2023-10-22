from django.db import models

class StudyMaterial(models.Model):
    title = models.CharField(max_length=255)
    upload_date = models.DateTimeField(auto_now_add=True)
    original_text = models.TextField()
    summary = models.TextField()
