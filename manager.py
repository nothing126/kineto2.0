import telebot
from telebot import types

import config
from yandex import send_message

#удаление клавиатуры с кнопками 
def remove():
    markup = types.ReplyKeyboardRemove(selective=False)
    return markup

#класс бота 
class BotManager:
#инициализация класса 
    def __init__(self, token):
        self.bot = telebot.TeleBot(token )#инициализация переменной для обращения к боту
        self.user_data = {}  # Словарь для хранения данных пользователей

    def start(self):
#реакция на команду/start
        @self.bot.message_handler(commands=['start'])
        def start(message):
            chat_id = message.chat.id
#созданик клавиатуры 
            markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
#создание кнопок 
            button1 = types.KeyboardButton("Русский")
            button2 = types.KeyboardButton("Romana")

#добавление кнопок на клавиатуру
            markup.add(button1)
            markup.add(button2)
#приветствие
            self.bot.send_message(chat_id, "Здравствуйте, выберите язык/Buna ziua,selectati limba:",
                                  reply_markup=markup)

#функция при выборе кнопки русского языка 
        @self.bot.message_handler(func=lambda message: message.text == "Русский")
        def change_ru(message):
            chat_id = message.chat.id

            self.bot.send_message(chat_id, "язык изменен на русский.Как я могу к вам обращаться?",
                                  reply_markup=remove())
            self.bot.register_next_step_handler(message, self.cause_ru)

#функция выбора румынского языка 
        @self.bot.message_handler(func=lambda message: message.text == "Romana")
        def change_ru(message):
            chat_id = message.chat.id

            self.bot.send_message(chat_id, "limba sa schimbat in romana. Cum te pot contacta",
                                  reply_markup=remove())
            self.bot.register_next_step_handler(message, self.cause_ro)

#реакция на нажатие кнопки "существующие мед.проблемы"
        @self.bot.message_handler(func=lambda message: message.text == "Существующие медицинские проблемы.")
        def problem_ru(message):
            chat_id = message.chat.id
            user_id = message.from_user.id
            user_name = self.user_data[user_id]['name']

            self.bot.send_message(chat_id, f"{user_name}, если у вас есть существующие медицинские проблемы, "
                                           "пожалуйста, расскажите о них подробнее",
                                  reply_markup=remove())
#слелующий. шаг
            self.bot.register_next_step_handler(message, self.save_medical_problem_ru)

#нажатие на кнопку "существующие мед.проблемы" на румынском 
        @self.bot.message_handler(func=lambda message: message.text == "Probleme medicale existente.")
        def problem_ru(message):
            chat_id = message.chat.id
            user_id = message.from_user.id
            user_name = self.user_data[user_id]['name']

            self.bot.send_message(chat_id, f"{user_name}, dacă aveți probleme medicale existente, "
                                           f"vă rugăm să ne spuneți mai multe despre ele",
                                  reply_markup=remove())

            self.bot.register_next_step_handler(message, self.save_medical_problem_ro)

#реакция на нажатие кнопки "дискомфорт в спине и суставах 
        @self.bot.message_handler(
            func=lambda message: message.text == "Дискомфорт или беспокойство в области спины или суставов.")
        def discomfort_ru(message):
            chat_id = message.chat.id
            user_id = message.from_user.id
            user_name = self.user_data[user_id]['name']

            self.bot.send_message(chat_id, f"{user_name},Пожалуйста, опишите характер дискомфорта и "
                                           f"его локализацию более подробно.",
                                  reply_markup=remove())
#следующий шаг
            self.bot.register_next_step_handler(message, self.reab_ru)
#реакция на "проблемы в области спины и суставов на румынском"
        @self.bot.message_handler(
            func=lambda message: message.text == "Disconfort sau neliniște în spate sau articulații.")
        def discomfort_ru(message):
            chat_id = message.chat.id
            user_id = message.from_user.id
            user_name = self.user_data[user_id]['name']

            self.bot.send_message(chat_id, f"{user_name},vă rugăm să descrieți mai detaliat natura "
                                           f"disconfortului și locația acestuia.",
                                  reply_markup=remove())

            self.bot.register_next_step_handler(message, self.reab_ro)

