# Djungo Bug

Unexpected behavior of django database `update_or_create` and `get_or_create`.

## Preambula

We wanted to use `update_or_create` with several models, that had different structure.

Model lookes like:

```python
class MyModelWithConstraint(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['constraint_field1', 'constraint_field2'],
                                    name='constraint_fields')
        ]

    id = models.AutoField(primary_key=True)
    constraint_field1 = models.CharField(max_length=50, null=False)
    constraint_field2 = models.CharField(max_length=50, null=False)
    text = models.TextField(null=True)
    ...
```

Our function lookes like:

```python
def use_update_or_create(modelclass, some_object):
    orm_object = modeltype.from_someobject(some_object)
    _, created = modelclass.update_or_create(
        constraint_field1=orm_model.constraint_field1,
        constraint_field2=orm_model.constraint_field2,
        defaults={**model_from_dict(orm_model)}
    )
    return created
```

## What happened?

We got unexpected `django.db.utils.IntegrityError: UNIQUE constraint failed:`, then did a research and made some experimens.

Here is an example of using `update_or_create` without database constraint:

```python
    ...
    self.assertEqual(MyModel.objects.count(), 1)
    obj, created = MyModel.objects.update_or_create(
        source=orm_model.source,
        source_message_id=orm_model.source_message_id,
        defaults={**model_to_dict(orm_model)}
    )
    self.assertFalse(created)
    self.assertEqual(MyModel.objects.count(), 1)
    # BUG: AssertionError: 2 != 1 : 2
```

So, `created=False` but `MyModel.objects.count() = 2`, and new object was actually created.

## Why it happened?

1. `django.forms.models.model_to_dict` returns a dictionary from ORM-object.
Actually, in our case, it returns:

```python
>>> model_to_dict(orm_object)
{'id': None, 'source': 'test_0', 'source_message_id': 'existed', 'text': 'once told me'}
```

2. Here is a source code of `update_or_create`:

```python
    def update_or_create(self, defaults=None, **kwargs):
        """
        Look up an object with the given kwargs, updating one with defaults
        if it exists, otherwise create a new one.
        Return a tuple (object, created), where created is a boolean
        specifying whether an object was created.
        """
        defaults = defaults or {}
        self._for_write = True
        with transaction.atomic(using=self.db):
            try:
                obj = self.select_for_update().get(**kwargs)
            except self.model.DoesNotExist:
                params = self._extract_model_params(defaults, **kwargs)
                # Lock the row so that a concurrent update is blocked until
                # after update_or_create() has performed its save.
                obj, created = self._create_object_from_params(kwargs, params, lock=True)
                if created:
                    return obj, created
            for k, v in resolve_callables(defaults):
                setattr(obj, k, v)
            obj.save(using=self.db)
        return obj, False
```

So, field `id` is overridden with `None`, and when it goes `obj.save()`, then `obj.id` autoincrements itself with new value.

## Suggestions

We understand that an issue took it's place because of our unknowing of how this functions work inside. But we souldn't know it!

The magic of autoincrements fields easily can deliver unexpected behavior and sould be carefully explained in documentation.
Or protected from the inside:
- check if field is auto incremented 
- and is it setted to a None-value, 
- and if it is, make a warning
That could be a satisfying solution.

Then it goes like this:
```python
```
