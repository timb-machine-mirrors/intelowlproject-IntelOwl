from django.db import models
from django.utils.timezone import now

def file_directory_path(instance, filename):
    return f"job_{now().strftime('%Y_%m_%d_%H_%M_%S')}_{filename}"

class Analyzable(models.Model):
    name = models.CharField(max_length=512, blank=False, null=False, unique=True)
    md5 = models.CharField(unique=True)
    sha1 = models.CharField(unique=True)
    sha256 = models.CharField(unique=True)
    creation_time = models.DateTimeField(default=now, blank=False, null=False)

    class Meta:
        abstract = True
        indexes = [
            models.Index(
                fields=[
                    "name"
                ]
            ),
            models.Index(
                fields=[
                    "md5"
                ]
            ),
            models.Index(
                fields=[
                    "sha1"
                ]
            ),
            models.Index(
                fields=[
                    "sha256"
                ],

            )
        ]
    # todo md5 is calculated pre save
    # todo sha1 is calculated pre save
    # todo sha256 is calculated pre save

class Observable(Analyzable):
    classification = models.CharField(null=False, blank=False, choices=ObservableClassification.choices)

    class Meta:
        indexes = [
            models.Index(
                fields=[
                    "classification"
                ]
            )
        ]
    # todo classification is calculated pre save

class File(Analyzable):
    name = models.CharField(max_length=512, blank=False, null=False, unique=False)
    file = models.FileField(null=False, blank=False, upload_to=file_directory_path, unique=True)
    mimetype = models.CharField(null=False, blank=False)

    class Meta:
        indexes = [
            models.Index(
                fields=[
                    "mimetype"
                ]
            )
        ]

    def read(self):
        self.file.seek(0)
        return self.file.read()

@receiver(models.signals.pre_delete, sender=File)
def delete_file(sender, instance: File, **kwargs):
    if instance.file:
        instance.file.delete()