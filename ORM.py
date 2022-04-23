from peewee import *

db = SqliteDatabase('ziby_notes_database.db')


class BaseModel(Model):
    class Meta:
        database = db


# tables
class Users(BaseModel):
    user_id = IntegerField()
    first_name = TextField()
    username = TextField()

    class Meta:
        db_table = 'users'


class Notes(BaseModel):
    user_id = IntegerField()
    user_note_id = IntegerField()
    note = TextField()

    class Meta:
        db_table = 'notes'


class RemindsImages(BaseModel):
    user_id = IntegerField()
    image_name = TextField()

    class Meta:
        db_table = 'reminds_images'


class RemindsAudio(BaseModel):
    user_id = IntegerField()
    audio_name = TextField()

    class Meta:
        db_table = 'reminds_audio'


if __name__ == '__main__':
    try:
        db.connect()
        Users.create_table()
        Notes.create_table()
        RemindsImages.create_table()
        RemindsAudio.create_table()
    except InternalError as px:
        print(str(px))
