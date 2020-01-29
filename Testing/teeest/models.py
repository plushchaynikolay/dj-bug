from django.db import models

class MyModel(models.Model):
    class Meta:
        db_table = 'arigato'

    id = models.AutoField(primary_key=True)
    constraint_field1 = models.CharField(max_length=50, null=False)
    constraint_field2 = models.CharField(max_length=50, null=True)
    field3 = models.TextField(null=True)

    objects = models.Manager()


class MyModelWithConstraint(models.Model):
    class Meta:
        db_table = 'bokunopico'
        constraints = [
            models.UniqueConstraint(fields=['constraint_field1', 'constraint_field2'],
                                    name='constraint_fields')
        ]

    id = models.AutoField(primary_key=True)
    constraint_field1 = models.CharField(max_length=50, null=False)
    constraint_field2 = models.CharField(max_length=50, null=True)
    field3 = models.TextField(null=True)

    objects = models.Manager()
