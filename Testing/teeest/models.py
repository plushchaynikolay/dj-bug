from django.db import models

class MyModel(models.Model):
    class Meta:
        db_table = 'arigato'

    id = models.AutoField(primary_key=True)
    source = models.CharField(max_length=50, null=False)
    source_message_id = models.CharField(max_length=50, null=True)
    text = models.TextField(null=True)

    objects = models.Manager()


class MyModelWithConstraint(models.Model):
    class Meta:
        db_table = 'bokunopico'
        constraints = [
            models.UniqueConstraint(fields=['source', 'source_message_id'],
                                    name='messages_source_source_message_id_key')
        ]

    id = models.AutoField(primary_key=True)
    source = models.CharField(max_length=50, null=False)
    source_message_id = models.CharField(max_length=50, null=True)
    text = models.TextField(null=True)

    objects = models.Manager()