#реакция на кнопку "профилактика и поддержание"
        @self.bot.message_handler(
            func=lambda message: message.text == "Профилактика и поддержание физической активности.")
        def problem_ru(message):
            chat_id = message.chat.id
            user_id = message.from_user.id
            self.user_data[user_id]["cause"] = message.text
            user_name = self.user_data[user_id]['name']

            markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

            button1 = types.KeyboardButton("Специализированный массаж.")
            button2 = types.KeyboardButton("Индивидуальное занятие по кинетотерапии.")

            markup.add(button1)
            markup.add(button2)

            self.bot.send_message(chat_id, f"{user_name},какие процедуры вас интересуют?",
                                  reply_markup=markup)
            self.bot.register_next_step_handler(message, self.registrForProf_ru)

#реакция на кнопку "профилактика и поддержание" на румынском 
        @self.bot.message_handler(
            func=lambda message: message.text == "Prevenirea și menținerea activității fizice.")
        def problem_ro(message):
            chat_id = message.chat.id
            user_id = message.from_user.id
            self.user_data[user_id]["cause"] = message.text
            user_name = self.user_data[user_id]['name']

            markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

            button1 = types.KeyboardButton("Masaj specializat.")
            button2 = types.KeyboardButton("Lecție individuală de kinetoterapie.")

            markup.add(button1)
            markup.add(button2)

            self.bot.send_message(chat_id, f"{user_name},ce proceduri te intereseaza?",
                                  reply_markup=markup)
            self.bot.register_next_step_handler(message, self.registrForProf_ro)

# реакция на подтверждение регистрации 
        @self.bot.message_handler(func=lambda message: message.text == "Да")
        def confirm_prof_ru(message):
            chat_id = message.chat.id
            user_id = message.from_user.id
            user_name = self.user_data[user_id]['name']

            self.bot.send_message(chat_id, f"{user_name}введите номер телефона в формате +373******* для того "
                                           "чтобы с вами могли связаться",
                                  reply_markup=remove())

            self.bot.register_next_step_handler(message, self.sendmess1_ru)

#подтверждение регистрации на румынском 
        @self.bot.message_handler(func=lambda message: message.text == "Da")
        def confirm_prof_ro(message):
            chat_id = message.chat.id
            user_id = message.from_user.id
            user_name = self.user_data[user_id]['name']

            self.bot.send_message(chat_id, f"{user_name},introduceți numărul dvs. de telefon în formatul "
                                           f"+373******* pentru a vă putea contacta",
                                  reply_markup=remove())

            self.bot.register_next_step_handler(message, self.sendmess1_ro)

#подтверждение регистрации 
        @self.bot.message_handler(func=lambda message: message.text == "Да,хочу записаться")
        def confirm_prob_ru(message):
            chat_id = message.chat.id
            user_id = message.from_user.id
            user_name = self.user_data[user_id]['name']

            self.bot.send_message(chat_id, f"{user_name},введите номер телефона в формате +373******* для того "
                                           "чтобы с вами могли связаться",
                                  reply_markup=remove())

            self.bot.register_next_step_handler(message, self.sendmess2_ru)

#подтверждение регистрации на румынском 
        @self.bot.message_handler(func=lambda message: message.text == "Da, vreau să mă înscriu")
        def confirm_prob_ro(message):
            chat_id = message.chat.id
            user_id = message.from_user.id
            user_name = self.user_data[user_id]['name']

            self.bot.send_message(chat_id, f"{user_name},introduceți numărul dvs. de telefon în formatul "
                                           f"+373******* pentru a vă putea contacta",
                                  reply_markup=remove())

            self.bot.register_next_step_handler(message, self.sendmess2_ro)

