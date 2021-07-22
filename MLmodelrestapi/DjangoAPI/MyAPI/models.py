from django.db import models

# Create your models here.
class Task(models.Model):
    date_created = models.DateTimeField(auto_now=True)
    audio = models.FileField(upload_to='Audio/',default='Audio/None/No-audio.wav')

    def __str__(self):
        return "%s" % self.pk