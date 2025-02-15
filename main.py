from config.auto_search_dir import data_config,  volley_preception, volley_pass, volley_attack, \
    volley_supply, borscht_sup, vegetable_soup
import urllib3
import telebot
from telebot.types import BotCommand, InlineKeyboardMarkup, InlineKeyboardButton

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

bot = telebot.TeleBot(data_config['my_telegram_bot']['bot_token'], parse_mode='HTML')


class Main:
    # дополнительный аргумент, для создания нового листа
    def __init__(self):
        self.buttons = []
        self.state_stack = {}  # Стек для хранения состояний
        self.markup = None
        self.call = None
        self.user_id = None
        self.start_main()

    def start_main(self):
        commands = [
            BotCommand("start", "В начало"),
            BotCommand("back", "Назад")
        ]
        bot.set_my_commands(commands)

        @bot.message_handler(commands=['start'])
        def handle_start_main(message):
            self.user_id = message.chat.id

            # Удаляем сообщения в диапазоне
            if message.message_id:
                for id_ in range(max(1, message.message_id - 10), message.message_id + 1):
                    try:
                        bot.delete_message(chat_id=message.chat.id, message_id=id_)
                    except:
                        continue
                        # После завершения цикла и удаления сообщений вызываем метод выбора месяца
            self.main_selection()

        @bot.message_handler(commands=['back'])
        def handle_back(message):
            if message.message_id:
                try:
                    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
                except Exception as error:
                    print(f"Ошибка при удалении сообщения в handle_back (1): {message.message_id}: {error}")
            while self.state_stack:
                last_key, last_function = self.state_stack.popitem()
                last_function()  # Попытка вызвать функцию
                break  # Выход из цикла, если вызов завершился успешно

        @bot.callback_query_handler(func=lambda call: True)
        def handle_query(call):
            self.call = call
            if self.call.data == 'Спорт':
                self.state_stack[
                    self.call.data] = self.main_selection
                self.list_sport_element()
            elif self.call.data == 'Рецепты':
                self.state_stack[
                    self.call.data] = self.main_selection
                self.list_reciepts_selection()
            elif self.call.data in ['Прием', 'Пас', 'Атака', 'Подача']:
                self.list_sport_element(self.call.data)
            elif self.call.data in ['Борщ', 'Овощной']:
                self.list_reciepts_selection(self.call.data)

    def main_selection(self):
        self.markup = InlineKeyboardMarkup()
        list_buttons = ['Спорт', 'Рецепты']
        buttons = []
        for button in list_buttons:
            item = InlineKeyboardButton(button, callback_data=button)
            buttons.append(item)
        self.markup = InlineKeyboardMarkup([buttons])

        try:
            bot.edit_message_text(
                f"Используй кнопки для навигации. Чтобы вернуться на шаг назад, используй команду /back. В начало /start\n\nВыберите раздел:",
                chat_id=self.call.message.chat.id,
                message_id=self.call.message.message_id,
                reply_markup=self.markup
            )

        except Exception as error:
            bot.send_message(self.user_id,
                             "Используй кнопки для навигации. Чтобы вернуться на шаг назад, используй команду /back. В начало /start\n\nВыберите раздел:",
                             reply_markup=self.markup)

    def list_sport_element(self, element=None):
        self.markup = InlineKeyboardMarkup()
        list_buttons = ['Прием', 'Пас', 'Атака', 'Подача']
        for button in list_buttons:
            item = InlineKeyboardButton(button, callback_data=button)
            self.markup.add(item)
        text = ''
        if element:
            if element == 'Прием':
                text = volley_preception
            elif element == 'Пас':
                text = volley_pass
            elif element == 'Атака':
                text = volley_attack
            else:
                text = volley_supply
        # Обновляем клавиатуру в том же сообщении
        bot.edit_message_text(
            f"""{text}\n\nВы находитесь в разделе: "Спорт".\n\nИспользуй кнопки для навигации. Чтобы вернуться на шаг назад, используй команду /back. В начало /start\n\nВыберете раздел:""",
            chat_id=self.call.message.chat.id,
            message_id=self.call.message.message_id,
            reply_markup=self.markup)

    def list_reciepts_selection(self, element= None):
        self.markup = InlineKeyboardMarkup()
        list_buttons = ['Борщ', 'Овощной']
        for button in list_buttons:
            item = InlineKeyboardButton(button, callback_data=button)
            self.markup.add(item)
        text = ''
        if element:
            if element == 'Борщ':
                text = borscht_sup
            elif element == 'Овощной':
                text = vegetable_soup
        # Обновляем клавиатуру в том же сообщении
        bot.edit_message_text(
            f"""{text}\n\nВы находитесь в разделе: "Рецепты".\n\nИспользуй кнопки для навигации. Чтобы вернуться на шаг назад, используй команду /back. В начало /start\n\nВыберете раздел:""",
            chat_id=self.call.message.chat.id,
            message_id=self.call.message.message_id,
            reply_markup=self.markup)


# запуск бота
while True:
    try:
        Main()
        bot.infinity_polling(timeout=90, long_polling_timeout=5)
    except Exception as e:
        continue
