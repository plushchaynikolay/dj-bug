from django.test import TestCase
from parameterized import parameterized
from django.forms.models import model_to_dict
from ..models import MyModel, MyModelWithConstraint


class TestModel(TestCase):
    def setUp(self):
        MyModel.objects.create(
            constraint_field1='test_0',
            constraint_field2='existed',
            field3='some body',
        )

    def test_update_or_create_creates_two(self):
        orm_model = MyModel(
            constraint_field1='test_0',
            constraint_field2='existed',
            field3='once told me',
        )
        print(model_to_dict(orm_model))
        print()
        self.assertEqual(MyModel.objects.count(), 1)
        obj, created = MyModel.objects.update_or_create(
            constraint_field1=orm_model.constraint_field1,
            constraint_field2=orm_model.constraint_field2,
            defaults={**model_to_dict(orm_model)}
        )
        print(model_to_dict(obj))
        print()
        self.assertFalse(created)
        objs = MyModel.objects.all()
        for obj in objs:
            print(model_to_dict(obj))
            print()
        # BUG: AssertionError: 2 != 1 : 2
        self.assertEqual(MyModel.objects.count(), 1)


class TestModelWithConstraint(TestCase):
    def setUp(self):
        MyModelWithConstraint.objects.create(
            constraint_field1='test_0',
            constraint_field2='existed',
            field3='some body',
        )

    def test_update_or_create_works(self):
        orm_model = MyModelWithConstraint(
            constraint_field1='test_0',
            constraint_field2='existed',
            field3='once told me',
        )
        print(model_to_dict(orm_model, exclude=['id', 'constraint_field1', 'constraint_field2']))
        print()
        obj, created = MyModelWithConstraint.objects.update_or_create(
            constraint_field1=orm_model.constraint_field1,
            constraint_field2=orm_model.constraint_field2,
            defaults={
                **model_to_dict(orm_model,
                exclude=['id', 'constraint_field1', 'constraint_field2'])
            }
        )
        self.assertFalse(created)
        self.assertTrue(MyModelWithConstraint.objects.filter(
                constraint_field1=orm_model.constraint_field1,
                constraint_field2=orm_model.constraint_field2,
                field3=orm_model.field3,
        ).exists())
        self.assertEqual(MyModelWithConstraint.objects.count(), 1)


    def test_update_or_create_fails(self):
        orm_model = MyModelWithConstraint(
            constraint_field1='test_0',
            constraint_field2='existed',
            field3='once told me',
        )
        print(model_to_dict(orm_model))
        print()
        # BUG: django.db.utils.IntegrityError: UNIQUE constraint failed: bokunopico.constraint_field1, bokunopico.constraint_field2
        obj, created = MyModelWithConstraint.objects.update_or_create(
            constraint_field1=orm_model.constraint_field1,
            constraint_field2=orm_model.constraint_field2,
            defaults={
                **model_to_dict(orm_model)
            }
        )
        self.assertFalse(created)
        self.assertTrue(MyModelWithConstraint.objects.filter(
                constraint_field1=orm_model.constraint_field1,
                constraint_field2=orm_model.constraint_field2,
                field3=orm_model.field3,
        ).exists())
        self.assertEqual(MyModelWithConstraint.objects.count(), 1)
