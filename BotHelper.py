import telebot
from telebot import types
from random import randint
import os
import random

# Токен вашего бота от BotFather
TOKEN = "your_bot_token_here"

# Проверяем, что токен изменен
if TOKEN == "your_bot_token_here":
    print("Ошибка: Токен бота не указан!")
    print("Получите токен у @BotFather и вставьте его в переменную TOKEN")
    exit(1)

# Создаем экземпляр бота
try:
    bot = telebot.TeleBot(TOKEN)
    print("✅ Бот успешно инициализирован!")
except Exception as e:
    print(f"❌ Ошибка при создании бота: {e}")
    exit(1)

@bot.message_handler(commands=['posts'])
def send_posts(message):
    bot.send_message(message.chat.id, "Мне всегда было интерестно видеть как люди способны с помощью ментальной арифметики производить множество вычислений за секунды.\n"
                                      "Поэтому в качестве предметной области я решил выбрать ментальную арифметику, которая развивает знания в математике и улучшает устный счёт\n")
    bot.send_message(message.chat.id, "Бот написан на языке программирование Python в среде разработки PyCharm, с использованием библиотеки telebot из Telegram Bot API.")
    bot.send_message(message.chat.id, "В результате получился бот, который расскажет в целом про этот предмет и про сложение, разность, умножение и деление в ментальной арифметике.\n"
                                      "\n"
                                      "Итоги\n"
                                      "Удобный интерфейс с inline кнопками и удобными меню.\n"
                                      "Бот незеркально отвечает на приветствия.\n"
                                      "Бот отправляет фото и видео файлы с необходимой теорией.\n"
                                      "Бот отправляет тестовые вопросы с результатами о прохождении.")


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("Меню📚", callback_data="menu")
    markup.add(btn)
    bot.send_message(message.chat.id, f"{message.from_user.first_name}, я обучающий бот 🤖.\n"
                                      "С моими возможностями можешь ознакомиться в menu.", reply_markup=markup)



# Обработчик команды /menu
@bot.message_handler(commands=['menu'])
def send_menu(message):
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("Ментальная арифметика🧮", callback_data="sections")
    markup.add(btn)

    bot.send_message(message.chat.id, "То чему я могу обучить:", reply_markup=markup)

