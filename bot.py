import logging
import sqlite3
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters

TOKEN = '5675913584:AAGH3YyB5O91wMBfHGjh6REwPWUNyYlWoO8'

def start(update, context):
    update.message.reply_text(
        "Телефонный справочник!\n"
        "Показать все записи - /info\n"
        "Поиск - /find\n"
        "Добавить - /add\n"
        "Удалить - /rem\n"
        "Изменит - /ref\n"
        )

def info(update, context):
    conn = sqlite3.connect('phonebook')
    cursor = conn.cursor()

    # показать все записи
    cursor.execute("select * from phonebook")
    results = cursor.fetchall()

    full_data = ''

    for i in range(len(results)):
        for j in range(len(results[i])):
            full_data = full_data + str(results[i][j]) + ' '
        full_data = full_data + '\n'

    update.message.reply_text(full_data)

    conn.commit()
    conn.close()

def find(update, context):
    update.message.reply_text('Введите имя для поиска')
    return 1

def find_output(update, context):
    conn = sqlite3.connect('phonebook')
    cursor = conn.cursor()

    # поиск записи
    name = update.message.text
    cursor.execute(f"select * from phonebook where name like '%{name}%'")
    results = cursor.fetchall()

    update.message.reply_text(results)

    conn.commit()
    conn.close()

def add(update, context):
    update.message.reply_text('Введите имя, телефон и описание через пробел')
    return 1

def add_output(update, context):
    conn = sqlite3.connect('phonebook')
    cursor = conn.cursor()

    # добавить
    text = update.message.text
    list = text.split()

    name = list[0]
    phone = list[1]
    desc = list[2]
    cursor.execute(
    f"insert into phonebook (name, phone, desc) "
    f"values ('{name}', {phone}, '{desc}')")

    conn.commit()
    conn.close()

def rem(update, context):
    update.message.reply_text('Введите id пользователя для удаления')
    return 1

def rem_output(update, context):
    conn = sqlite3.connect('phonebook')
    cursor = conn.cursor()

    # удалить
    id = update.message.text
    cursor.execute(
        f"delete from phonebook where id={id}"
    )

    conn.commit()
    conn.close()

def ref(update, context):
    update.message.reply_text('Введите id и новое имя пользователя через пробел')
    return 1

def ref_output(update, context):
    conn = sqlite3.connect('phonebook')
    cursor = conn.cursor()

    # обновить запись
    text = update.message.text
    list = text.split()

    id = list[0]
    name = list[1]
    cursor.execute(
        f"update phonebook set name='{name}' where id={id}"
    )

    conn.commit()
    conn.close()

def stop(update, context):
    update.message.reply_text("Всего доброго!")
    return ConversationHandler.END


def main():
    updater = Updater(TOKEN)
    find_handler = ConversationHandler(
    
        entry_points=[CommandHandler('find', find)],

        states={
            1: [MessageHandler(Filters.text & ~Filters.command, find_output)]
        },

        # Точка прерывания диалога. В данном случае — команда /stop.
        fallbacks=[CommandHandler('stop', stop)]
    )

    add_handler = ConversationHandler(
    
        entry_points=[CommandHandler('add', add)],

        states={
            1: [MessageHandler(Filters.text & ~Filters.command, add_output)]
        },

        # Точка прерывания диалога. В данном случае — команда /stop.
        fallbacks=[CommandHandler('stop', stop)]
    )

    rem_handler = ConversationHandler(
    
        entry_points=[CommandHandler('rem', rem)],

        states={
            1: [MessageHandler(Filters.text & ~Filters.command, rem_output)]
        },

        # Точка прерывания диалога. В данном случае — команда /stop.
        fallbacks=[CommandHandler('stop', stop)]
    )

    ref_handler = ConversationHandler(
    
        entry_points=[CommandHandler('ref', ref)],

        states={
            1: [MessageHandler(Filters.text & ~Filters.command, ref_output)]
        },

        # Точка прерывания диалога. В данном случае — команда /stop.
        fallbacks=[CommandHandler('stop', stop)]
    )

    start_handler = CommandHandler('start', start)
    info_handler = CommandHandler('info', info)

    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(info_handler)
    updater.dispatcher.add_handler(find_handler)
    updater.dispatcher.add_handler(add_handler)
    updater.dispatcher.add_handler(rem_handler)
    updater.dispatcher.add_handler(ref_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
