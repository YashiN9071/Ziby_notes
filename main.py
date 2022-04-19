# t.me/ziby_notes_bot
import logging
import sqlite3
from telegram.ext import Updater, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup
from ORM import *

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
        'Давайте начнём!',
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

Для того, чтобы создать заметку воспользуйтесь командой /create_note (ваша заметка).

Для того, чтобы удалить заметку вам нужно использовать команду /delete_note и указать её \
порядковый номер. Если хотите удалить несколько, то запишите все цифры через пробел.''')

    user_id = update.message.from_user.id
    user_notes = view_note(user_id)
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
    user_notes_len = len(view_note(user_id))
    add_note(user_id, user_notes_len + 1, new_note)

    user_notes = view_note(user_id)
    list_of_notes = []
    for note_number in range(len(user_notes)):
        list_of_notes.append(f'{user_notes[note_number][0]}. {user_notes[note_number][1]}')
    list_of_notes = '\n'.join(list_of_notes)

    update.message.reply_text(f'''Теперь ваши заметки выглядят так:\n{list_of_notes}''')


def delete_note(update, context):
    number_of_notes_for_delete = update.message.text[13:]
    notes_for_delete = [int(x) for x in number_of_notes_for_delete.split()]
    user_id = update.message.from_user.id
    conn = sqlite3.connect("ziby_notes_database.db")
    cur = conn.cursor()
    user_notes = cur.execute('SELECT note_number_for_user, note FROM notes WHERE user_id = ?', (user_id,)).fetchall()
    print(user_notes)
    for note_number in notes_for_delete:
        cur.execute('DELETE FROM notes WHERE user_id = ? and note_number_for_user = ?', (user_id, note_number))
    user_notes = cur.execute('SELECT note_number_for_user, note FROM notes WHERE user_id = ?', (user_id,)).fetchall()
    print(user_notes)

    user_notes = cur.execute('SELECT note FROM notes WHERE user_id = ?', (user_id,)).fetchall()
    list_of_notes = []
    for note_number in range(len(user_notes)):
        list_of_notes.append(f'{note_number + 1}. {user_notes[note_number][0]}')
    list_of_notes = '\n'.join(list_of_notes)

    update.message.reply_text(f'''Теперь ваши заметки выглядят так:\n{list_of_notes}''')


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


# start program
if __name__ == '__main__':
    main()