#подтвержденик регистрации 
        @self.bot.message_handler(func=lambda message: message.text == "Да,готов записаться")
        def confirm_prob_ru(message):
            chat_id = message.chat.id
            user_id = message.from_user.id
            user_name = self.user_data[user_id]['name']

            self.bot.send_message(chat_id, f"{user_name},введите номер телефона в формате +373******* для того "
                                           "чтобы с вами могли связаться",
                                  reply_markup=remove())

            self.bot.register_next_step_handler(message, self.sendmess3_ru)

#подтверждение регистрации на румынском 
        @self.bot.message_handler(func=lambda message: message.text == "Da, sunt gata să mă înscriu")
        def confirm_prob_ru(message):
            chat_id = message.chat.id
            user_id = message.from_user.id
            user_name = self.user_data[user_id]['name']

            self.bot.send_message(chat_id, f"{user_name},introduceți numărul dvs. de telefon în formatul "
                                           f"+373******* pentru a vă putea contacta",
                                  reply_markup=remove())

            self.bot.register_next_step_handler(message, self.sendmess3_ro)

        @self.bot.message_handler(func=lambda message: message.text == "Nu, mulțumesc")
        def confirm_prob_ro(message):
            chat_id = message.chat.id

            self.bot.send_message(chat_id, "Vă mulțumim că ne-ați contactat! Nu uita să ai grijă de sănătatea ta. "
                                           "Dacă sunt necesare sfaturi suplimentare, "
                                           "nu ezitați să contactați.La revedere și sănătate",
                                  reply_markup=remove())

#отказ от регистрации 
        @self.bot.message_handler(func=lambda message: message.text == "Нет, спасибо")
        def confirm_prob_ru(message):
            chat_id = message.chat.id

            self.bot.send_message(chat_id, "Спасибо за обращение! Не забывайте заботиться о своем здоровье. "
                                           "Если потребуется дополнительная консультация, не стесняйтесь обращаться."
                                           " До свидания и здоровья",
                                  reply_markup=remove())

        self.bot.polling()

#обрабртка выбора языка
    def language_handler(self, message):
        if message.text == "Romana":
            self.bot.register_next_step_handler(message, self.cause_ro)
        elif message.text == "Русский":
            self.bot.register_next_step_handler(message, self.cause_ru)

#предложение регистрации 
    def reab_ru(self, message):
        discomfort = message.text
        chat_id = message.chat.id
        user_id = message.from_user.id
        user_name = self.user_data[user_id]['name']

        self.user_data[user_id]["disc"] = discomfort

        markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

        button1 = types.KeyboardButton("Да,готов записаться")
        button2 = types.KeyboardButton("Нет, спасибо")

        markup.add(button1)
        markup.add(button2)

        self.bot.send_message(chat_id,
                              f"{user_name},для разработки программы по реабилитации необходима консультация "
                              f"специалиста. Мы предлагаем вам запись на консультацию и пробную процедуру для "
                              f"определения наилучшего способа помощи. Готовы ли вы записаться на консультацию?",
                              reply_markup=markup)

#предложение регистрации на румынском 
    def reab_ro(self, message):
        discomfort = message.text
        chat_id = message.chat.id
        user_id = message.from_user.id
        user_name = self.user_data[user_id]['name']

        self.user_data[user_id]["disc"] = discomfort

        markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

        button1 = types.KeyboardButton("Da, sunt gata să mă înscriu")
        button2 = types.KeyboardButton("Nu, mulțumesc")

        markup.add(button1)
        markup.add(button2)

        self.bot.send_message(chat_id,
                              f"{user_name},Pentru a dezvolta un program de reabilitare, este necesară consultarea"
                              f" unui specialist. Vă oferim o programare pentru o consultație și o procedură de probă "
                              f"pentru a determina cea mai bună modalitate de a ajuta. "
                              f"Sunteți gata să programați o consultație?",
                              reply_markup=markup)
