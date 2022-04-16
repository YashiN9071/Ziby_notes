# t.me/ziby_notes_bot
import logging
import sqlite3
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
# notes
notes_reply_keyboard = [['create_note', '/view_notes'],
                        ['/delete_note', '/come_back']]
notes_markup = ReplyKeyboardMarkup(notes_reply_keyboard, one_time_keyboard=True)
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
    dp.add_handler(CommandHandler('view_notes', view_notes))
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
    conn = sqlite3.connect("ziby_notes_database.db")
    cur = conn.cursor()
    all_users = [x[0] for x in cur.execute('SELECT user_id FROM users').fetchall()]
    if not user_inf[0] in all_users:
        cur.execute('INSERT INTO users VALUES (?, ?, ?);', user_inf)
        conn.commit()


def stop(update, context):
    update.message.reply_text('Значит на этом всё, надеюсь был полезен. Ваши заметки и напоминалки будут удалены.')
    return ConversationHandler.END


def help(update, context):
    update.message.reply_text(
        'У меня есть следующие функции:'
    )


def notes(update, context):
    update.message.reply_text('Здесь вы можете посмотреть все ваши существующие заметки, добавить новую\
или удалить старую заметку (Всего я могу хранить только 10 ваших заметок)', reply_markup=notes_markup)


def create_note(update, context):
    update.message.reply_text('Напишите новую заметку')
    context.args = update.message.text
    new_note = update.message.text
    user_id = update.message.from_user.id
    conn = sqlite3.connect("ziby_notes_database.db")
    cur = conn.cursor()
    quantity_notes = len(cur.execute('SELECT note FROM notes WHERE user_id = ?', (user_id,)).fetchall())
    if quantity_notes < 11:
        cur.execute('INSERT INTO notes VALUES (?, ?);', (user_id, new_note))
        conn.commit()


def view_notes(update, context):
    update.message.reply_text('Вот ваши заметки')


def delete_note(update, context):
    update.message.reply_text('Укажите номер заметки, которую хотите удалить')


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
