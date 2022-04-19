# t.me/ziby_notes_bot
import logging
from peewee import *
from telegram.ext import Updater, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup

# logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)
TOKEN = '5387683486:AAEHQB94zVgmg3JcYPQFmgHR_ZcmCy47SOU'

# keyboards
# main
main_reply_keyboard = [['/notes', '/reminds'],
                       ['/help', '/stop']]
main_markup = ReplyKeyboardMarkup(main_reply_keyboard, one_time_keyboard=True)
# reminds
reminds_reply_keyboard = [['/create_remind', '/view_reminds'],
                          ['/delete_remind', '/come_back']]
reminds_markup = ReplyKeyboardMarkup(reminds_reply_keyboard, one_time_keyboard=True)


# functions and commands
def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(CommandHandler('stop', stop))
    dp.add_handler(CommandHandler('notes', notes))
    dp.add_handler(CommandHandler('reminds', reminds))
    dp.add_handler(CommandHandler('create_note', create_note))
    dp.add_handler(CommandHandler('delete_note', delete_note))
    dp.add_handler(CommandHandler('create_remind', create_remind))
    dp.add_handler(CommandHandler('view_reminds', view_reminds))
    dp.add_handler(CommandHandler('delete_remind', delete_remind))
    dp.add_handler(CommandHandler('come_back', come_back))
    updater.start_polling()

    updater.idle()


def start(update, context):
    update.message.reply_text(
        'Здравствуйте! Я — бот Ziby notes, в котором вы можете создавать заметки, отправлять себе сообщения в будущее',
        reply_markup=main_markup
    )
    user_inf = (
        update.message.from_user.id,
        update.message.from_user.first_name if update.message.from_user.first_name else '0',
        update.message.from_user.username if update.message.from_user.username else '0')
    add_user(user_inf[0], user_inf[1], user_inf[2])


def stop(update, context):
    update.message.reply_text('Значит на этом всё, надеюсь был полезен. Ваши заметки и напоминалки будут удалены.')
    return ConversationHandler.END


def help(update, context):
    update.message.reply_text(
        'У меня есть следующие функции:'
    )


def notes(update, context):
    update.message.reply_text('''Здесь вы можете посмотреть все ваши существующие заметки, добавить новую или удалить \
старую заметку.

Команда /create_note {ваша заметка} — создаёт новую заметку.

Команда /delete_note {цифра/цифры, записанные через пробел} — позволяет удалить заметку/заметки.''')

    user_id = update.message.from_user.id
    user_notes = view_notes(user_id)
    list_of_notes = []
    if len(user_notes):
        for note_number in range(len(user_notes)):
            list_of_notes.append(f'{user_notes[note_number][0]}. {user_notes[note_number][1]}')
        list_of_notes = '\n'.join(list_of_notes)

        update.message.reply_text(f'''Вот все ваши заметки:\n{list_of_notes}''')

    else:
        update.message.reply_text('У вас пока нет заметок.')


def create_note(update, context):
    new_note = update.message.text[13:]
    user_id = update.message.from_user.id
    user_notes_len = len(view_notes(user_id))
    add_note(user_id, user_notes_len + 1, new_note)

    user_notes = view_notes(user_id)
    list_of_notes = []
    for note_number in range(len(user_notes)):
        list_of_notes.append(f'{user_notes[note_number][0]}. {user_notes[note_number][1]}')
    list_of_notes = '\n'.join(list_of_notes)

    update.message.reply_text(f'''Теперь ваши заметки выглядят так:\n{list_of_notes}''')


def delete_note(update, context):
    try:
        notes_for_delete_message = update.message.text[13:]
        notes_for_delete = [int(x) for x in notes_for_delete_message.split()]
        user_id = update.message.from_user.id
        remove_note(user_id, notes_for_delete)

        user_notes = view_notes(user_id)
        list_of_notes = []
        for note_number in range(len(user_notes)):
            list_of_notes.append(f'{user_notes[note_number][0]}. {user_notes[note_number][1]}')
        list_of_notes = '\n'.join(list_of_notes)

        update.message.reply_text(f'''Теперь ваши заметки выглядят так:\n{list_of_notes}''')

    except ValueError:
        update.message.reply_text('Пожалуйста, отправьте цифру/цифры, записанные через пробел, если хотите \
удалить сообщение')


def reminds(update, context):
    update.message.reply_text(
        'Эта функция используется вами, чтобы отправить себе сообщение в будущее. Вы можете создать новую\
"напоминалку", посмотреть их все (после срабатывания они удаляются автоматически) и удалить созданные,\
если вам они больше не нужны',
        reply_markup=reminds_markup)


def create_remind(update, context):
    update.message.reply_text('Напишите новую напоминалку')


def view_reminds(update, context):
    update.message.reply_text('Вот ваши напоминалки')


def delete_remind(update, context):
    update.message.reply_text('Укажите номер напоминалки, которую хотите удалить')


def come_back(update, context):
    update.message.reply_text('Возвращаю', reply_markup=main_markup)


# ORM models
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


def view_notes(user_id):
    user_notes_count = Notes.select(Notes.user_id == user_id).count()
    all_notes = []
    for note_number in range(1, user_notes_count + 1):
        note = Notes.get(Notes.user_id == user_id, Notes.user_note_id == note_number)
        all_notes.append((note.user_note_id, note.note))
    return all_notes


def remove_note(user_id, *note_ids):
    ids = sorted(note_ids[0])
    ids.reverse()
    user_notes_count = Notes.select(Notes.user_id == user_id).count()
    if max(ids) <= user_notes_count:
        all_notes = []
        for note_number in range(1, user_notes_count + 1):
            note = Notes.get(Notes.user_id == user_id, Notes.user_note_id == note_number)
            all_notes.append(note.note)
        for i in ids:
            note = Notes.get(Notes.user_id == user_id, Notes.user_note_id == i)
            note.delete_instance()
            all_notes.pop(i - 1)
        user_notes_count = Notes.select(Notes.user_id == user_id).count()
        for i in range(user_notes_count):
            note = Notes.get(Notes.user_id == user_id, Notes.note == all_notes[i])
            note.user_note_id = i + 1
            note.save()


# start program
if __name__ == '__main__':
    main()