#выбор причины обращения 
    def cause_ru(self, message):
        chat_id = message.chat.id
        user_id = message.from_user.id
        user_name = message.text

        self.user_data[user_id] = {"name": user_name}  # Сохраняем имя пользователя в словаре

        markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

        button1 = types.KeyboardButton("Существующие медицинские проблемы.")
        button2 = types.KeyboardButton("Профилактика и поддержание физической активности.")
        button3 = types.KeyboardButton("Дискомфорт или беспокойство в области спины или суставов.")

        markup.add(button1)
        markup.add(button2)
        markup.add(button3)

        self.bot.send_message(chat_id, f"Что привело вас сегодня, {user_name} ?",
                              reply_markup=markup)

#выбор причины обращения на румынском 
    def cause_ro(self, message):
        chat_id = message.chat.id
        user_id = message.from_user.id
        user_name = message.text

        self.user_data[user_id] = {"name": user_name}  # Сохраняем имя пользователя в словаре

        markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

        button1 = types.KeyboardButton("Probleme medicale existente.")
        button2 = types.KeyboardButton("Prevenirea și menținerea activității fizice.")
        button3 = types.KeyboardButton("Disconfort sau neliniște în spate sau articulații.")

        markup.add(button1)
        markup.add(button2)
        markup.add(button3)

        self.bot.send_message(chat_id, f"Ce vă aduce astăzi, {user_name} ?",
                              reply_markup=markup)

#предложение регистрации 
    def registrForProf_ru(self, message):
        chat_id = message.chat.id

        markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

        button1 = types.KeyboardButton("Да")
        button2 = types.KeyboardButton("Нет, спасибо")

        markup.add(button1)
        markup.add(button2)

        self.bot.send_message(chat_id, "Желаете ли вы записаться на процедуру?",
                              reply_markup=markup)
#предложение регистрации на румынском 
    def registrForProf_ro(self, message):
        chat_id = message.chat.id

        markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

        button1 = types.KeyboardButton("Da")
        button2 = types.KeyboardButton("Nu, mulțumesc")

        markup.add(button1)
        markup.add(button2)

        self.bot.send_message(chat_id, "Doriți să faceți o programare pentru procedură?",
                              reply_markup=markup)

#получение мед. проблемы 
    def save_medical_problem_ru(self, message):
        chat_id = message.chat.id
        user_id = message.from_user.id
        user_name = self.user_data[user_id]['name']
        medical_problem = message.text

        self.user_data[user_id]["problem"] = medical_problem

        self.bot.send_message(chat_id, f"{user_name},ваш случай требует более детальной оценки и "
                                       f"консультации нашего специалиста. "
                                       f"Мы рекомендуем вам записаться на консультацию.")

        markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

        button1 = types.KeyboardButton("Да,хочу записаться")
        button2 = types.KeyboardButton("Нет, спасибо")

        markup.add(button1)
        markup.add(button2)

        self.bot.send_message(chat_id, "Желаете ли вы записаться на процедуру?",
                              reply_markup=markup)

#получение мед. проблемы на румынском 
    def save_medical_problem_ro(self, message):
        chat_id = message.chat.id
        user_id = message.from_user.id
        user_name = self.user_data[user_id]['name']
        medical_problem = message.text

        self.user_data[user_id]["problem"] = medical_problem

        self.bot.send_message(chat_id, f"{user_name},cazul dumneavoastră necesită o evaluare mai detaliată și o "
                                       f"consultare cu specialistul nostru. Vă recomandăm să programați o consultație.",
                              reply_markup=remove())

        markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

        button1 = types.KeyboardButton("Da, vreau să mă înscriu")
        button2 = types.KeyboardButton("Nu, mulțumesc")

        markup.add(button1)
        markup.add(button2)

        self.bot.send_message(chat_id, "Doriți să faceți o programare pentru procedură?",
                              reply_markup=markup)

#отправка данных пользователя на почту и благодарность 
    def sendmess1_ru(self, message):
        phone_num = message.text
        chat_id = message.chat.id
        user_id = message.from_user.id
        user_name = self.user_data[user_id]['name']
        cause = self.user_data[user_id]['cause']

        send_message(config.MAIL, "новый на профилактику", f"имя:{user_name}\n"
                                                           f"причина обращения:{cause}\n"
                                                           f"номер телефона:{phone_num}")

        self.bot.send_message(chat_id, f"{user_name}, отлично! Ваш запрос принят. "
                                       f"Я свяжусь с вами в ближайшее время для уточнения деталей.",
                              reply_markup=remove())

