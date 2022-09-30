import datetime
import os

from peewee import DateTimeField, IntegerField, Model, SqliteDatabase, TextField

from .filesystem import data_dir

db_filepath = os.path.join(data_dir, "dardanelles.db")
print("Using database at", db_filepath)
sql_database = SqliteDatabase(db_filepath)


class JSONField(TextField):
    def db_value(self, value):
        return super().db_value(
            json.dumps(
                value,
                ensure_ascii=False,
                indent=2,
            )
        )

    def python_value(self, value):
        return json.loads(value)


class File(Model):
    filepath = TextField()
    sha256 = TextField(unique=True)
    database = TextField()
    description = TextField()
    depends = JSONField(default=[])
    created = DateTimeField(default=datetime.datetime.now)
    accessed = DateTimeField(default=datetime.datetime.now)
    count = IntegerField(default=0)

    class Meta:
        database = sql_database


sql_database.create_tables([File], safe=True)
