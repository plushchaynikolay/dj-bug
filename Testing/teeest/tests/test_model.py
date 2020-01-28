from django.test import TestCase
from parameterized import parameterized
from django.forms.models import model_to_dict
from ..models import MyModel, MyModelWithConstraint


class TestModel(TestCase):
    def setUp(self):
        MyModel.objects.create(
            source='test_0',
            source_message_id='existed',
            text='some body',
        )

    def test_update_or_create_creates_two(self):
        orm_model = MyModel(
            source='test_0',
            source_message_id='existed',
            text='once told me',
        )
        print(model_to_dict(orm_model))
        print()
        self.assertEqual(MyModel.objects.count(), 1)
        obj, created = MyModel.objects.update_or_create(
            source=orm_model.source,
            source_message_id=orm_model.source_message_id,
            defaults={
                **model_to_dict(orm_model,
                exclude=['id'])
            }
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
            source='test_0',
            source_message_id='existed',
            text='some body',
        )

    def test_update_or_create_works(self):
        orm_model = MyModelWithConstraint(
            source='test_0',
            source_message_id='existed',
            text='once told me',
        )
        print(model_to_dict(orm_model, exclude=['id', 'source', 'source_message_id']))
        print()
        obj, created = MyModelWithConstraint.objects.update_or_create(
            source=orm_model.source,
            source_message_id=orm_model.source_message_id,
            defaults={
                **model_to_dict(orm_model,
                exclude=['id', 'source', 'source_message_id'])
            }
        )
        self.assertFalse(created)
        self.assertTrue(MyModelWithConstraint.objects.filter(
                source=orm_model.source,
                source_message_id=orm_model.source_message_id,
                text=orm_model.text,
        ).exists())
        self.assertEqual(MyModelWithConstraint.objects.count(), 1)


    def test_update_or_create_fails(self):
        orm_model = MyModelWithConstraint(
            source='test_0',
            source_message_id='existed',
            text='once told me',
        )
        print(model_to_dict(orm_model))
        print()
        # BUG: django.db.utils.IntegrityError: UNIQUE constraint failed: bokunopico.source, bokunopico.source_message_id
        obj, created = MyModelWithConstraint.objects.update_or_create(
            source=orm_model.source,
            source_message_id=orm_model.source_message_id,
            defaults={
                **model_to_dict(orm_model)
            }
        )
        self.assertFalse(created)
        self.assertTrue(MyModelWithConstraint.objects.filter(
                source=orm_model.source,
                source_message_id=orm_model.source_message_id,
                text=orm_model.text,
        ).exists())
        self.assertEqual(MyModelWithConstraint.objects.count(), 1)