#отправка данных пользователя на почту и благодарность на рум
    def sendmess1_ro(self, message):
        phone_num = message.text
        chat_id = message.chat.id
        user_id = message.from_user.id
        user_name = self.user_data[user_id]['name']
        cause = self.user_data[user_id]['cause']

        send_message(config.MAIL, "новый на профилактику", f"имя:{user_name}\n"
                                                           f"причина обращения:{cause}\n"
                                                           f"номер телефона:{phone_num}")

        self.bot.send_message(chat_id, f"{user_name}, Grozav! Solicitarea dvs. a fost acceptată. "
                                       f"Vă voi contacta în scurt timp pentru a clarifica detalii.",
                              reply_markup=remove())

#отправка данных пользователя на почту и благодарность 
    def sendmess2_ru(self, message):
        phone_num = message.text
        chat_id = message.chat.id
        user_id = message.from_user.id
        user_name = self.user_data[user_id]['name']
        medical_problem = self.user_data[user_id]['problem']

        send_message(config.MAIL, "новый пациент c проблемой", f"имя:{user_name}\n"
                                                               f"проблема:{medical_problem}\n"
                                                               f"номер телефона:{phone_num}")

        self.bot.send_message(chat_id, f"{user_name}, отлично! Ваш запрос принят. "
                                       f"Я свяжусь с вами в ближайшее время для уточнения деталей.",
                              reply_markup=remove())


#отправка данных пользователя на почту и благодарность на рум
    def sendmess2_ro(self, message):
        phone_num = message.text
        lang = "romana"
        chat_id = message.chat.id
        user_id = message.from_user.id
        user_name = self.user_data[user_id]['name']
        medical_problem = self.user_data[user_id]['problem']

        send_message(config.MAIL, "новый пациент c проблемой", f"имя:{user_name}\n"
                                                               f"проблема:{medical_problem}\n"
                                                               f"номер телефона:{phone_num}\n"
                                                               f"язык:{lang}")
        self.bot.send_message(chat_id, f"{user_name}, Grozav! Solicitarea dvs. a fost acceptată. "
                                       f"Vă voi contacta în scurt timp pentru a clarifica detalii.",
                              reply_markup=remove())


#отправка данных пользователя на почту и благодарность     def sendmess3_ru(self, message):
        lang = "русский"
        phone_num = message.text
        chat_id = message.chat.id
        user_id = message.from_user.id
        user_name = self.user_data[user_id]['name']
        disc = self.user_data[user_id]['disc']

        send_message(config.MAIL, "новый пациент дискомфортом",
                     f"имя:{user_name}\n"
                     f"характер дискомфорта:{disc}\n"
                     f"номер телефона:{phone_num}\n"
                     f"язык:{lang}")

        self.bot.send_message(chat_id, f"{user_name}, отлично! Ваш запрос принят. "
                                       f"Я свяжусь с вами в ближайшее время для уточнения деталей.",
                              reply_markup=remove())

#отправка данных пользователя на почту и благодарность на рум
    def sendmess3_ro(self, message):
        lang = "romana"
        phone_num = message.text
        chat_id = message.chat.id
        user_id = message.from_user.id
        user_name = self.user_data[user_id]['name']
        disc = self.user_data[user_id]['disc']

        send_message(config.MAIL, "новый пациент дискомфортом",
                     f"имя:{user_name}\n"
                     f"характер дискомфорта:{disc}\n"
                     f"номер телефона:{phone_num}\n"
                     f"язык:{lang}")

        self.bot.send_message(chat_id, f"{user_name}, Grozav! Solicitarea dvs. a fost acceptată. "
                                       f"Vă voi contacta în scurt timp pentru a clarifica detalii.",
                              reply_markup=remove())