@bot.message_handler(commands=['sections'])
def send_sections(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton("Сложение и вычитание➕➖", callback_data="mentalarithmetic_1")
    btn2 = types.InlineKeyboardButton("Умножение и деление✖➗", callback_data="mentalarithmetic_2")
    markup.add(btn1, btn2)

    bot.send_message(message.chat.id, "Разделы:", reply_markup=markup)



# Обработчик команды /mentalarithmetic_1
@bot.message_handler(commands=['mentalarithmetic_1'])
def send_mental_1(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton("Обучающее видео🎞️", callback_data="mentalvideo")
    btn2 = types.InlineKeyboardButton("Справочная информация📖", callback_data="mentaltext")
    btn3 = types.InlineKeyboardButton("Изображение🖼️", callback_data="mentalphoto")
    btn4 = types.InlineKeyboardButton("Тест📝", callback_data="mentaltest")
    btn5 = types.InlineKeyboardButton("К выбору разделов", callback_data="sections")
    markup.add(btn1, btn2, btn3, btn4, btn5)

    bot.send_message(message.chat.id, "Отлично! Вы выбрали ментальную арифметику, сложение и вычитание.", reply_markup=markup)

# Обработчик команды /mentalvideo
@bot.message_handler(commands=['mentalvideo'])
def send_video(message):
    # Открываем видеофайл и отправляем
    video = open('Videos_1/' + random.choice(os.listdir('Videos_1')), 'rb')
    bot.send_video(message.chat.id, video, timeout=20000)
    video.close()


# Обработчик команды /mentalphoto
# Создаем словарь для хранения текущего индекса фото для каждого чата
current_photo_index = {}

@bot.message_handler(commands=['mentalphoto'])
def send_pic(message, path):
    # Получаем список всех файлов в папке Pictures_1
    photos = sorted(os.listdir(path))
    # Инициализируем индекс для чата, если его нет
    if message.chat.id not in current_photo_index:
        current_photo_index[message.chat.id] = 0

    # Отправляем текущее фото
    send_photo_with_button(message.chat.id, photos, path)


def send_photo_with_button(chat_id, photos_list, path):
    # Получаем текущий индекс для чата
    index = current_photo_index.get(chat_id, 0)

    # Проверяем, не вышли ли за пределы списка
    if index >= len(photos_list):
        index = 0
        current_photo_index[chat_id] = 0

    # Открываем и отправляем фото
    photo_path = os.path.join(path, photos_list[index])
    with open(photo_path, 'rb') as photo:
        # Создаем inline-кнопку
        markup = types.InlineKeyboardMarkup()
        next_button = types.InlineKeyboardButton("Далее →", callback_data=f"next_photo:{path}")
        markup.add(next_button)

        # Отправляем фото с кнопкой
        bot.send_photo(chat_id, photo, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith("next_photo:"))
def next_photo_callback(call):
    path = call.data.split(":")[1]
    # Увеличиваем индекс для этого чата
    chat_id = call.message.chat.id
    current_photo_index[chat_id] = current_photo_index.get(chat_id, 0) + 1

    # Получаем обновленный список фото
    photos = sorted(os.listdir(path))

    # Удаляем предыдущее сообщение с фото
    bot.delete_message(chat_id, call.message.message_id)

    # Отправляем следующее фото
    send_photo_with_button(chat_id, photos, path)


# Обработчик команды /mentaltext
@bot.message_handler(commands=['mentaltext'])
def send_info(message):
    photo = open('Abacus/Soroban.png', 'rb')
    bot.send_photo(message.chat.id, photo, caption=
                                      "Абакус (соробан) — древние счёты, используемые для вычислений.\n"
                                      "Каждая спица представляет разряд (единицы, десятки, сотни и т. д.).\n"
                                      "Косточки делятся на верхние (небесные) и нижние (земные).\n"
                                      "Верхняя косточка = 5 единиц текущего разряда.\n"
                                      "Нижние косточки = по 1 единице каждая.\n")
    photo.close()
    bot.send_message(message.chat.id, "Ментальная арифметика — это методика развития умственных способностей, основанная"
                                      " на устном счёте с помощью абакуса (счётов) и визуализации. Она помогает улучшить "
                                      "концентрацию, память, скорость мышления и математические навыки.\n"
                                      "\n"
                                      "Простые вычисления на абакусе\n"
                                      "Пример сложения (3 + 4):\n"
                                      "Поднимите 3 нижние косточки (единицы).\n"
                                      "Добавьте ещё 4: так как осталась только 1 косточка, опустите верхнюю (5) и уберите 1 нижнюю (получится 5 – 1 = 4).\n"
                                      "Итог: 7.\n"
                                      "Пример вычитания (8 – 3):\n"
                                      "Отложите 8 (верхняя + 3 нижние косточки).\n"
                                      "Уберите 3: опустите верхнюю (5) и добавьте 2 (5 – 3 = 2).\n"
                                      "Итог: 5.\n"
                                      "\n"
                                      "После освоения абакуса ученики переходят к мысленному представлению счётов, двигая косточки в уме. Это развивает:\n"
                                      "Фотографическую память\n"
                                      "Скорость обработки информации\n"
                                      "Креативное мышление")







# Обработчик команды /mentalarithmetic_2
@bot.message_handler(commands=['mentalarithmetic_2'])
def send_mental_2(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton("Обучающее видео🎞️", callback_data="mentalvideo_2")
    btn2 = types.InlineKeyboardButton("Справочная информация📖", callback_data="mentaltext_2")
    btn3 = types.InlineKeyboardButton("Изображение🖼️", callback_data="mentalphoto_2")
    btn4 = types.InlineKeyboardButton("Тест📝", callback_data="mentaltest_2")
    btn5 = types.InlineKeyboardButton("К выбору разделов", callback_data="sections")
    markup.add(btn1, btn2, btn3, btn4, btn5)

    bot.send_message(message.chat.id, "Отлично! Вы выбрали ментальную арифметику, умножение и деление.", reply_markup=markup)

# Обработчик команды /mentaltext_2
@bot.message_handler(commands=['mentaltext_2'])
def send_info_2(message):
    photo = open('Abacus/Soroban1.png', 'rb')
    bot.send_photo(message.chat.id, photo)

    bot.send_message(message.chat.id, "1. Умножение на абакусе\n"
                                      "Умножение на абакусе выполняется с использованием метода распределения (разложения). Каждая цифра множителя умножается на каждую цифру множимого, а результаты складываются с учетом разрядов.\n"
    "Пример:\n"
    "23×4\n"
    "Разложим умножение:\n"
    "20×4 = 80\n"
    "3×4 = 12\n"
    "Сложим результаты:\n"
    "80 + 12 = 92.\n"

    "На абакусе это выполняется пошагово:\n"
    "Отложите 20, затем прибавьте 20×4 = 80.\n"
    "Отложите 3, затем прибавьте 3×4 = 12.\n"
    "Итог: 92.\n"

    "2.Деление на абакусе\n"
    "Деление выполняется через последовательное вычитание делителя из делимого с подсчетом количества операций.\n"

    "Пример: 56÷7\n"
    "Определим, сколько раз 7 помещается в 56:\n"
    "56−7 = 49(1раз)\n"
    "49−7 = 42(2раза)\n"
    "...\n"
    "7−7 = 0(8раз)\n"
    "Итог: 8.")


user_data = {}  # Будет хранить данные вида {chat_id: {"score": int, "current_question": int}}
t = 0


# Обработчик команды /mentaltest
@bot.message_handler(commands=['mentaltest'])
def start_test(message):
    # Инициализируем данные пользователя (результат, номер вопроса)
    user_data[message.chat.id] = {"score": 0, "current_question": 1}
    ask_question(message)
    # проверка, что открыт второй тест

# Обработчик команды /mentaltest_2 (второй тест)
@bot.message_handler(commands=['mentaltest_2'])
def start_test_2(message):
    # Инициализируем данные пользователя (результат, номер вопроса)
    user_data[message.chat.id] = {"score": 0, "current_question": 10}
    ask_question(message)


# Функция, которая задаёт вопрос пользователю
def ask_question(message):
    chat_id = message.chat.id  # сокращаем для удобства
    current_q = user_data[chat_id]["current_question"]  # берём номер вопроса

    # Создание всплывающего меню
    markup = types.ReplyKeyboardMarkup(row_width=3)
    buttons = [types.KeyboardButton(str(i)) for i in range(1, 4)]
    markup.add(*buttons)

    if current_q == 1:
        bot.send_message(chat_id, "Что такое абакус?\n"
                                  "1) Калькулятор\n"
                                  "2) Древние счёты\n"
                                  "3) Линейка", reply_markup=markup)  # Разметка ответа
    elif current_q == 2:
        bot.send_message(chat_id, "Сколько единиц представляет верхняя косточка на абакусе?\n"
                                  "1) 1\n"
                                  "2) 5\n"
                                  "3) 10", reply_markup=markup)
    elif current_q == 3:
        bot.send_message(chat_id, "Как отложить число 7 на абакусе?\n"
                                  "1) Верхняя + 2 нижние косточки\n"
                                  "2) Только верхняя\n"
                                  "3) 7 нижних косточек", reply_markup=markup)
    elif current_q == 4:
        bot.send_message(chat_id, "Как получить 4 из 9 на абакусе?\n"
                                  "1) Убрать верхнюю косточку и добавить 1 нижнюю\n"
                                  "2) Убрать верхнюю и 4 нижние\n"
                                  "3) Сбросить все косточки", reply_markup=markup)

    elif current_q == 5:
        photo = open('Abacus/7.png', 'rb')
        bot.send_photo(message.chat.id, photo, caption=
        "Какая цифра изображена на абакусе?\n"
        "1) 7\n"
        "2) 8\n"
        "3) 5", reply_markup=markup)
        photo.close()

    elif current_q == 6:
        bot.send_message(chat_id, "Как выглядит число 3 на абакусе?\n"
                                  "1) 3 нижние косточки\n"
                                  "2) Верхняя косточка\n"
                                  "3) 1 верхняя + 2 нижние", reply_markup=markup)
    elif current_q == 7:
        bot.send_message(chat_id, "Что такое ментальный счёт?\n"
                                  "1) Сложение на бумаге\n"
                                  "2) Визуализация абакуса в уме\n"
                                  "3) Использование калькулятора", reply_markup=markup)
    elif current_q == 8:
        bot.send_message(chat_id, "Какое действие выполняется: Верхняя + 1 нижняя = 6?\n"
                                  "1) 5 + 1\n"
                                  "2) 4 + 2\n"
                                  "3) 3 + 3", reply_markup=markup)

    elif current_q == 9:
        photo = open('Abacus/86.png', 'rb')
        bot.send_photo(message.chat.id, photo, caption=
        "Какое число изображено на абакусе?\n"
        "1) 28\n"
        "2) 75\n"
        "3) 86", reply_markup=markup)
        photo.close()

    if current_q == 10:
        bot.send_message(chat_id, "Как правильно умножить 15×6 на абакусе?\n"
                                  "1) 10×6=60, затем 5×6=30, итого 60+30=90\n"
                                  "2) 15+6=21\n"
                                  "3) 6×10=60, затем 6×5=30, итого 60−30=30", reply_markup=markup)  # Разметка ответа
    elif current_q == 11:
        bot.send_message(chat_id, "Как выполняется деление 72÷8 на абакусе?\n"
                                  "1) 72−8 ровно 7 раз, пока не получится 16\n"
                                  "2) 72−8 9 раз, пока не получится 0\n"
                                  "3) 8×9=72, значит, ответ 9", reply_markup=markup)
    elif current_q == 12:
        bot.send_message(chat_id, "Какой метод используется для умножения многозначных чисел на абакусе?\n"
                                  "1) Простое сложение\n"
                                  "2) Разложение по разрядам и поэтапное умножение\n"
                                  "3) Только умножение последних цифр", reply_markup=markup)
    elif current_q == 13:
        bot.send_message(chat_id, " Если при делении 45÷5 на абакусе получилось 9, сколько раз вычли 5?\n"
                                  "1) 5 раз\n"
                                  "2) 9 раз\n"
                                  "3) 10 раз", reply_markup=markup)
    elif current_q == 14:
        bot.send_message(chat_id, " Чему равно 132 ÷ 12 через разложение?\n"
                                  "1) (120÷12) + (12÷12) = 11\n"
                                  "2) (100÷12) + (32÷12) ≈ 11\n"
                                  "3) 132 ÷ (6×2) = 11", reply_markup=markup)


@bot.message_handler(func=lambda m: m.text in ['1', '2', '3'] and m.chat.id in user_data)
def handle_answer(message):
    chat_id = message.chat.id
    user_state = user_data[chat_id]
    current_q = user_state["current_question"]
    # Проверяем ответ
    if user_state["current_question"] == 1 and message.text == '2':
        user_state["score"] += 1
    elif user_state["current_question"] == 2 and message.text == '2':
        user_state["score"] += 1
    elif user_state["current_question"] == 3 and message.text == '1':
        user_state["score"] += 1
    elif user_state["current_question"] == 4 and message.text == '2':
        user_state["score"] += 1
    elif user_state["current_question"] == 5 and message.text == '1':
        user_state["score"] += 1
    elif user_state["current_question"] == 6 and message.text == '1':
        user_state["score"] += 1
    elif user_state["current_question"] == 7 and message.text == '2':
        user_state["score"] += 1
    elif user_state["current_question"] == 8 and message.text == '1':
        user_state["score"] += 1
    elif user_state["current_question"] == 9 and message.text == '3':
        user_state["score"] += 1


    elif user_state["current_question"] == 10 and message.text == '1':
        user_state["score"] += 1
    elif user_state["current_question"] == 11 and message.text == '2':
        user_state["score"] += 1
    elif user_state["current_question"] == 12 and message.text == '2':
        user_state["score"] += 1
    elif user_state["current_question"] == 13 and message.text == '2':
        user_state["score"] += 1
    elif user_state["current_question"] == 14 and message.text == '1':
        user_state["score"] += 1
    else:
        bot.send_message(chat_id, f"Неверно")

    # Переходим к следующему вопросу или завершаем тест
    if current_q < 9:  # Первый тест
        user_state["current_question"] += 1
        ask_question(message)
    elif current_q == 9:  # Завершение первого теста
        bot.send_message(chat_id, f"Вы набрали {user_state['score']}/9 баллов.",
                         reply_markup=types.ReplyKeyboardRemove())

        markup = types.InlineKeyboardMarkup(row_width=1)
        btn1 = types.InlineKeyboardButton("Назад в меню", callback_data="mentalarithmetic_1")
        markup.add(btn1)

        if user_state['score'] >= 8:
            bot.send_message(chat_id, "Отличный результат!", reply_markup=markup)
        elif user_state['score'] >= 5:
            bot.send_message(chat_id, "Нормальный результат. Вы почти у цели!", reply_markup=markup)
        else:
            bot.send_message(chat_id, "Плохой результат. Стоит подготовиться ещё.", reply_markup=markup)

        del user_data[chat_id]

    elif 10 <= current_q < 14:  # Второй тест
        user_state["current_question"] += 1
        ask_question(message)
    elif current_q == 14:  # Завершение второго теста
        bot.send_message(chat_id, f"Вы набрали {user_state['score']}/5 баллов.",
                         reply_markup=types.ReplyKeyboardRemove())

        markup = types.InlineKeyboardMarkup(row_width=1)
        btn1 = types.InlineKeyboardButton("Назад в меню", callback_data="mentalarithmetic_2")
        markup.add(btn1)

        if user_state['score'] == 5:
            bot.send_message(chat_id, "Отличный результат!", reply_markup=markup)
        elif user_state['score'] >= 3:
            bot.send_message(chat_id, "Нормальный результат. Вы почти у цели!", reply_markup=markup)
        else:
            bot.send_message(chat_id, "Плохой результат. Стоит подготовиться ещё.", reply_markup=markup)

        del user_data[chat_id]

@bot.message_handler(commands=['mentalvideo_2'])
def send_video_2(message):
    # Открываем видеофайл и отправляем
    video = open('Videos_2/' + random.choice(os.listdir('Videos_2')), 'rb')
    bot.send_video(message.chat.id, video, timeout=20000)
    video.close()



# Обработка inline кнопок
@bot.callback_query_handler(func=lambda call: True)
def handle_menu_click(call):
    if call.data == "menu":
        # Можно вызвать функцию, связанную с /menu
        send_menu(call.message)
    if call.data == "sections":
        # Можно вызвать функцию, связанную с /menu
        send_sections(call.message)


    if call.data == "mentalarithmetic_1":
        # Можно вызвать функцию, связанную с /mentalarithmetic_1
        send_mental_1(call.message)
    if call.data == "mentalvideo":
        # Можно вызвать функцию, связанную с /mentalvideo
        send_video(call.message)
    if call.data == "mentalphoto":
        # Можно вызвать функцию, связанную с /mentalphoto
        send_pic(call.message, "Pictures_1")
    if call.data == "mentaltext":
        # Можно вызвать функцию, связанную с /mentaltext
        send_info(call.message)
    if call.data == "mentaltest":
        # Можно вызвать функцию, связанную с /mentaltest
        start_test(call.message)


    if call.data == "mentalarithmetic_2":
        # Можно вызвать функцию, связанную с /mentalarithmetic_2
        send_mental_2(call.message)
    if call.data == "mentaltext_2":
        # Можно вызвать функцию, связанную с /mentaltext_2
        send_info_2(call.message)
    if call.data == "mentaltest_2":
        # Можно вызвать функцию, связанную с /mentaltest_2
        start_test_2(call.message)
    if call.data == "mentalvideo_2":
        # Можно вызвать функцию, связанную с /mentalvideo_2
        send_video_2(call.message)
    if call.data == "mentalphoto_2":
        # Можно вызвать функцию, связанную с /mentalphoto_2
        send_pic(call.message, "Pictures_2")


greetings = ['привет', 'здравствуй', 'здравствуйте', 'hello', 'hi', 'хай', 'здорова', 'добрый день', 'доброе утро',
             'добрый вечер']

@bot.message_handler(content_types=['text'])
def handle_message(message):
    # Приводим текст сообщения к нижнему регистру для проверки
    text = message.text.lower()

    # Проверяем, содержит ли сообщение приветствие
    if any(greeting in text for greeting in greetings):
        # Создаем клавиатуру с кнопками
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Что ты умеешь?")
        markup.add(btn1)

        # Генерация рандомного индекса для незеркального ответа
        while True:
            x = randint(0, 9)
            # Если рандомное слово не равно введенному, то оно используется в ответе
            if greetings[x] != text:
                word = greetings[x]
                break

        # Отправляем ответ с приветствием
        # capitalize() - делает строку с заглавной буквы
        bot.reply_to(message, f"{word.capitalize()}, {message.from_user.first_name}! 😊 Рад тебя видеть!", reply_markup=markup)
    elif "что ты умеешь" in text:
        send_welcome(message)
    else:
        bot.reply_to(message, "Извини, я не понимаю. Напиши 'привет' или любую команду во вкладке меню!")


bot.polling()