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


class Reminds(BaseModel):
    user_id = IntegerField()
    remind = TextField()
    datetime = DateTimeField()

    class Meta:
        db_table = 'reminds'


# user
def add_user(user_id, first_name, username):
    row = Users(user_id=user_id, first_name=first_name, username=username)
    row.save()


# notes
def add_note(user_id, user_note_id, note):
    row = Notes(user_id=user_id, user_note_id=user_note_id, note=note)
    row.save()


def view_note(user_id):
    user_notes_count = Notes.select(Notes.user_id == user_id).count()
    all_notes = []
    for note_number in range(1, user_notes_count + 1):
        note = Notes.get(Notes.user_id == user_id, Notes.user_note_id == note_number)
        all_notes.append((note.user_note_id, note.note))
    return all_notes


def delete_note(user_id, note_ids):
    note_ids.sort().reverse()
    user_notes = Notes.get(Notes.user_id == user_id)
    for note_num in note_ids:
        user_notes.remove(note_num)
    save_user_notes = user_notes[:]
    user_notes.delete_instance()
    # for save_notes in save_user_notes:


if __name__ == '__main__':
    try:
        db.connect()
        Users.create_table()
        Notes.create_table()
        Reminds.create_table()
    except InternalError as px:
        print(str(px))
