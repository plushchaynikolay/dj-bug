```bash
% python manage.py test teeest.tests.test_model                                                                       ✹
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
{'id': None, 'constraint_field1': 'test_0', 'constraint_field2': 'existed', 'field3': 'once told me'}

{'id': 1, 'constraint_field1': 'test_0', 'constraint_field2': 'existed', 'field3': 'once told me'}

{'id': 1, 'constraint_field1': 'test_0', 'constraint_field2': 'existed', 'field3': 'once told me'}

.{'id': None, 'constraint_field1': 'test_0', 'constraint_field2': 'existed', 'field3': 'once told me'}

E{'field3': 'once told me'}

.
======================================================================
ERROR: test_update_or_create_fails (teeest.tests.test_model.TestModelWithConstraint)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/nikolay/.local/share/virtualenvs/dj-bug-As5S_Z9q/lib/python3.8/site-packages/django/db/backends/utils.py", line 86, in _execute
    return self.cursor.execute(sql, params)
  File "/home/nikolay/.local/share/virtualenvs/dj-bug-As5S_Z9q/lib/python3.8/site-packages/django/db/backends/sqlite3/base.py", line 396, in execute
    return Database.Cursor.execute(self, query, params)
sqlite3.IntegrityError: UNIQUE constraint failed: bokunopico.constraint_field1, bokunopico.constraint_field2

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/home/nikolay/NIT/dj-bug/Testing/teeest/tests/test_model.py", line 85, in test_update_or_create_fails
    obj, created = MyModelWithConstraint.objects.update_or_create(
  File "/home/nikolay/.local/share/virtualenvs/dj-bug-As5S_Z9q/lib/python3.8/site-packages/django/db/models/manager.py", line 82, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
  File "/home/nikolay/.local/share/virtualenvs/dj-bug-As5S_Z9q/lib/python3.8/site-packages/django/db/models/query.py", line 585, in update_or_create
    obj.save(using=self.db)
  File "/home/nikolay/.local/share/virtualenvs/dj-bug-As5S_Z9q/lib/python3.8/site-packages/django/db/models/base.py", line 745, in save
    self.save_base(using=using, force_insert=force_insert,
  File "/home/nikolay/.local/share/virtualenvs/dj-bug-As5S_Z9q/lib/python3.8/site-packages/django/db/models/base.py", line 782, in save_base
    updated = self._save_table(
  File "/home/nikolay/.local/share/virtualenvs/dj-bug-As5S_Z9q/lib/python3.8/site-packages/django/db/models/base.py", line 887, in _save_table
    results = self._do_insert(cls._base_manager, using, fields, returning_fields, raw)
  File "/home/nikolay/.local/share/virtualenvs/dj-bug-As5S_Z9q/lib/python3.8/site-packages/django/db/models/base.py", line 924, in _do_insert
    return manager._insert(
  File "/home/nikolay/.local/share/virtualenvs/dj-bug-As5S_Z9q/lib/python3.8/site-packages/django/db/models/manager.py", line 82, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
  File "/home/nikolay/.local/share/virtualenvs/dj-bug-As5S_Z9q/lib/python3.8/site-packages/django/db/models/query.py", line 1204, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
  File "/home/nikolay/.local/share/virtualenvs/dj-bug-As5S_Z9q/lib/python3.8/site-packages/django/db/models/sql/compiler.py", line 1384, in execute_sql
    cursor.execute(sql, params)
  File "/home/nikolay/.local/share/virtualenvs/dj-bug-As5S_Z9q/lib/python3.8/site-packages/django/db/backends/utils.py", line 68, in execute
    return self._execute_with_wrappers(sql, params, many=False, executor=self._execute)
  File "/home/nikolay/.local/share/virtualenvs/dj-bug-As5S_Z9q/lib/python3.8/site-packages/django/db/backends/utils.py", line 77, in _execute_with_wrappers
    return executor(sql, params, many, context)
  File "/home/nikolay/.local/share/virtualenvs/dj-bug-As5S_Z9q/lib/python3.8/site-packages/django/db/backends/utils.py", line 86, in _execute
    return self.cursor.execute(sql, params)
  File "/home/nikolay/.local/share/virtualenvs/dj-bug-As5S_Z9q/lib/python3.8/site-packages/django/db/utils.py", line 90, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/home/nikolay/.local/share/virtualenvs/dj-bug-As5S_Z9q/lib/python3.8/site-packages/django/db/backends/utils.py", line 86, in _execute
    return self.cursor.execute(sql, params)
  File "/home/nikolay/.local/share/virtualenvs/dj-bug-As5S_Z9q/lib/python3.8/site-packages/django/db/backends/sqlite3/base.py", line 396, in execute
    return Database.Cursor.execute(self, query, params)
django.db.utils.IntegrityError: UNIQUE constraint failed: bokunopico.constraint_field1, bokunopico.constraint_field2

----------------------------------------------------------------------
Ran 3 tests in 0.015s

FAILED (errors=1)
Destroying test database for alias 'default'...
```